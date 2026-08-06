import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ioc_store import IOCStore  # noqa: E402

store = IOCStore()
seen: dict[int, str] = {}
key_a, key_b = None, None

for i in range(1000):
    key = f"test-key-{i}"
    idx = store._hash(key)
    if idx in seen:
        key_a, key_b = seen[idx], key
        print(f"COLLISION FOUND: {key_a} and {key_b} both hash to bucket {idx}")
        break
    seen[idx] = key
if key_a is None or key_b is None:
    raise RuntimeError("No collision found in 1000 tries — try a bigger range")


store.add(key_a)
store.add(key_b)
print(f"bucket contents: {store.buckets[store._hash(key_a)]}")
print(f"is_blocked({key_a}):", store.is_blocked(key_a))
print(f"is_blocked({key_b}):", store.is_blocked(key_b))
