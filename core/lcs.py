# core/lcs.py

def solve_recursive(X, Y, m, n):
    """
    Solves the Longest Common Subsequence (LCS) problem recursively.
    """
    if m == 0 or n == 0:
        return 0
    
    if X[m-1] == Y[n-1]:
        return 1 + solve_recursive(X, Y, m-1, n-1)
    else:
        return max(solve_recursive(X, Y, m, n-1), solve_recursive(X, Y, m-1, n))

def solve_tabular(X, Y):
    """
    Solves the LCS problem iteratively using 2D DP.
    Returns a dictionary: {"length": int, "table": 2D_list, "path": str}
    """
    if not X or not Y:
        m = len(X) if X else 0
        n = len(Y) if Y else 0
        return {"length": 0, "table": [[0 for _ in range(n + 1)] for _ in range(m + 1)], "path": ""}

    m, n = len(X), len(Y)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                
    length = dp[m][n]
    path = get_path(dp, X, Y)
    return {"length": int(length), "table": dp, "path": path}

def solve_space_optimized(X, Y):
    """
    Solves the LCS problem using space-optimized DP (two rows).
    Returns the length of LCS and the final DP row.
    """
    m, n = len(X), len(Y)
    # We maintain previous and current rows for space optimization
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        # Move current row to previous row
        prev = list(curr)
        
    return prev[n], prev

def get_path(dp_table, X, Y):
    """
    Reconstructs the LCS string from the 2D DP table.
    """
    m, n = len(X), len(Y)
    lcs_chars = []
    
    i, j = m, n
    while i > 0 and j > 0:
        # If characters match, they are part of LCS
        if X[i-1] == Y[j-1]:
            lcs_chars.append(X[i-1])
            i -= 1
            j -= 1
        # Else, go in the direction of the larger value
        elif dp_table[i-1][j] >= dp_table[i][j-1]:
            i -= 1
        else:
            j -= 1
            
    # Reconstructed backwards, so reverse it
    lcs_chars.reverse()
    return "".join(lcs_chars)
