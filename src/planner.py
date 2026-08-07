def cumulative_risk_naive(n: int) -> int:
    if n <= 1:
        return n

    return cumulative_risk_naive(n - 1) + cumulative_risk_naive(n - 2)


def cumulative_risk_memo(n: int, cache: dict | None = None) -> int:
    if cache is None:
        cache = {}

    if n <= 1:
        return n

    if n in cache:
        return cache[n]

    result = cumulative_risk_memo(n - 1, cache) + cumulative_risk_memo(n - 2, cache)
    cache[n] = result
    return result
