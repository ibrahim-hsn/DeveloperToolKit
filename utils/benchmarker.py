# utils/benchmarker.py

import time
import random
from core import coinchange, knapsack, lcs, matrix_chain

def benchmark_algorithm(algo_name, sizes=[4, 6, 8, 10, 12, 14, 16]):
    """
    Benchmarks recursive vs tabular DP execution times for a given algorithm.
    Returns: (sizes, recursive_times, dp_times)
    All times in milliseconds.
    """
    recursive_times = []
    dp_times = []
    
    for size in sizes:
        if algo_name == "0/1 Knapsack":
            # Generate weights and values
            weights = [random.randint(1, 5) for _ in range(size)]
            values = [random.randint(10, 50) for _ in range(size)]
            capacity = size * 3
            
            # Recursive (limit size to keep it fast)
            if size <= 15:
                t0 = time.perf_counter()
                knapsack.solve_recursive(weights, values, capacity, size)
                t_rec = (time.perf_counter() - t0) * 1000.0
            else:
                t_rec = None
                
            # Tabular
            t0 = time.perf_counter()
            knapsack.solve_tabular(weights, values, capacity)
            t_dp = (time.perf_counter() - t0) * 1000.0
            
        elif algo_name == "Longest Common Subsequence":
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            X = "".join(random.choice(chars) for _ in range(size))
            Y = "".join(random.choice(chars) for _ in range(size))
            
            # Recursive
            if size <= 15:
                t0 = time.perf_counter()
                lcs.solve_recursive(X, Y, size, size)
                t_rec = (time.perf_counter() - t0) * 1000.0
            else:
                t_rec = None
                
            # Tabular
            t0 = time.perf_counter()
            lcs.solve_tabular(X, Y)
            t_dp = (time.perf_counter() - t0) * 1000.0
            
        elif algo_name == "Coin Change":
            coins = [1, 2, 5, 10]
            amount = size * 3
            
            # Recursive
            if size <= 15:
                t0 = time.perf_counter()
                coinchange.solve_recursive(coins, amount, len(coins))
                t_rec = (time.perf_counter() - t0) * 1000.0
            else:
                t_rec = None
                
            # Tabular
            t0 = time.perf_counter()
            coinchange.solve_tabular(coins, amount)
            t_dp = (time.perf_counter() - t0) * 1000.0
            
        elif algo_name == "Matrix Chain Multiplication":
            p = [random.randint(5, 50) for _ in range(size + 1)]
            
            # Recursive
            if size <= 12:
                t0 = time.perf_counter()
                matrix_chain.solve_recursive(p, 1, size)
                t_rec = (time.perf_counter() - t0) * 1000.0
            else:
                t_rec = None
                
            # Tabular
            t0 = time.perf_counter()
            matrix_chain.solve_tabular(p)
            t_dp = (time.perf_counter() - t0) * 1000.0
            
        else:
            t_rec, t_dp = None, None
            
        recursive_times.append(t_rec)
        dp_times.append(t_dp)
        
    return sizes, recursive_times, dp_times
