def naive_search(text: str, pattern: str) -> list:
    """Return every starting index where pattern occurs in text."""
    matches = []
    n, m = len(text), len(pattern)

    for i in range(n - m + 1):
        if text[i : i + m] == pattern:
            matches.append(i)

    return matches
