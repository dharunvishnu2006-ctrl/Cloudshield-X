import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

n = 100000

data_for_append = []
start = time.perf_counter()
for i in range(n):
    data_for_append.append(i)
append_time = time.perf_counter() - start

data_for_insert: list[int] = []
start = time.perf_counter()
for i in range(n):
    data_for_insert.insert(0, i)
insert_time = time.perf_counter() - start

print(f"append x{n}:     {append_time * 1000:.2f} ms")
print(f"insert(0,x) x{n}: {insert_time * 1000:.2f} ms")
print(f"insert(0,x) is {insert_time / append_time:.0f}x slower")
