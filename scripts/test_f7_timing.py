import sys
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ranking import bubble_sort, selection_sort, insertion_sort  # noqa: E402

random.seed(42)
data = [random.randint(1, 100000) for _ in range(5000)]

for name, sort_fn in [
    ("bubble_sort", bubble_sort),
    ("selection_sort", selection_sort),
    ("insertion_sort", insertion_sort),
]:
    start = time.perf_counter()
    result = sort_fn(data)
    elapsed = time.perf_counter() - start
    assert result == sorted(data), f"{name} produced incorrect output!"
    print(f"{name}: {elapsed * 1000:.2f} ms")
