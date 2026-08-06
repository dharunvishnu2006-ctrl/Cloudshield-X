def linear_scan(sorted_ips: list, target: str) -> bool:
    """Search for target by checking every item, one at a time."""
    for ip in sorted_ips:
        if ip == target:
            return True
    return False


def binary_search(sorted_ips: list, target: str) -> bool:
    """Search for target in a SORTED list by repeatedly halving the search space."""
    low, high = 0, len(sorted_ips) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_ips[mid] == target:
            return True
        elif sorted_ips[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return False
