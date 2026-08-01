import os
from src.log_reader import read_logs
from src.ip_detector import detect_suspicious_ips
from src.report_generator import generate_report


def make_log(tmp_path, content):
    log = tmp_path / "test.log"
    log.write_text(content)
    return str(log)


def test_read_logs_returns_list(tmp_path):
    path = make_log(
        tmp_path,
        "2026-06-14 09:15:42 | 203.0.113.45 | POST /api/login | 401\n"
        "2026-06-14 09:16:01 | 49.205.10.8 | GET /api/orders | 200\n",
    )
    result = read_logs(path)
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], dict)
    assert len(result[0]) == 4


def test_repeated_failures_flagged(tmp_path):
    path = make_log(
        tmp_path,
        "2026-06-14 09:15:42 | 203.0.113.45 | POST /api/login | 401\n"
        "2026-06-14 09:15:44 | 203.0.113.45 | POST /api/login | 401\n"
        "2026-06-14 09:15:46 | 203.0.113.45 | POST /api/login | 401\n"
        "2026-06-14 09:16:01 | 49.205.10.8 | GET /api/orders | 200\n",
    )
    logs = read_logs(path)
    suspicious = detect_suspicious_ips(logs)
    assert "203.0.113.45" in suspicious


def test_clean_ip_not_flagged(tmp_path):
    path = make_log(
        tmp_path,
        "2026-06-14 09:15:42 | 203.0.113.45 | POST /api/login | 401\n"
        "2026-06-14 09:15:44 | 203.0.113.45 | POST /api/login | 401\n"
        "2026-06-14 09:15:46 | 203.0.113.45 | POST /api/login | 401\n"
        "2026-06-14 09:16:01 | 49.205.10.8 | GET /api/orders | 200\n",
    )
    logs = read_logs(path)
    suspicious = detect_suspicious_ips(logs)
    assert "49.205.10.8" not in suspicious


def test_report_file_created(tmp_path):
    path = make_log(
        tmp_path,
        "2026-06-14 09:15:42 | 203.0.113.45 | POST /api/login | 401\n"
        "2026-06-14 09:15:44 | 203.0.113.45 | POST /api/login | 401\n"
        "2026-06-14 09:15:46 | 203.0.113.45 | POST /api/login | 401\n",
    )
    logs = read_logs(path)
    suspicious = detect_suspicious_ips(logs)
    report_path = generate_report(suspicious)
    assert os.path.exists(report_path)


def test_missing_file_handled():
    result = read_logs("data/this_file_does_not_exist.log")
    assert result == []
