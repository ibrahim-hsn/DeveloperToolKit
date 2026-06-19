<div align="center">

# ⚡ DP Optimization Engine

### Dynamic Programming Visualization & Benchmarking Toolkit

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-GUI-blueviolet?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Plotting-orange?style=for-the-badge&logo=python)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![AI Assisted](https://img.shields.io/badge/Built%20with-AI%20Assistance-ff69b4?style=for-the-badge&logo=google&logoColor=white)](#-ai-assisted-development)

*An interactive desktop application for visualizing, analyzing, and benchmarking classic Dynamic Programming algorithms — built with a modern dark-mode UI and real-time performance profiling.*

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Supported Algorithms](#-supported-algorithms)
- [Complexity Reference](#-complexity-reference)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [AI-Assisted Development](#-ai-assisted-development)
- [Roadmap](#-roadmap)

---

## 🔍 Overview

The **DP Optimization Engine** is a Python desktop application that bridges the gap between theoretical algorithm knowledge and practical implementation understanding. It provides:

- **Step-by-step visual animation** of how dynamic programming tables are built bottom-up.
- **Traceback path highlighting** to show which choices were made to reach the optimal solution.
- **Live performance benchmarking** that plots recursive vs. tabular execution times, making the exponential-to-polynomial performance leap visually tangible.

> **Target Audience**: Computer science students, algorithms instructors, and developers exploring optimization techniques and performance tradeoffs.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎬 **Interactive Playback** | Play, Pause, Step-by-Step navigation with a configurable speed slider (0.1s – 2.0s per step) |
| 🌡️ **Dynamic Heatmap** | Table cells color-code dynamically by value magnitude using a dark-to-blue gradient |
| 🔗 **Traceback Visualization** | Optimal reconstruction path highlighted in bold green after animation completes |
| 📊 **Performance Benchmarking** | Real-time line graphs comparing recursive O(2^N) vs. tabular polynomial runtimes |
| 🔒 **FSM State Guards** | Input fields and controls are locked during computation to prevent race conditions |
| 🖥️ **Dual-Axis Scrolling** | Custom scrollable grid supporting both horizontal and vertical navigation for large tables |
| 🌙 **Dark Mode UI** | Catppuccin Mocha-inspired premium theme throughout the entire application |

---

## 📸 Screenshots

> *The application features a split-panel layout: a control sidebar on the left and an interactive visualization workspace on the right.*

<img width="1277" height="857" alt="image" src="https://github.com/user-attachments/assets/9e667143-a4c4-413e-b0a1-f293aadbf8a6" />

```

---

## 🧮 Supported Algorithms

The toolkit implements **four classical DP algorithms**, each with three solver variants:
- **Recursive** — pure exponential solution (no caching)
- **Tabular 2D** — iterative bottom-up with full DP table
- **Space-Optimized** — reduced memory footprint using 1D arrays

---

### 1. 0/1 Knapsack

> Maximize total value of selected items subject to a weight capacity constraint.

**Input Format**: `Weights & Capacity` (e.g. `1, 2, 3 | 5`) and `Values` (e.g. `6, 10, 12`)

**Recurrence**:
```
dp[i][j] = max(dp[i-1][j], v[i-1] + dp[i-1][j - w[i-1]])   if w[i-1] <= j
dp[i][j] = dp[i-1][j]                                        otherwise
```

---

### 2. Longest Common Subsequence (LCS)

> Find the longest sequence of characters present in both input strings in the same relative order.

**Input Format**: `String X` (e.g. `ABCBDAB`) and `String Y` (e.g. `BDCABA`)

**Recurrence**:
```
dp[i][j] = dp[i-1][j-1] + 1          if X[i-1] == Y[j-1]
dp[i][j] = max(dp[i-1][j], dp[i][j-1])  otherwise
```

---

### 3. Coin Change (Min Coins)

> Find the minimum number of coins needed to make a target amount using an unlimited supply of given denominations.

**Input Format**: `Coin Denominations` (e.g. `1, 2, 5`) and `Target Amount` (e.g. `11`)

**Recurrence**:
```
dp[i][j] = min(dp[i-1][j], 1 + dp[i][j - c[i-1]])   if c[i-1] <= j
dp[i][j] = dp[i-1][j]                                 otherwise
```

---

### 4. Matrix Chain Multiplication (MCM)

> Find the most efficient parenthesization to multiply a chain of matrices with the fewest scalar multiplications.

**Input Format**: `Matrix Dimensions` (e.g. `40, 20, 30, 10, 30`)

**Recurrence**:
```
dp[i][j] = min over k in [i, j): dp[i][k] + dp[k+1][j] + p[i-1] * p[k] * p[j]
```

---

## 📈 Complexity Reference

| Algorithm | Tabular Time | Recursive Time | Tabular Space | Space-Optimized |
|---|---|---|---|---|
| **0/1 Knapsack** | `O(N · W)` | `O(2^N)` | `O(N · W)` | `O(W)` |
| **Longest Common Subsequence** | `O(M · N)` | `O(2^min(M,N))` | `O(M · N)` | `O(N)` |
| **Coin Change** | `O(N · A)` | `O(2^height)` | `O(N · A)` | `O(A)` |
| **Matrix Chain Multiplication** | `O(N³)` | `O(2^N)` | `O(N²)` | `O(N²)` |

---

## 📁 Project Structure

```
DeveloperToolKit/
│
├── main.py                          # Startup orchestrator and CLI test-suite
├── README.md                        # This file
├── PROJECT_CONTEXT.md               # AI-readable full project context document
├── ALGORITHMS_AND_VISUALIZATION.md  # In-depth algorithm theory and visualization guide
├── TECHNICAL_README.md              # Frontend/backend design pattern reference
├── requirements.txt                 # Python package dependencies
│
├── core/                            # DP algorithm backend modules (no GUI dependencies)
│   ├── coinchange.py                # Coin Change — 3 solvers + path tracker
│   ├── knapsack.py                  # 0/1 Knapsack — 3 solvers + path tracker
│   ├── lcs.py                       # LCS — 3 solvers + path tracker
│   └── matrix_chain.py              # MCM — 3 solvers + path tracker
│
├── utils/                           # Tooling and analysis helpers
│   ├── benchmarker.py               # Timing profiler for recursive vs. tabular solvers
│   └── data_gen.py                  # (Reserved) Dataset generation utilities
│
└── GUI/                             # User interface layer
    ├── app_window.py                # Main CTk application — controller, animator, plotter
    └── visualizer.py                # Standalone canvas-based table renderer with arrows
```

### Backend API Contract

All tabular solvers in `core/` return a **standardized dictionary**:

```python
{
    "length": int,      # Optimal objective value (max value, LCS length, min coins, etc.)
    "table":  2D_list,  # Full DP computation matrix
    "path":   str       # Human-readable optimal solution description
}
```

---

## ⚙️ Installation

### Prerequisites

- Python **3.10** or higher
- pip package manager

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/DeveloperToolKit.git
cd DeveloperToolKit

# 2. (Recommended) Create a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the application
python main.py
```

### Dependencies

| Package | Purpose |
|---|---|
| `customtkinter` | Modern dark-mode GUI widgets |
| `matplotlib` | Performance benchmarking plots |
| `tkinter` | Bundled with Python — canvas layout engine |

---

## 🚀 Usage

### GUI Mode (Default)

```bash
python main.py
```

1. **Select an algorithm** from the dropdown menu in the left sidebar.
2. **Enter your inputs** in the fields (or leave them blank to use built-in defaults).
3. **Click "Run Analysis"** — the DP table will begin animating cell-by-cell.
4. Use **Play / Pause / Step** to control the animation pace.
5. Adjust the **Speed Slider** (0.1s – 2.0s per step) for faster or slower playback.
6. After animation completes:
   - The **optimal path** is highlighted in green on the table.
   - The **solution string** appears in the reconstruction panel.
   - A **performance chart** plots recursive vs. tabular runtimes.

### CLI Mode (Console Tests)

```bash
python main.py --cli
```

Runs all four algorithm solvers with sample inputs and prints results to the terminal.

### Input Format Reference

| Algorithm | Input 1 | Input 2 |
|---|---|---|
| **0/1 Knapsack** | `weights \| capacity` e.g. `1, 2, 3 \| 5` | `values` e.g. `6, 10, 12` |
| **LCS** | String X e.g. `ABCBDAB` | String Y e.g. `BDCABA` |
| **Coin Change** | Denominations e.g. `1, 2, 5` | Target amount e.g. `11` |
| **MCM** | Dimensions e.g. `40, 20, 30, 10, 30` | *(not used)* |

---

## 🏗️ Architecture

### Application Flow

```
User Input
    │
    ▼
run_analysis()          ← Input validation & parsing
    │
    ▼
core/solver.solve_tabular()   ← Pure DP computation (no GUI dependency)
    │
    ▼
animate_grid()          ← CTkLabel grid creation with base case rendering
    │
    ▼
animate_loop()          ← Non-blocking step-by-step cell animation (self.after)
    │
    ▼
on_animation_complete() ← Path traceback highlight + benchmarker call
    │
    ▼
benchmarker.benchmark_algorithm() ← Recursive vs. Tabular timing across N=4..16
    │
    ▼
Matplotlib canvas redrawn ← Final performance graph displayed
```

### Key Design Decisions

- **Decoupled Backends**: All `core/` modules are pure Python with zero GUI dependency. They communicate with the frontend through a standardized dictionary contract.
- **Main-Thread Scheduling**: Animations use `self.after(delay_ms, callback)` — Tkinter's safe scheduling mechanism — to avoid multi-threading pitfalls while keeping the UI responsive.
- **Dual-Axis Scroll Grid**: A custom solution using a `tkinter.Canvas` embedding a `CTkFrame` grid viewport overcomes CustomTkinter's native single-axis scroll limitation.
- **Safety-Capped Benchmarks**: Recursive solvers are capped at `N ≤ 15` (or `N ≤ 12` for MCM) to prevent the UI thread from hanging on exponential growth.

---

## 🤖 AI-Assisted Development

> This project was developed with the assistance of **AI coding tools**, specifically leveraging large language model capabilities for:
>
> - **Architecture design** — structuring the decoupled backend/frontend pattern and defining the standardized solver API contract.
> - **Algorithm implementation** — generating and verifying the three solver variants (Recursive, Tabular, Space-Optimized) and their traceback logic for each algorithm.
> - **GUI construction** — building the CustomTkinter layout, dual-axis scrolling widget, and Catppuccin Mocha theme system.
> - **Animation engine** — designing the non-blocking cell-by-cell step loop and heatmap interpolation gradient.
> - **Benchmarking framework** — developing the timing profiler with safe recursion limits and Matplotlib chart integration.
> - **Documentation** — generating the `PROJECT_CONTEXT.md`, `TECHNICAL_README.md`, and `ALGORITHMS_AND_VISUALIZATION.md` reference documents.
>
> AI assistance was used as a pair-programming tool throughout development. All generated code was reviewed, tested, and integrated by the project author.

---

## 🗺️ Roadmap

Identified areas for future improvement:

- [ ] **Top-Down Memoized Solvers** — Add recursive + cache variants to the benchmark comparison alongside pure recursive and tabular solvers.
- [ ] **Background Thread Benchmarking** — Move performance profiling off the main UI thread to eliminate potential stuttering on slower hardware.
- [ ] **Data Generation Utilities** — Implement `utils/data_gen.py` with standardized input generation helpers.
- [ ] **Visualizer Integration** — Unify `GUI/visualizer.py` with the main animation engine or deprecate it to keep the codebase clean.
- [ ] **Additional Algorithms** — Extend the toolkit with Longest Increasing Subsequence (LIS), Edit Distance, and Rod Cutting problems.
- [ ] **Export Feature** — Allow users to export the DP table and benchmarking chart as PNG or CSV files.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with ⚡ Python · CustomTkinter · Matplotlib

*Designed for learning. Powered by dynamic programming.*

</div>
