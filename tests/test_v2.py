import sqlite3
import pytest
from src.db import get_conn, init_db, insert_events, upsert_ip
from src.reports import (
    top_attackers,
    readable_events,
    never_attacked_ips,
    propagation_trace,
)
from src.analytics_v2 import escalation_detector
from src.ioc_store import IOCStore, compare_feeds, DomainTrie
from src.ranking import (
    bubble_sort,
    merge_sort,
    quick_sort,
    counting_sort_severity,
    top_k_threats,
)
from src.bst import BST, AVLTree
from src.pipeline import linear_scan, binary_search, first_line_at_or_after
from src.lru_cache import LRUCache
from src.scanner_pipeline import brackets_balanced, AlertQueue
from src.attack_graph import AttackGraph
from src.burst import sliding_window_burst
from src.planner import prioritize, greedy_plan
from src.signatures import naive_search, kmp_search, in_subnet


def test_schema_and_fk():
    init_db()
    conn = get_conn()
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    table_names = [t["name"] for t in tables]
    assert "ip_addresses" in table_names
    assert "threat_actors" in table_names
    assert "security_events" in table_names
    conn.close()


def test_bad_foreign_key_rejected():
    conn = get_conn()
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO security_events (event_time, source_ip)" "VALUES (?, ?)",
                ("2026-08-05T10:00:00", 99999),
            )
    finally:
        conn.close()


def test_index_is_used():
    conn = get_conn()
    plan = conn.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM security_events WHERE source_ip = 1"
    ).fetchall()
    conn.close()
    plan_text = " ".join(row["detail"] for row in plan)
    assert "USING INDEX" in plan_text


def test_top_attackers():
    init_db()
    insert_events(
        [
            {"ip": "77.77.77.77", "event_time": f"2026-08-05T10:{i:02d}", "status": 403}
            for i in range(10)
        ]
    )
    results = top_attackers(min_hits=5, limit=10)
    matching = [r for r in results if r["ip"] == "77.77.77.77"]
    assert len(matching) == 1
    assert matching[0]["hits"] == 10


def test_severity_label_critical():
    init_db()
    insert_events(
        [
            {
                "ip": "8.8.8.8",
                "event_time": "2026-08-05T11:00",
                "status": 403,
                "severity_score": 9,
            }
        ]
    )
    rows = readable_events(limit=50)
    matching = [r for r in rows if r["ip"] == "8.8.8.8"]
    assert matching[0]["severity_label"] == "CRITICAL"


def test_left_join_finds_quiet_ips():
    init_db()
    upsert_ip("172.16.0.1", "2026-08-05")
    quiet_ips = never_attacked_ips()
    assert "172.16.0.1" in quiet_ips


def test_inner_join_excludes_never_attacked():
    init_db()
    insert_events(
        [
            {
                "ip": "192.168.1.1",
                "event_time": "2026-08-05T14:00",
                "status": 200,
            }
        ]
    )
    quiet_ips = never_attacked_ips()
    assert "192.168.1.1" not in quiet_ips


def test_lag_detects_escalation():
    init_db()
    insert_events(
        [
            {
                "ip": "99.99.99.1",
                "event_time": "2026-08-05T20:00",
                "severity_score": 2.2,
            },
            {
                "ip": "99.99.99.1",
                "event_time": "2026-08-05T20:05",
                "severity_score": 5.5,
            },
            {
                "ip": "99.99.99.1",
                "event_time": "2026-08-05T20:10",
                "severity_score": 8.8,
            },
            {
                "ip": "99.99.99.2",
                "event_time": "2026-08-05T21:00",
                "severity_score": 4.4,
            },
            {
                "ip": "99.99.99.2",
                "event_time": "2026-08-05T21:05",
                "severity_score": 4.4,
            },
        ]
    )
    rows = escalation_detector(limit=1000)

    rising_row = next(r for r in rows if r["severity_score"] == 8.8)
    assert rising_row["prev_severity"] == 5.5

    flat_row = next(
        r for r in rows if r["severity_score"] == 4.4 and r["prev_severity"] == 4.4
    )
    assert flat_row["prev_severity"] == flat_row["severity_score"]


