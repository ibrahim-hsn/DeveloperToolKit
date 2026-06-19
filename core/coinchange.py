# core/coinchange.py

def solve_recursive(coins, amount, n):
    """
    Solves the Coin Change problem recursively to find the minimum number of coins.
    """
    # Base case: if amount is 0, 0 coins are needed
    if amount == 0:
        return 0
    # If no coins are left but amount is > 0, return infinity (not possible)
    if n == 0:
        return float('inf')
    
    # If the coin's value is greater than the amount, we cannot include it
    if coins[n-1] > amount:
        return solve_recursive(coins, amount, n - 1)
    
    # We can either include the coin or exclude it
    # Since we can use an unlimited number of each coin, we don't decrement n when including
    include = 1 + solve_recursive(coins, amount - coins[n-1], n)
    exclude = solve_recursive(coins, amount, n - 1)
    
    return min(include, exclude)

def solve_tabular(coins, amount):
    """
    Solves the Coin Change problem iteratively using 2D DP.
    Returns a dictionary: {"length": int, "table": 2D_list, "path": str}
    """
    if not coins or amount <= 0:
        n = len(coins) if coins else 0
        amt = max(0, amount)
        dp = [[0 for _ in range(amt + 1)] for _ in range(n + 1)]
        return {"length": 0, "table": dp, "path": "Coins used: []"}

    n = len(coins)
    # Initialize DP table with infinity
    dp = [[float('inf') for _ in range(amount + 1)] for _ in range(n + 1)]
    
    # Base case: 0 amount requires 0 coins
    for i in range(n + 1):
        dp[i][0] = 0
        
    # Iterative logic
    for i in range(1, n + 1):
        for j in range(1, amount + 1):
            if coins[i-1] <= j:
                dp[i][j] = min(dp[i-1][j], 1 + dp[i][j - coins[i-1]])
            else:
                dp[i][j] = dp[i-1][j]
                
    result = dp[n][amount]
    if result == float('inf'):
        result = -1
        
    path_list = get_path(dp, coins, amount)
    path_str = f"Coins used: {path_list}"
    
    # Replace float('inf') with 99999 for UI visualization compatibility
    for r in range(len(dp)):
        for c in range(len(dp[0])):
            if dp[r][c] == float('inf'):
                dp[r][c] = 99999
                
    return {"length": int(result), "table": dp, "path": path_str}

def solve_space_optimized(coins, amount):
    """
    Solves the Coin Change problem using a space-optimized 1D DP array.
    Returns the minimum number of coins and the 1D DP array.
    """
    dp = [float('inf')] * (amount + 1)
    
    # Base case: 0 amount requires 0 coins
    dp[0] = 0
    
    for coin in coins:
        for j in range(coin, amount + 1):
            if dp[j - coin] != float('inf'):
                dp[j] = min(dp[j], dp[j - coin] + 1)
                
    result = dp[amount] if dp[amount] != float('inf') else -1
    return result, dp

def get_path(dp_table, coins, amount):
    """
    Reconstructs the path to find which coins were used to make up the amount.
    Note: Requires a 2D DP table.
    """
    n = len(coins)
    path = []
    
    # If no solution exists
    if dp_table[n][amount] == float('inf') or dp_table[n][amount] == -1:
        return path
        
    i, j = n, amount
    while j > 0 and i > 0:
        # If the value came from excluding the coin
        if dp_table[i][j] == dp_table[i-1][j]:
            i -= 1
        else:
            # The coin was included
            path.append(coins[i-1])
            j -= coins[i-1]
            # Keep i the same since we can use multiple coins of the same denomination
            
    return path
