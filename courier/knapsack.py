"""Phase 2 - box filling with 0/1 knapsack dynamic programming.

State   : dp[i][w] = best total priority using the first i parcels with
          capacity w kg.
Recurrence:
    dp[i][w] = dp[i-1][w]                                   if wt_i > w
    dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt_i] + val_i)     otherwise
Time O(n*W), space O(n*W) (full table kept so the chosen set can be traced back).
"""


def knapsack_dp(parcels, capacity):
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, val = parcels[i - 1].weight, parcels[i - 1].priority
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if wt <= w and dp[i - 1][w - wt] + val > dp[i][w]:
                dp[i][w] = dp[i - 1][w - wt] + val

    # back-track to recover which parcels were chosen
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(parcels[i - 1])
            w -= parcels[i - 1].weight
    chosen.reverse()
    return dp[n][capacity], chosen, dp


def format_dp_table(parcels, dp, max_cols=None):
    """Pretty-print the DP table (used as evidence in the report)."""
    cols = len(dp[0]) if max_cols is None else min(max_cols, len(dp[0]))
    head = "item\\cap " + " ".join(f"{w:>3}" for w in range(cols))
    lines = [head]
    for i, row in enumerate(dp):
        label = "none" if i == 0 else parcels[i - 1].id
        lines.append(f"{label:<8} " + " ".join(f"{v:>3}" for v in row[:cols]))
    return "\n".join(lines)
