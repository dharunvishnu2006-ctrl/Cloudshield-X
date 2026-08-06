import sys
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ranking import top_k_threats  # noqa: E402

random.seed(42)
data = [random.randint(1, 1000000) for _ in range(50000)]

start = time.perf_counter()
heap_result = top_k_threats(data, k=10)
heap_time = time.perf_counter() - start

start = time.perf_counter()
sorted_result = sorted(data, reverse=True)[:10]
sorted_time = time.perf_counter() - start

assert heap_result == sorted_result, "Results don't match!"

print(f"top_k_threats (min-heap): {heap_time * 1000:.2f} ms")
print(f"sorted(...)[:10]:         {sorted_time * 1000:.2f} ms")
print(f"heap is {sorted_time / heap_time:.1f}x faster")
