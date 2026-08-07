def naive_search(text: str, pattern: str) -> list:
    """Return every starting index where pattern occurs in text."""
    matches = []
    n, m = len(text), len(pattern)

    for i in range(n - m + 1):
        if text[i : i + m] == pattern:
            matches.append(i)

    return matches


def build_failure_table(pattern: str) -> list:
    """Return, for each position, how much of a prior match to reuse."""
    m = len(pattern)
    table = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            table[i] = length
            i += 1
        elif length > 0:
            length = table[length - 1]
        else:
            table[i] = 0
            i += 1

    return table


def kmp_search(text: str, pattern: str) -> list:
    """Return every starting index where pattern occurs, without
    ever re-examining a character in text."""
    if not pattern:
        return []

    table = build_failure_table(pattern)
    matches: list = []
    i = j = 0
    n, m = len(text), len(pattern)

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == m:
                matches.append(i - j)
                j = table[j - 1]
        elif j > 0:
            j = table[j - 1]
        else:
            i += 1

    return matches
