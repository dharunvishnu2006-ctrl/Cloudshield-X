import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ioc_store import IOCStore  # noqa: E402

indicators = [f"192.0.2.{i % 256}.{i}" for i in range(10000)]

indicator_list = list(indicators)

store = IOCStore(num_buckets=4096)
for ip in indicators:
    store.add(ip)

target = indicators[9999]

start = time.perf_counter()
found_list = target in indicator_list
list_time = time.perf_counter() - start

start = time.perf_counter()
found_hash = store.is_blocked(target)
hash_time = time.perf_counter() - start

print(f"list scan:  {list_time * 1000:.4f} ms  (found={found_list})")
print(f"hash table: {hash_time * 1000:.4f} ms  (found={found_hash})")
print(f"hash table is {list_time / hash_time:.0f}x faster")
