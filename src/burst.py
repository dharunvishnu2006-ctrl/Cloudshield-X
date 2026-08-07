def sliding_window_burst(events: list, seconds: int = 60, threshold: int = 100) -> list:
    """Find windows where more than `threshold` events occur within `seconds`.
    events must be a list of (ip, timestamp) tuples, sorted by timestamp."""
    bursts = []
    left = 0

    for right in range(len(events)):
        while events[right][1] - events[left][1] > seconds:
            left += 1

        window_size = right - left + 1
        if window_size > threshold:
            bursts.append((events[left][1], events[right][1], window_size))

    return bursts


def correlate_feeds(log_a: list, log_b: list, within_seconds: int = 2) -> list:
    matches = []
    i, j = 0, 0

    while i < len(log_a) and j < len(log_b):
        time_a = log_a[i][1]
        time_b = log_b[j][1]
        gap = abs(time_a - time_b)

        if gap <= within_seconds:
            matches.append((log_a[i], log_b[j]))
            i += 1
            j += 1
        elif time_a < time_b:
            i += 1
        else:
            j += 1

    return matches


class SegmentTree:
    def __init__(self, data: list):
        self.n = len(data)
        self.tree = [float("-inf")] * (4 * self.n)
        self.data = data
        self._build(1, 0, self.n - 1)

    def _build(self, node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = self.data[start]
            return

        mid = (start + end) // 2
        self._build(2 * node, start, mid)
        self._build(2 * node + 1, mid + 1, end)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def query_max(self, lo: int, r: int) -> float:
        return self._query(1, 0, self.n - 1, lo, r)

    def _query(self, node: int, start: int, end: int, lo: int, r: int) -> float:
        if r < start or end < lo:
            return float("-inf")

        if lo <= start and end <= r:
            return self.tree[node]

        mid = (start + end) // 2
        left_max = self._query(2 * node, start, mid, lo, r)
        right_max = self._query(2 * node + 1, mid + 1, end, lo, r)
        return max(left_max, right_max)
