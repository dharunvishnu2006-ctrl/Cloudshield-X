from src.db import get_conn

conn = get_conn()
conn.execute("DELETE FROM host_links")  # start clean

chain = [
    ("web-server", "app-server"),
    ("app-server", "db-server"),
    ("app-server", "auth-server"),
    ("db-server", "payments-server"),
    ("auth-server", "admin-console"),
]
conn.executemany(
    "INSERT INTO host_links (src_host, dst_host) VALUES (?, ?)",
    chain,
)
conn.commit()
print(f"Seeded {len(chain)} host links for the demo.")
