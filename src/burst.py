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