def test_recursive_cte_terminates():
    conn = get_conn()
    conn.executemany(
        "INSERT INTO host_links (src_host, dst_host) VALUES (?, ?)",
        [
            ("test-A", "test-B"),
            ("test-B", "test-C"),
            ("test-C", "test-A"),
        ],
    )
    conn.commit()
    conn.close()

    results = propagation_trace("test-A", max_hops=6)
    hosts_found = {r["host"] for r in results}

    assert hosts_found == {"test-A", "test-B", "test-C"}
    assert len(results) == 3


def test_hash_table_stores_and_finds():
    store = IOCStore()
    store.add("185.220.101.5")
    assert store.is_blocked("185.220.101.5") is True
    assert store.is_blocked("9.9.9.9") is False


def test_hash_table_survives_collision():
    store = IOCStore()
    store.add("test-key-11")
    store.add("test-key-20")
    assert store.is_blocked("test-key-11") is True
    assert store.is_blocked("test-key-20") is True


def test_compare_feeds_intersection_and_difference():
    feed_a = {"1.1.1.1", "2.2.2.2", "3.3.3.3"}
    feed_b = {"2.2.2.2", "3.3.3.3", "4.4.4.4"}
    result = compare_feeds(feed_a, feed_b)
    assert result["agreed"] == {"2.2.2.2", "3.3.3.3"}
    assert result["only_in_a"] == {"1.1.1.1"}
    assert result["only_in_b"] == {"4.4.4.4"}


def test_trie_matches_subdomains():
    trie = DomainTrie()
    trie.insert("evil.com")
    assert trie.matches("login.evil.com") is True
    assert trie.matches("evilbank.com") is False


def test_sorts_agree_with_python_sorted():
    import random

    random.seed(7)
    data = [random.randint(1, 1000) for _ in range(200)]
    expected = sorted(data)
    assert bubble_sort(data) == expected
    assert merge_sort(data) == expected
    assert quick_sort(data) == expected


def test_counting_sort_severity_buckets():
    assert counting_sort_severity([2, 0, 1, 2, 0, 3, 1]) == [0, 0, 1, 1, 2, 2, 3]


def test_top_k_matches_full_sort():
    import random

    random.seed(11)
    data = [random.randint(1, 100000) for _ in range(500)]
    heap_result = top_k_threats(data, k=10)
    full_sort_result = sorted(data, reverse=True)[:10]
    assert heap_result == full_sort_result


def test_bst_degrades_avl_stays_balanced():
    bst = BST()
    avl = AVLTree()
    for value in [1, 2, 3, 4, 5]:
        bst.insert(value)
        avl.insert(value)
    assert bst.height() == 5
    assert avl.height() == 3


def test_binary_search_matches_linear_search():
    data = sorted([3, 7, 1, 9, 4, 8, 2, 10, 6, 5])
    assert binary_search(data, 7) == linear_scan(data, 7)
    assert binary_search(data, 99) == linear_scan(data, 99)


def test_first_line_at_or_after_finds_gaps_boundary():
    timestamps = ["10:00", "10:05", "10:05", "10:10", "10:15"]
    idx = first_line_at_or_after(timestamps, "10:07")
    assert timestamps[idx] == "10:10"


