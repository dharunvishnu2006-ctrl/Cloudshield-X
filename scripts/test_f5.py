import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.db import get_conn  # noqa: E402

conn = get_conn()
conn.executemany(
    "INSERT INTO host_links (src_host, dst_host) VALUES (?, ?)",
    [
        ("host-A", "host-B"),
        ("host-B", "host-C"),
        ("host-C", "host-D"),
        ("host-C", "host-A"),
    ],
)
conn.commit()
conn.close()
print("test chain inserted, with a cycle: A -> B -> C -> D, and C -> A")
