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


def prioritize(threats: list, budget: int) -> tuple:
    n = len(threats)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, risk, efforts = threats[i - 1]

        for w in range(budget + 1):
            if efforts > w:
                dp[i][w] = dp[i - 1][w]
            else:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - efforts] + risk)

    chosen = []
    w = budget

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            name, risk, effort = threats[i - 1]
            chosen.append(name)
            w -= effort

    chosen.reverse()
    return dp[n][budget], chosen


def greedy_plan(threats: list, budget: int) -> tuple:
    ordered = sorted(threats, key=lambda t: t[1], reverse=True)

    chosen = []
    total = 0
    remaining = budget

    for name, risk, effort in ordered:
        if effort <= remaining:
            chosen.append(name)
            total += risk
            remaining -= effort

    return total, chosen
