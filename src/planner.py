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


def max_risk_non_adjacent(risks: list) -> int:
    if not risks:
        return 0
    if len(risks) == 1:
        return risks[0]

    dp = [0] * len(risks)
    dp[0] = risks[0]
    dp[1] = max(risks[0], risks[1])

    for i in range(2, len(risks)):
        dp[i] = max(dp[i - 1], dp[i - 2] + risks[i])

    return dp[-1]
