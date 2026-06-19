# core/knapsack.py

def solve_recursive(weights, values, capacity, n):
    """
    Solves the 0/1 Knapsack problem recursively.
    """
    # Base Case: No items left or capacity is 0
    if n == 0 or capacity == 0:
        return 0

    # If weight of the nth item is more than Knapsack capacity,
    # then this item cannot be included in the optimal solution
    if weights[n-1] > capacity:
        return solve_recursive(weights, values, capacity, n-1)

    # Return the maximum of two cases:
    # (1) nth item included
    # (2) not included
    else:
        return max(
            values[n-1] + solve_recursive(weights, values, capacity - weights[n-1], n-1),
            solve_recursive(weights, values, capacity, n-1)
        )

def solve_tabular(weights, values, capacity):
    """
    Solves the 0/1 Knapsack problem iteratively using 2D DP.
    Returns a dictionary: {"length": int, "table": 2D_list, "path": str}
    """
    if not weights or not values or capacity <= 0 or len(weights) != len(values):
        # Return empty state matching the capacity
        cap = max(0, capacity)
        return {"length": 0, "table": [[0 for _ in range(cap + 1)]], "path": "Item indices chosen: []"}

    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w - weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    length = dp[n][capacity]
    path_indices = get_path(dp, weights, values, capacity)
    path_str = f"Item indices chosen: {path_indices}"

    return {"length": int(length), "table": dp, "path": path_str}

def solve_space_optimized(weights, values, capacity):
    """
    Solves the 0/1 Knapsack problem using a space-optimized 1D DP array.
    Returns the maximum value and the 1D DP array.
    """
    dp = [0] * (capacity + 1)

    for i in range(len(values)):
        # Traverse capacity from right to left to avoid using the same item multiple times
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity], dp

def get_path(dp_table, weights, values, capacity):
    """
    Reconstructs the path to find which items (by index) were included in the knapsack.
    Note: Requires a 2D DP table.
    """
    n = len(values)
    path = []
    w = capacity
    
    for i in range(n, 0, -1):
        # If the value came from including the item, the value must be different from the cell above
        if dp_table[i][w] != dp_table[i-1][w]:
            path.append(i-1)  # 0-based index of the item
            w -= weights[i-1]
            
    # Return path reversed to show items in order of original list
    path.reverse()
    return path