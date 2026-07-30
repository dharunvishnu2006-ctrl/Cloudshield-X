import time
import threading
import asyncio
import hashlib
from pathlib import Path
from src.reader import read_events
from src.logging_setup import setup_logging

setup_logging()

LOG_FILE = "data/sample_server.log"
NUM_FILES = 6


def io_workload_sequential() -> float:
    start = time.perf_counter()
    for _ in range(NUM_FILES):
        events = list(read_events(LOG_FILE))
    return time.perf_counter() - start


def io_workload_threaded() -> float:
    start = time.perf_counter()
    threads = []
    for _ in range(NUM_FILES):
        t = threading.Thread(
            target=lambda: list(read_events(LOG_FILE))
        )
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start


async def io_workload_async() -> float:
    start = time.perf_counter()

    async def read_one():
        return list(read_events(LOG_FILE))

    tasks = [read_one() for _ in range(NUM_FILES)]
    await asyncio.gather(*tasks)
    return time.perf_counter() - start


def cpu_workload_sequential() -> float:
    start = time.perf_counter()
    for _ in range(NUM_FILES):
        for event in read_events(LOG_FILE):
            hashlib.sha256(event.ip.encode()).hexdigest()
    return time.perf_counter() - start


print("=" * 50)
print("BENCHMARKING — I/O WORKLOAD")
print("=" * 50)

seq = io_workload_sequential()
print(f"Sequential:  {seq*1000:.1f}ms")

thr = io_workload_threaded()
print(f"Threaded:    {thr*1000:.1f}ms")

asyn = asyncio.run(io_workload_async())
print(f"Async:       {asyn*1000:.1f}ms")

print("\n" + "=" * 50)
print("BENCHMARKING — CPU WORKLOAD")
print("=" * 50)

seq_cpu = cpu_workload_sequential()
print(f"Sequential:  {seq_cpu*1000:.1f}ms")
print("Processes: skipped on Windows notebook")