def test_lru_evicts_oldest():
    cache = LRUCache(capacity=3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    cache.get("a")
    cache.put("d", 4)
    assert cache.get("b") is None
    assert cache.get("a") == 1


def test_brackets_balanced_catches_mismatch():
    assert brackets_balanced("{[}]") is False
    assert brackets_balanced("{[]}") is True


def test_alert_queue_is_fifo_not_lifo():
    queue = AlertQueue()
    queue.enqueue("A")
    queue.enqueue("B")
    queue.enqueue("C")
    assert queue.dequeue() == "A"
    assert queue.dequeue() == "B"
    assert queue.dequeue() == "C"


def test_dijkstra_beats_bfs_on_weights():
    g = AttackGraph()
    g.add_edge("A", "B", weight=1)
    g.add_edge("B", "D", weight=1)
    g.add_edge("A", "D", weight=8)

    bfs_result = g.bfs("A", max_hops=3)
    assert bfs_result["D"] == 1

    dijkstra_path, dijkstra_cost = g.dijkstra("A", "D")
    assert dijkstra_path == ["A", "B", "D"]
    assert dijkstra_cost == 2.0


def test_no_path_when_isolated():
    g = AttackGraph()
    g.add_edge("A", "B", weight=1)
    g.adjacency["isolated-host"] = []

    path, cost = g.dijkstra("A", "isolated-host")
    assert path == []
    assert cost == float("inf")


def test_sliding_window_burst():
    events = [
        ("1.1.1.1", 0),
        ("1.1.1.1", 1),
        ("1.1.1.1", 2),
        ("1.1.1.1", 3),
        ("1.1.1.1", 4),
        ("1.1.1.1", 5),
    ]
    result = sliding_window_burst(events, seconds=60, threshold=5)
    assert len(result) > 0

    quiet_events = [("1.1.1.1", i * 100) for i in range(6)]
    quiet_result = sliding_window_burst(quiet_events, seconds=60, threshold=5)
    assert len(quiet_result) == 0


def test_dp_beats_greedy():
    threats = [("A", 5, 4), ("B", 4, 3), ("C", 3, 2)]
    dp_total, dp_chosen = prioritize(threats, budget=5)
    greedy_total, greedy_chosen = greedy_plan(threats, budget=5)

    assert dp_total == 7
    assert greedy_total == 5
    assert dp_total > greedy_total


def test_knapsack_respects_budget():
    threats = [("X", 10, 6), ("Y", 8, 4), ("Z", 5, 2)]
    total, chosen = prioritize(threats, budget=6)

    used_effort = sum(effort for name, risk, effort in threats if name in chosen)
    assert used_effort <= 6


def test_kmp_matches_naive():
    text = "mississippi"
    pattern = "issi"
    assert kmp_search(text, pattern) == naive_search(text, pattern)
    assert kmp_search(text, pattern) == [1, 4]


def test_in_subnet_checks_a_whole_block():
    assert in_subnet("203.0.113.5", "203.0.113.0/24") is True
    assert in_subnet("203.0.113.200", "203.0.113.0/24") is True
    assert in_subnet("203.0.114.5", "203.0.113.0/24") is False


def test_scan_endpoint_rejects_bad_path():
    from src.api import app

    client = app.test_client()
    r = client.post("/scan", json={"log_path": "/etc/passwd"})
    assert r.status_code == 400


def test_threats_endpoint_returns_list():
    from src.api import app

    insert_events([{"ip": "50.1.1.1", "event_time": "2026-08-07T10:00", "status": 403}])
    client = app.test_client()
    r = client.get("/threats?limit=5")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)


def test_plan_endpoint_matches_dp_counterexample():
    from src.api import app

    client = app.test_client()
    r = client.post(
        "/plan",
        json={"threats": [["A", 5, 4], ["B", 4, 3], ["C", 3, 2]], "budget": 5},
    )
    data = r.get_json()
    assert r.status_code == 200
    assert data["total_risk_reduced"] == 7
    assert set(data["chosen"]) == {"B", "C"}


def test_propagation_endpoint_requires_host():
    from src.api import app

    client = app.test_client()
    r = client.get("/propagation")
    assert r.status_code == 400


def test_health_endpoint_returns_real_fields():
    from src.api import app

    client = app.test_client()
    r = client.get("/health")
    data = r.get_json()

    assert r.status_code == 200
    assert data["database"] == "connected"
    assert "tables" in data
    assert "graph_hosts" in data
    assert "cache_hit_rate" in data


def test_health_graph_hosts_counts_destination_only_host():
    from src.db import get_conn
    from src.health import build_health_report

    conn = get_conn()
    conn.executemany(
        "INSERT INTO host_links (src_host, dst_host) VALUES (?, ?)",
        [("hh-1", "hh-2"), ("hh-2", "hh-3")],
    )
    conn.commit()
    conn.close()

    report = build_health_report()
    assert report["graph_hosts"]
