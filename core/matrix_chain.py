# core/matrix_chain.py

def solve_recursive(p, i, j):
    """
    Solves the Matrix Chain Multiplication (MCM) problem recursively.
    Finds the minimum number of scalar multiplications needed to multiply the chain.
    Call with i=1, j=len(p)-1.
    """
    if i == j:
        return 0
        
    min_cost = float('inf')
    
    for k in range(i, j):
        cost = (solve_recursive(p, i, k) + 
                solve_recursive(p, k + 1, j) + 
                p[i-1] * p[k] * p[j])
        if cost < min_cost:
            min_cost = cost
            
    return min_cost

def solve_tabular(p):
    """
    Solves the Matrix Chain Multiplication problem iteratively using 2D DP.
    Returns a dictionary: {"length": int, "table": 2D_list, "path": str}
    """
    if not p or len(p) < 2:
        return {"length": 0, "table": [[0]], "path": ""}

    n = len(p) - 1
    # Create a DP table of size (n+1) x (n+1)
    dp = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    
    # dp[i][i] is 0 (already initialized)
    
    # L is chain length
    for L in range(2, n + 1):
        for i in range(1, n - L + 2):
            j = i + L - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + p[i-1] * p[k] * p[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    
    length = dp[1][n]
    if length == float('inf'):
        length = 0
    path = get_path(dp, p)
    
    # Replace float('inf') with 999999 for UI visualization compat
    for r in range(len(dp)):
        for c in range(len(dp[0])):
            if dp[r][c] == float('inf'):
                dp[r][c] = 999999
                
    return {"length": int(length), "table": dp, "path": path}

def solve_space_optimized(p):
    """
    Space-optimized version of Matrix Chain Multiplication.
    Note: Standard MCM requires O(n^2) space as it is an interval DP.
    This returns the tabular result and table for compatibility.
    """
    res = solve_tabular(p)
    return res["length"], res["table"]

def get_path(dp_table, p):
    """
    Reconstructs the optimal parenthesization string from the 2D DP table.
    """
    n = len(p) - 1
    if n <= 0:
        return ""
    
    def reconstruct(i, j):
        if i == j:
            # Using 1-indexed naming (A1, A2, ...) to match standard mathematical notation
            return f"A{i}"
        
        for k in range(i, j):
            cost = dp_table[i][k] + dp_table[k+1][j] + p[i-1] * p[k] * p[j]
            if dp_table[i][j] == cost:
                return f"({reconstruct(i, k)} x {reconstruct(k+1, j)})"
        return f"A{i}"  # Fallback
        
    return reconstruct(1, n)