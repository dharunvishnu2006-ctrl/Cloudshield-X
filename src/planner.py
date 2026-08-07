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


def sequence_similarity(seq_a: list, seq_b: list) -> int:
    m, n = len(seq_a), len(seq_b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq_a[i - 1] == seq_b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
