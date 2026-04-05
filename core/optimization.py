# DP: 0/1 Knapsack (Unit III)
def knapsack_dp(budget, items):
    n = len(items)
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(budget + 1):
            if items[i-1]['price'] <= w:
                dp[i][w] = max(items[i-1]['calories'] + dp[i-1][w-items[i-1]['price']], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    
    # Backtracking for items
    res, w, chosen = dp[n][budget], budget, []
    for i in range(n, 0, -1):
        if res <= 0: break
        if res != dp[i-1][w]:
            chosen.append(items[i-1])
            res -= items[i-1]['calories']
            w -= items[i-1]['price']
    return dp[n][budget], chosen

# Greedy: Fractional Knapsack (Unit II)
def knapsack_greedy(budget, items):
    sorted_items = sorted(items, key=lambda x: x['calories']/x['price'], reverse=True)
    total_val, remaining = 0, budget
    for itm in sorted_items:
        if itm['price'] <= remaining:
            remaining -= itm['price']
            total_val += itm['calories']
    return total_val

# NEW: Binomial Coefficient (Unit III - DP)
def binomial_coeff(n, k):
    C = [[0 for x in range(k + 1)] for x in range(n + 1)]
    for i in range(n + 1):
        for j in range(min(i, k) + 1):
            if j == 0 or j == i: C[i][j] = 1
            else: C[i][j] = C[i-1][j-1] + C[i-1][j]
    return C[n][k]