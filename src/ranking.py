def bubble_sort(items: list) -> list:
    """Sort by repeatedly swapping adjacent out-of-order pairs."""
    arr = items.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(items: list) -> list:
    """Sort by repeatedly finding the minimum and swapping it into place."""
    arr = items.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(items: list) -> list:
    """Sort by sliding each new element backward into its correct position."""
    arr = items.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def _merge(left: list, right: list) -> list:
    """Merge two already-sorted lists into one sorted list."""
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(items: list) -> list:
    """Sort by recursively splitting in half, then merging sorted halves."""
    arr = items.copy()
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def quick_sort(items: list) -> list:
    """Sort by picking a pivot and partitioning around it."""
    arr = items.copy()
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    smaller = [x for x in arr[1:] if x < pivot]
    larger = [x for x in arr[1:] if x >= pivot]
    return quick_sort(smaller) + [pivot] + quick_sort(larger)
