import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.signatures import naive_search, kmp_search  # noqa: E402

text = "a" * 300000 + "b"
pattern = "a" * 200 + "b"

start = time.perf_counter()
naive_search(text, pattern)
naive_time = time.perf_counter() - start

start = time.perf_counter()
kmp_search(text, pattern)
kmp_time = time.perf_counter() - start

print(f"naive_search: {naive_time * 1000:.2f} ms")
print(f"kmp_search:   {kmp_time * 1000:.2f} ms")
