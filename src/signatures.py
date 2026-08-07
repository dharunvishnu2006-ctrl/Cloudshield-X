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
