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
