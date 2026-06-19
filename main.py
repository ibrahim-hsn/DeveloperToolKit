# main.py
from core import coinchange, knapsack, lcs, matrix_chain

def test_coin_change():
    print("=== COIN CHANGE TESTS ===")
    coins = [1, 2, 5]
    amount = 11
    print(f"Coins: {coins}, Amount: {amount}")
    
    res_rec = coinchange.solve_recursive(coins, amount, len(coins))
    print(f"Recursive Result: {res_rec}")
    
    res_dict = coinchange.solve_tabular(coins, amount)
    print(f"Tabular Result: {res_dict['length']}")
    
    res_space, dp_1d = coinchange.solve_space_optimized(coins, amount)
    print(f"Space Optimized Result: {res_space}")
    
    print(res_dict['path'])
    print("-" * 40)

def test_knapsack():
    print("=== 0/1 KNAPSACK TESTS ===")
    weights = [1, 2, 3]
    values = [6, 10, 12]
    capacity = 5
    n = len(values)
    print(f"Weights: {weights}, Values: {values}, Capacity: {capacity}")
    
    res_rec = knapsack.solve_recursive(weights, values, capacity, n)
    print(f"Recursive Result: {res_rec}")
    
    res_dict = knapsack.solve_tabular(weights, values, capacity)
    print(f"Tabular Result: {res_dict['length']}")
    
    res_space, dp_1d = knapsack.solve_space_optimized(weights, values, capacity)
    print(f"Space Optimized Result: {res_space}")
    
    print(res_dict['path'])
    print("-" * 40)

def test_lcs():
    print("=== LONGEST COMMON SUBSEQUENCE TESTS ===")
    X = "ABCBDAB"
    Y = "BDCABA"
    print(f"X: '{X}', Y: '{Y}'")
    
    res_rec = lcs.solve_recursive(X, Y, len(X), len(Y))
    print(f"Recursive Result: {res_rec}")
    
    res_dict = lcs.solve_tabular(X, Y)
    print(f"Tabular Result: {res_dict['length']}")
    
    res_space, dp_1d = lcs.solve_space_optimized(X, Y)
    print(f"Space Optimized Result: {res_space}")
    
    print(f"LCS: '{res_dict['path']}'")
    print("-" * 40)

def test_matrix_chain():
    print("=== MATRIX CHAIN MULTIPLICATION TESTS ===")
    p = [40, 20, 30, 10, 30]
    print(f"Dimensions: {p}")
    
    res_rec = matrix_chain.solve_recursive(p, 1, len(p) - 1)
    print(f"Recursive Result: {res_rec}")
    
    res_dict = matrix_chain.solve_tabular(p)
    print(f"Tabular Result: {res_dict['length']}")
    
    res_space, dp_1d = matrix_chain.solve_space_optimized(p)
    print(f"Space Optimized Result: {res_space}")
    
    print(f"Optimal Parenthesization: {res_dict['path']}")
    print("-" * 40)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        test_coin_change()
        test_knapsack()
        test_lcs()
        test_matrix_chain()
    else:
        try:
            from GUI.app_window import App
            print("Starting DP Optimization Engine...")
            app = App()
            app.mainloop()
        except Exception as e:
            print(f"Could not launch GUI ({e}). Running console tests instead:\n")
            test_coin_change()
            test_knapsack()
            test_lcs()
            test_matrix_chain()
