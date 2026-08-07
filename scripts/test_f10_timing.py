import sys
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.burst import sliding_window_burst  # noqa: E402


def naive_burst(events: list, seconds: int = 60, threshold: int = 100) -> list:
    """The slow way: re-count the whole window from scratch for every event."""
    bursts = []
    for i in range(len(events)):
        count = 0
        for j in range(i, -1, -1):
            if events[i][1] - events[j][1] > seconds:
                break
            count += 1
        if count > threshold:
            bursts.append((events[i][1], count))
    return bursts


random.seed(3)
events = sorted([("1.1.1.1", i) for i in range(100000)], key=lambda e: e[1])

start = time.perf_counter()
sliding_result = sliding_window_burst(events, seconds=60, threshold=50)
sliding_time = time.perf_counter() - start

start = time.perf_counter()
naive_result = naive_burst(events, seconds=60, threshold=50)
naive_time = time.perf_counter() - start

print(f"sliding_window_burst: {sliding_time * 1000:.2f} ms")
print(f"naive_burst:           {naive_time * 1000:.2f} ms")
print(f"sliding window is {naive_time / sliding_time:.0f}x faster")
