# GUI/app_window.py

import tkinter
import customtkinter
import sys
import os
import matplotlib
matplotlib.use("TkAgg")  # Ensure correct backend for embedding in Tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Import core modules
from core import coinchange, knapsack, lcs, matrix_chain
# Import benchmarker
from utils import benchmarker

# Set dark appearance mode and modern color theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# ─── Premium Color Palette (Catppuccin Mocha Extended) ──────────────────────
_PALETTE = {
    "bg_base":        "#0f0f1a",   # Deep midnight – window background
    "bg_surface":     "#161625",   # Sidebar / panel background
    "bg_card":        "#1c1c30",   # Card surface
    "bg_elevated":    "#22223a",   # Elevated panels / inputs
    "bg_input":       "#12121f",   # Text-entry background
    "border_subtle":  "#2a2a44",   # Subtle borders
    "border_accent":  "#3d3d66",   # Accent border for monitor frame
    "text_primary":   "#e2e8f0",   # Primary text (near-white)
    "text_secondary": "#94a3b8",   # Secondary labels
    "text_muted":     "#64748b",   # Muted / hint text
    "accent_blue":    "#7c93f5",   # Primary accent (soft indigo-blue)
    "accent_cyan":    "#67e8f9",   # Teal / cyan highlight
    "accent_green":   "#6ee7b7",   # Success / path green
    "accent_pink":    "#f472b6",   # Error / infinity pink
    "accent_amber":   "#fbbf24",   # Warning / attention amber
    "accent_purple":  "#a78bfa",   # Secondary accent (lavender)
    "heatmap_low":    "#1a1a2e",   # Heatmap cold end
    "heatmap_high":   "#7c93f5",   # Heatmap hot end
}

_P = _PALETTE  # shorthand


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.title("⚡ DP Optimization Engine — Dynamic Programming Visualizer")
        self.geometry("1280x860")
        self.minsize(1000, 700)
        self.configure(fg_color=_P["bg_base"])

        # ─── Fonts ──────────────────────────────────────────────────────
        self._font_brand      = customtkinter.CTkFont(family="Segoe UI", size=22, weight="bold")
        self._font_section    = customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold")
        self._font_label      = customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold")
        self._font_body       = customtkinter.CTkFont(family="Segoe UI", size=12)
        self._font_small      = customtkinter.CTkFont(family="Segoe UI", size=11)
        self._font_cell       = customtkinter.CTkFont(family="Consolas", size=11)
        self._font_cell_bold  = customtkinter.CTkFont(family="Consolas", size=11, weight="bold")
        self._font_status     = customtkinter.CTkFont(family="Segoe UI", size=11, weight="bold")
        self._font_btn        = customtkinter.CTkFont(family="Segoe UI", size=13, weight="bold")
        self._font_btn_sm     = customtkinter.CTkFont(family="Segoe UI", size=12, weight="bold")
        self._font_path       = customtkinter.CTkFont(family="Consolas", size=13, weight="bold")

        # ─── Root Grid ──────────────────────────────────────────────────
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=310)   # Sidebar
        self.grid_columnconfigure(1, weight=1)                 # Main content

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #  LEFT SIDEBAR
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        self.sidebar = customtkinter.CTkFrame(
            self, width=310, fg_color=_P["bg_surface"], corner_radius=0,
            border_width=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_propagate(False)

        # ── Brand Bar ───────────────────────────────────────────────────
        self.brand_frame = customtkinter.CTkFrame(
            self.sidebar, fg_color=_P["bg_card"], corner_radius=0, height=80
        )
        self.brand_frame.grid(row=0, column=0, sticky="ew")
        self.brand_frame.grid_propagate(False)
        self.brand_frame.grid_columnconfigure(0, weight=1)
        self.brand_frame.grid_rowconfigure(0, weight=1)

        self.brand_inner = customtkinter.CTkFrame(self.brand_frame, fg_color="transparent")
        self.brand_inner.grid(row=0, column=0, sticky="w", padx=24)

        self.brand_icon = customtkinter.CTkLabel(
            self.brand_inner, text="⚡", font=customtkinter.CTkFont(size=26),
            text_color=_P["accent_cyan"]
        )
        self.brand_icon.pack(side="left", padx=(0, 10))

        self.brand_text_frame = customtkinter.CTkFrame(self.brand_inner, fg_color="transparent")
        self.brand_text_frame.pack(side="left")

        self.title_lbl = customtkinter.CTkLabel(
            self.brand_text_frame, text="DP Engine",
            font=self._font_brand, text_color=_P["text_primary"]
        )
        self.title_lbl.pack(anchor="w")

        self.subtitle_lbl = customtkinter.CTkLabel(
            self.brand_text_frame, text="Dynamic Programming Visualizer",
            font=self._font_small, text_color=_P["text_muted"]
        )
        self.subtitle_lbl.pack(anchor="w")

        # ── Divider ────────────────────────────────────────────────────
        self._sidebar_divider(row=1)

        # ── Section 1: Algorithm Selection ─────────────────────────────
        self.section1_frame = customtkinter.CTkFrame(
            self.sidebar, fg_color="transparent"
        )
        self.section1_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(18, 0))
        self.section1_frame.grid_columnconfigure(0, weight=1)

        self.section1_label = customtkinter.CTkLabel(
            self.section1_frame, text="🧬  ALGORITHM",
            font=self._font_section, text_color=_P["accent_purple"],
            anchor="w"
        )
        self.section1_label.grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.algo_menu = customtkinter.CTkOptionMenu(
            self.section1_frame,
            values=["0/1 Knapsack", "Longest Common Subsequence", "Coin Change", "Matrix Chain Multiplication"],
            command=self.on_algo_change,
            fg_color=_P["bg_elevated"],
            button_color=_P["bg_elevated"],
            button_hover_color=_P["border_accent"],
            dropdown_fg_color=_P["bg_card"],
            dropdown_hover_color=_P["border_accent"],
            dropdown_text_color=_P["text_primary"],
            text_color=_P["text_primary"],
            font=self._font_body,
            corner_radius=8,
            height=38
        )
        self.algo_menu.grid(row=1, column=0, sticky="ew")

        # ── Section 2: Data Generation ─────────────────────────────────
        self._sidebar_divider(row=3)

        self.section2_frame = customtkinter.CTkFrame(
            self.sidebar, fg_color="transparent"
        )
        self.section2_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(14, 0))
        self.section2_frame.grid_columnconfigure(0, weight=1)

        self.section2_label = customtkinter.CTkLabel(
            self.section2_frame, text="📊  DATA GENERATION",
            font=self._font_section, text_color=_P["accent_purple"],
            anchor="w"
        )
        self.section2_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Input 1
        self.input1_lbl = customtkinter.CTkLabel(
            self.section2_frame, text="Input 1:",
            font=self._font_label, text_color=_P["text_secondary"]
        )
        self.input1_lbl.grid(row=1, column=0, sticky="w", pady=(0, 4))

        self.input1_entry = customtkinter.CTkEntry(
            self.section2_frame, placeholder_text="",
            fg_color=_P["bg_input"], border_color=_P["border_subtle"],
            text_color=_P["text_primary"], font=self._font_body,
            corner_radius=8, height=36, border_width=1
        )
        self.input1_entry.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        # Input 2
        self.input2_lbl = customtkinter.CTkLabel(
            self.section2_frame, text="Input 2:",
            font=self._font_label, text_color=_P["text_secondary"]
        )
        self.input2_lbl.grid(row=3, column=0, sticky="w", pady=(0, 4))

        self.input2_entry = customtkinter.CTkEntry(
            self.section2_frame, placeholder_text="",
            fg_color=_P["bg_input"], border_color=_P["border_subtle"],
            text_color=_P["text_primary"], font=self._font_body,
            corner_radius=8, height=36, border_width=1
        )
        self.input2_entry.grid(row=4, column=0, sticky="ew", pady=(0, 16))

        # Run Button
        self.run_btn = customtkinter.CTkButton(
            self.section2_frame, text="▶  Run Analysis",
            command=self.run_algorithm,
            fg_color=_P["accent_blue"], hover_color=_P["accent_purple"],
            text_color="#ffffff", font=self._font_btn,
            corner_radius=10, height=44, border_width=0
        )
        self.run_btn.grid(row=5, column=0, sticky="ew", pady=(0, 6))

        # ── Section 3: Playback & Speed ────────────────────────────────
        self._sidebar_divider(row=5)

        self.section3_frame = customtkinter.CTkFrame(
            self.sidebar, fg_color="transparent"
        )
        self.section3_frame.grid(row=6, column=0, sticky="ew", padx=20, pady=(14, 0))
        self.section3_frame.grid_columnconfigure(0, weight=1)
        self.section3_frame.grid_columnconfigure(1, weight=1)

        self.section3_label = customtkinter.CTkLabel(
            self.section3_frame, text="🎮  PLAYBACK",
            font=self._font_section, text_color=_P["accent_purple"],
            anchor="w"
        )
        self.section3_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        self.play_pause_btn = customtkinter.CTkButton(
            self.section3_frame, text="▶  Play",
            command=self.toggle_play_pause,
            fg_color=_P["accent_green"], hover_color=_P["accent_cyan"],
            text_color="#0f0f1a", font=self._font_btn_sm,
            corner_radius=8, height=38, width=120
        )
        self.play_pause_btn.grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=(0, 10))

        self.next_btn = customtkinter.CTkButton(
            self.section3_frame, text="⏭  Step",
            command=self.next_step,
            fg_color=_P["bg_elevated"], hover_color=_P["border_accent"],
            text_color=_P["text_primary"], font=self._font_btn_sm,
            corner_radius=8, height=38, width=120
        )
        self.next_btn.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(0, 10))

        # Speed control row
        self.speed_row = customtkinter.CTkFrame(self.section3_frame, fg_color="transparent")
        self.speed_row.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 6))
        self.speed_row.grid_columnconfigure(1, weight=1)

        self.speed_lbl = customtkinter.CTkLabel(
            self.speed_row, text="Speed: 0.5s",
            font=self._font_small, text_color=_P["text_muted"]
        )
        self.speed_lbl.grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.speed_slider = customtkinter.CTkSlider(
            self.speed_row,
            from_=0.1, to=2.0, number_of_steps=19,
            command=self.on_speed_change,
            fg_color=_P["bg_elevated"],
            progress_color=_P["accent_blue"],
            button_color=_P["accent_blue"],
            button_hover_color=_P["accent_purple"],
            height=16
        )
        self.speed_slider.set(0.5)
        self.speed_slider.grid(row=0, column=1, sticky="ew")

        # Status indicator
        self.status_frame = customtkinter.CTkFrame(
            self.section3_frame, fg_color=_P["bg_card"], corner_radius=8, height=36
        )
        self.status_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self.status_frame.grid_propagate(False)
        self.status_frame.grid_columnconfigure(1, weight=1)

        self.status_dot = customtkinter.CTkLabel(
            self.status_frame, text="●", font=customtkinter.CTkFont(size=10),
            text_color=_P["text_muted"], width=20
        )
        self.status_dot.grid(row=0, column=0, padx=(12, 4), pady=8)

        self.info_lbl = customtkinter.CTkLabel(
            self.status_frame, text="Idle — ready to run",
            font=self._font_status, text_color=_P["text_secondary"]
        )
        self.info_lbl.grid(row=0, column=1, sticky="w", pady=8)

        # ── Bottom Spacer (push footer down) ───────────────────────────
        self.sidebar.grid_rowconfigure(7, weight=1)

        # ── Footer Credit ──────────────────────────────────────────────
        self.footer_lbl = customtkinter.CTkLabel(
            self.sidebar, text="Built with CustomTkinter",
            font=customtkinter.CTkFont(size=10), text_color=_P["text_muted"]
        )
        self.footer_lbl.grid(row=8, column=0, pady=(0, 14))

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #  RIGHT MAIN CONTENT
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        self.main_content = customtkinter.CTkFrame(
            self, fg_color=_P["bg_base"], corner_radius=0
        )
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=(4, 16), pady=16)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=4)   # Table Visualizer
        self.main_content.grid_rowconfigure(1, weight=0)   # Path Output (fixed)
        self.main_content.grid_rowconfigure(2, weight=5)   # Graph Plotter

        # ── 1. TOP: Interactive DP Table Visualization ──────────────────
        self.top_frame = customtkinter.CTkFrame(
            self.main_content, fg_color=_P["bg_card"],
            corner_radius=12, border_width=1, border_color=_P["border_subtle"]
        )
        self.top_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)

        # Top frame header bar
        self.top_header = customtkinter.CTkFrame(
            self.top_frame, fg_color=_P["bg_elevated"], corner_radius=0, height=42
        )
        self.top_header.grid(row=0, column=0, sticky="ew")
        self.top_header.grid_propagate(False)
        self.top_header.grid_columnconfigure(1, weight=1)

        self.top_icon = customtkinter.CTkLabel(
            self.top_header, text="◉", font=customtkinter.CTkFont(size=12),
            text_color=_P["accent_green"], width=20
        )
        self.top_icon.grid(row=0, column=0, padx=(16, 6), pady=10)

        self.top_title = customtkinter.CTkLabel(
            self.top_header, text="Interactive DP Table Visualization",
            font=self._font_section, text_color=_P["text_primary"]
        )
        self.top_title.grid(row=0, column=1, sticky="w", pady=10)

        # ── Table Container (monitor-style frame) ──────────────────────
        self.monitor_frame = customtkinter.CTkFrame(
            self.top_frame, fg_color=_P["bg_base"],
            corner_radius=6, border_width=2, border_color=_P["border_accent"]
        )
        self.monitor_frame.grid(row=1, column=0, sticky="nsew", padx=14, pady=(8, 14))
        self.monitor_frame.grid_rowconfigure(0, weight=1)
        self.monitor_frame.grid_columnconfigure(0, weight=1)

        self.table_container = customtkinter.CTkFrame(
            self.monitor_frame, fg_color=_P["bg_base"]
        )
        self.table_container.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.table_container.grid_rowconfigure(0, weight=1)
        self.table_container.grid_columnconfigure(0, weight=1)

        # Canvas
        self.table_canvas = tkinter.Canvas(
            self.table_container, bg=_P["bg_base"], highlightthickness=0
        )
        self.table_canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        self.vsb = customtkinter.CTkScrollbar(
            self.table_container, orientation="vertical",
            command=self.table_canvas.yview
        )
        self.hsb = customtkinter.CTkScrollbar(
            self.table_container, orientation="horizontal",
            command=self.table_canvas.xview
        )
        self.table_canvas.configure(
            yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set
        )

        # Inner Frame
        self.scrollable_inner_frame = customtkinter.CTkFrame(
            self.table_canvas, fg_color=_P["bg_base"]
        )
        self.canvas_window = self.table_canvas.create_window(
            (0, 0), window=self.scrollable_inner_frame, anchor="nw"
        )

        # Bindings
        self.scrollable_inner_frame.bind("<Configure>", self.on_inner_configure)
        self.table_canvas.bind("<Configure>", self.on_canvas_configure)
        self.table_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.table_canvas.bind_all("<Shift-MouseWheel>", self.on_shift_mousewheel)

        # ── 2. MIDDLE: Path Reconstruction ──────────────────────────────
        self.middle_frame = customtkinter.CTkFrame(
            self.main_content, fg_color=_P["bg_card"],
            corner_radius=12, border_width=1, border_color=_P["border_subtle"]
        )
        self.middle_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self.middle_frame.grid_columnconfigure(0, weight=1)

        self.path_icon = customtkinter.CTkLabel(
            self.middle_frame, text="🔗",
            font=customtkinter.CTkFont(size=14), width=24
        )
        self.path_icon.grid(row=0, column=0, padx=(18, 0), pady=14, sticky="w")

        self.path_lbl = customtkinter.CTkLabel(
            self.middle_frame,
            text="Optimal path reconstruction will appear here after analysis.",
            font=self._font_path, text_color=_P["accent_green"],
            wraplength=780, anchor="w", justify="left"
        )
        self.path_lbl.grid(row=0, column=1, padx=(6, 18), pady=14, sticky="w")
        self.middle_frame.grid_columnconfigure(1, weight=1)

        # ── 3. BOTTOM: Benchmarking Graph ───────────────────────────────
        self.bottom_frame = customtkinter.CTkFrame(
            self.main_content, fg_color=_P["bg_card"],
            corner_radius=12, border_width=1, border_color=_P["border_subtle"]
        )
        self.bottom_frame.grid(row=2, column=0, sticky="nsew")
        self.bottom_frame.grid_rowconfigure(1, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        # Bottom header bar
        self.bottom_header = customtkinter.CTkFrame(
            self.bottom_frame, fg_color=_P["bg_elevated"], corner_radius=0, height=42
        )
        self.bottom_header.grid(row=0, column=0, sticky="ew")
        self.bottom_header.grid_propagate(False)
        self.bottom_header.grid_columnconfigure(1, weight=1)

        self.bottom_icon = customtkinter.CTkLabel(
            self.bottom_header, text="◉", font=customtkinter.CTkFont(size=12),
            text_color=_P["accent_pink"], width=20
        )
        self.bottom_icon.grid(row=0, column=0, padx=(16, 6), pady=10)

        self.bottom_title = customtkinter.CTkLabel(
            self.bottom_header, text="Algorithm Performance Benchmarking",
            font=self._font_section, text_color=_P["text_primary"]
        )
        self.bottom_title.grid(row=0, column=1, sticky="w", pady=10)

        self.graph_frame = customtkinter.CTkFrame(
            self.bottom_frame, fg_color=_P["bg_base"]
        )
        self.graph_frame.grid(row=1, column=0, sticky="nsew", padx=14, pady=(8, 14))

        # Initialize Matplotlib Figure (dark-mode styling)
        self.fig, self.ax = plt.subplots(figsize=(6, 3), dpi=100)
        self.fig.patch.set_facecolor(_P["bg_card"])
        self.ax.set_facecolor(_P["bg_base"])
        self._style_graph_axes()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # ─── Animation State ────────────────────────────────────────────
        self.anim_matrix = None
        self.anim_cells = []
        self.anim_sequence = []
        self.anim_step_index = 0
        self.is_playing = False
        self.anim_timer_id = None
        self.anim_min_val = 0
        self.anim_max_val = 1
        self.anim_path_str = ""
        self.anim_complexity_label = ""
        self.anim_poly_power = 2
        self.anim_path_coords = []

        # Initialize with default placeholder styles
        self.on_algo_change("0/1 Knapsack")

    # ─── Helpers ─────────────────────────────────────────────────────────

    def _sidebar_divider(self, row):
        """Draw a thin horizontal divider line in the sidebar."""
        div = customtkinter.CTkFrame(
            self.sidebar, fg_color=_P["border_subtle"], height=1
        )
        div.grid(row=row, column=0, sticky="ew", padx=20, pady=(14, 0))

    # ─── Event Handlers & Logic (UNCHANGED) ──────────────────────────────

    def on_closing(self):
        self.quit()
        self.destroy()
        os._exit(0)

    def _style_graph_axes(self):
        self.ax.tick_params(colors=_P["text_secondary"], labelsize=9)
        self.ax.xaxis.label.set_color(_P["text_secondary"])
        self.ax.yaxis.label.set_color(_P["text_secondary"])
        self.ax.title.set_color(_P["accent_blue"])
        self.ax.title.set_fontsize(11)
        for spine in self.ax.spines.values():
            spine.set_color(_P["border_subtle"])
        self.ax.set_xlabel("Input Size (N)", fontsize=10)
        self.ax.set_ylabel("Execution Time (ms)", fontsize=10)
        self.ax.set_title("Performance Analysis: Run to plot curves")

    def on_speed_change(self, value):
        self.speed_lbl.configure(text=f"Speed: {value:.1f}s")

    def set_inputs_state(self, state):
        self.run_btn.configure(state=state)
        if state == "disabled":
            self.input1_entry.configure(state="disabled")
            self.input2_entry.configure(state="disabled")
            self.algo_menu.configure(state="disabled")
        else:
            self.input1_entry.configure(state="normal")
            self.algo_menu.configure(state="normal")
            selected_algo = self.algo_menu.get()
            if selected_algo == "Matrix Chain Multiplication":
                self.input2_entry.configure(state="disabled")
            else:
                self.input2_entry.configure(state="normal")

    def draw_no_data_plot(self, message="No Data Available"):
        self.ax.clear()
        self.ax.set_facecolor(_P["bg_base"])
        self._style_graph_axes()
        self.ax.text(
            0.5, 0.5, message, color=_P["accent_pink"], fontsize=10,
            ha='center', va='center', transform=self.ax.transAxes, wrap=True
        )
        self.canvas.draw()

    def on_inner_configure(self, event):
        self.update_scrollbars()

    def on_canvas_configure(self, event):
        self.update_scrollbars()

    def on_mousewheel(self, event):
        if hasattr(self, "table_canvas") and self.table_canvas.winfo_exists():
            self.table_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_shift_mousewheel(self, event):
        if hasattr(self, "table_canvas") and self.table_canvas.winfo_exists():
            self.table_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def scroll_to_cell(self, r, c):
        if not hasattr(self, "table_canvas") or not self.table_canvas.winfo_exists():
            return
        if not hasattr(self, "scrollable_inner_frame") or not self.scrollable_inner_frame.winfo_exists():
            return

        # Calculate cell bounding box (including headers)
        # Column width is 76 (74 + 2 padding)
        # Row height is 34 (32 + 2 padding)
        x_min = (c + 1) * 76
        x_max = (c + 2) * 76
        y_min = (r + 1) * 34
        y_max = (r + 2) * 34

        # Get total scrollable size
        total_w = self.scrollable_inner_frame.winfo_reqwidth()
        total_h = self.scrollable_inner_frame.winfo_reqheight()
        if total_w <= 0 or total_h <= 0:
            return

        # Get viewport size
        v_w = self.table_canvas.winfo_width()
        v_h = self.table_canvas.winfo_height()

        # Get current view fractions
        try:
            x_frac_start, x_frac_end = self.table_canvas.xview()
            y_frac_start, y_frac_end = self.table_canvas.yview()
        except Exception:
            return

        # Current visible coordinates
        v_left = x_frac_start * total_w
        v_right = x_frac_end * total_w
        v_top = y_frac_start * total_h
        v_bottom = y_frac_end * total_h

        # Adjust horizontal scroll if cell is out of view
        if x_min < v_left:
            self.table_canvas.xview_moveto(x_min / total_w)
        elif x_max > v_right:
            self.table_canvas.xview_moveto(max(0, x_max - v_w) / total_w)

        # Adjust vertical scroll if cell is out of view
        if y_min < v_top:
            self.table_canvas.yview_moveto(y_min / total_h)
        elif y_max > v_bottom:
            self.table_canvas.yview_moveto(max(0, y_max - v_h) / total_h)

    def update_scrollbars(self):
        if not hasattr(self, "table_canvas") or not self.table_canvas.winfo_exists():
            return
        if not hasattr(self, "scrollable_inner_frame") or not self.scrollable_inner_frame.winfo_exists():
            return

        # Force Tkinter geometry manager to process pending layout tasks
        # so frame_width and frame_height reflect the actual gridded table size
        self.update_idletasks()

        canvas_width = self.table_canvas.winfo_width()
        canvas_height = self.table_canvas.winfo_height()

        frame_width = self.scrollable_inner_frame.winfo_reqwidth()
        frame_height = self.scrollable_inner_frame.winfo_reqheight()

        # Expand inner frame if smaller than canvas
        new_width = max(canvas_width, frame_width)
        new_height = max(canvas_height, frame_height)

        # Avoid redundant configures to prevent recursive loops
        try:
            curr_w = float(self.table_canvas.itemcget(self.canvas_window, "width"))
            curr_h = float(self.table_canvas.itemcget(self.canvas_window, "height"))
        except Exception:
            curr_w, curr_h = 0, 0

        if abs(curr_w - new_width) > 1 or abs(curr_h - new_height) > 1:
            self.table_canvas.itemconfig(self.canvas_window, width=new_width, height=new_height)
            self.update_idletasks()

        # Determine the final scroll region using the bounding box of the inner frame
        bbox = self.table_canvas.bbox(self.canvas_window)
        if bbox:
            scroll_w = max(canvas_width, bbox[2])
            scroll_h = max(canvas_height, bbox[3])
            self.table_canvas.configure(scrollregion=(0, 0, scroll_w, scroll_h))
        else:
            self.table_canvas.configure(scrollregion=(0, 0, new_width, new_height))

        # Always grid both scrollbars so the table visualization is scrollable both ways in every single algorithm table
        self.hsb.grid(row=1, column=0, sticky="ew")
        self.vsb.grid(row=0, column=1, sticky="ns")

    def on_algo_change(self, choice):
        # Cancel any active animation
        if hasattr(self, "anim_timer_id") and self.anim_timer_id:
            self.after_cancel(self.anim_timer_id)
            self.anim_timer_id = None

        self.is_playing = False
        if hasattr(self, "play_pause_btn"):
            self.play_pause_btn.configure(text="▶  Play")
        if hasattr(self, "info_lbl"):
            self.info_lbl.configure(text="Idle — ready to run")
            if hasattr(self, "status_dot"):
                self.status_dot.configure(text_color=_P["text_muted"])

        # Clear table grid
        if hasattr(self, "scrollable_inner_frame"):
            for child in self.scrollable_inner_frame.winfo_children():
                child.destroy()
            self.update_scrollbars()

        # Reset optimal path label and graph performance title
        if hasattr(self, "path_lbl"):
            self.path_lbl.configure(text="Optimal path reconstruction will appear here after analysis.")

        if choice == "0/1 Knapsack":
            self.input1_lbl.configure(text="Weights & Capacity:")
            self.input1_entry.delete(0, customtkinter.END)
            self.input1_entry.configure(placeholder_text="e.g. 1, 2, 3 | 5")
            self.input2_lbl.configure(text="Values:")
            self.input2_entry.configure(state="normal")
            self.input2_entry.delete(0, customtkinter.END)
            self.input2_entry.configure(placeholder_text="e.g. 6, 10, 12")
        elif choice == "Longest Common Subsequence":
            self.input1_lbl.configure(text="String X:")
            self.input1_entry.delete(0, customtkinter.END)
            self.input1_entry.configure(placeholder_text="e.g. ABCBDAB")
            self.input2_lbl.configure(text="String Y:")
            self.input2_entry.configure(state="normal")
            self.input2_entry.delete(0, customtkinter.END)
            self.input2_entry.configure(placeholder_text="e.g. BDCABA")
        elif choice == "Coin Change":
            self.input1_lbl.configure(text="Coins:")
            self.input1_entry.delete(0, customtkinter.END)
            self.input1_entry.configure(placeholder_text="e.g. 1, 2, 5")
            self.input2_lbl.configure(text="Target Amount:")
            self.input2_entry.configure(state="normal")
            self.input2_entry.delete(0, customtkinter.END)
            self.input2_entry.configure(placeholder_text="e.g. 11")
        elif choice == "Matrix Chain Multiplication":
            self.input1_lbl.configure(text="Dimensions:")
            self.input1_entry.delete(0, customtkinter.END)
            self.input1_entry.configure(placeholder_text="e.g. 40, 20, 30, 10, 30")
            self.input2_lbl.configure(text="Values/Array 2 (Unused):")
            self.input2_entry.delete(0, customtkinter.END)
            self.input2_entry.configure(placeholder_text="Not used for MCM")
            self.input2_entry.configure(state="disabled")

    def run_algorithm(self):
        self.run_analysis()

    def run_analysis(self):
        try:
            if self.anim_timer_id:
                self.after_cancel(self.anim_timer_id)
                self.anim_timer_id = None

            selected_algo = self.algo_menu.get()

            # Read inputs
            input1 = self.input1_entry.get().strip()
            input2 = self.input2_entry.get().strip()

            # Use defaults if empty
            if not input1:
                if selected_algo == "0/1 Knapsack":
                    input1 = "1, 2, 3 | 5"
                elif selected_algo == "Longest Common Subsequence":
                    input1 = "ABCBDAB"
                elif selected_algo == "Coin Change":
                    input1 = "1, 2, 5"
                elif selected_algo == "Matrix Chain Multiplication":
                    input1 = "40, 20, 30, 10, 30"

            if not input2 and selected_algo != "Matrix Chain Multiplication":
                if selected_algo == "0/1 Knapsack":
                    input2 = "6, 10, 12"
                elif selected_algo == "Longest Common Subsequence":
                    input2 = "BDCABA"
                elif selected_algo == "Coin Change":
                    input2 = "11"

            # Parse inputs & run actual core algorithms
            if selected_algo == "0/1 Knapsack":
                if "|" not in input1:
                    raise ValueError("Input 1 must be weights & capacity separated by '|' (e.g. 1, 2, 3 | 5)")
                w_str, c_str = input1.split("|")
                weights = [int(x.strip()) for x in w_str.split(",") if x.strip()]
                capacity = int(c_str.strip())
                values = [int(x.strip()) for x in input2.split(",") if x.strip()]

                if len(weights) != len(values):
                    raise ValueError("Weights count must match values count.")
                if any(x <= 0 for x in weights) or any(x < 0 for x in values):
                    raise ValueError("Weights and values must be positive numbers.")

                res = knapsack.solve_tabular(weights, values, capacity)
                matrix = res["table"]
                length = res["length"]
                path_str = res["path"]

                rows = len(matrix)
                cols = len(matrix[0])
                row_hdrs = ["Base"] + [f"Item {i} (w:{weights[i-1]}, v:{values[i-1]})" for i in range(1, rows)]
                col_hdrs = [str(w) for w in range(cols)]

                # Traceback coordinates
                path_coords = []
                w = capacity
                for i in range(rows - 1, 0, -1):
                    if matrix[i][w] != matrix[i-1][w]:
                        path_coords.append((i, w))
                        w -= weights[i-1]
                path_coords.append((0, w))
                self.anim_path_coords = path_coords

                display_path_str = f"Optimal Value: {length} | {path_str}"
                complexity_label = "O(N * W)"
                poly_power = 2

            elif selected_algo == "Longest Common Subsequence":
                X = input1
                Y = input2

                res = lcs.solve_tabular(X, Y)
                matrix = res["table"]
                length = res["length"]
                path_str = res["path"]

                rows = len(matrix)
                cols = len(matrix[0])
                row_hdrs = ["-"] + list(X)
                col_hdrs = ["-"] + list(Y)

                # Traceback coordinates
                path_coords = []
                i, j = rows - 1, cols - 1
                while i > 0 and j > 0:
                    if X[i-1] == Y[j-1]:
                        path_coords.append((i, j))
                        i -= 1
                        j -= 1
                    elif matrix[i-1][j] >= matrix[i][j-1]:
                        i -= 1
                    else:
                        j -= 1
                path_coords.append((0, 0))
                self.anim_path_coords = path_coords

                display_path_str = f"LCS Length: {length} | Subsequence: '{path_str}'"
                complexity_label = "O(M * N)"
                poly_power = 2

            elif selected_algo == "Coin Change":
                coins = [int(x.strip()) for x in input1.split(",") if x.strip()]
                amount = int(input2.strip())

                if amount < 0:
                    raise ValueError("Target Amount must be positive.")
                if any(c <= 0 for c in coins):
                    raise ValueError("Coin denominations must be positive numbers.")

                res = coinchange.solve_tabular(coins, amount)
                matrix = res["table"]
                length = res["length"]
                path_str = res["path"]

                rows = len(matrix)
                cols = len(matrix[0])
                row_hdrs = ["Base"] + [f"Coin {c}" for c in coins]
                col_hdrs = [str(a) for a in range(cols)]

                # Traceback coordinates
                path_coords = []
                if matrix[rows - 1][amount] != 99999:  # 99999 represents infinity/no solution
                    i, j = rows - 1, amount
                    while j > 0 and i > 0:
                        if matrix[i][j] == matrix[i-1][j]:
                            i -= 1
                        else:
                            path_coords.append((i, j))
                            j -= coins[i-1]
                    path_coords.append((0, 0))
                self.anim_path_coords = path_coords

                display_path_str = f"Min Coins: {length if length != -1 else 'No Solution'} | {path_str}"
                complexity_label = "O(N * Amount)"
                poly_power = 2

            else:  # Matrix Chain Multiplication
                p = [int(x.strip()) for x in input1.split(",") if x.strip()]
                if len(p) < 2:
                    raise ValueError("MCM dimensions must contain at least 2 numbers (e.g. 40, 20).")
                if any(x <= 0 for x in p):
                    raise ValueError("Dimensions must be positive integers.")

                res = matrix_chain.solve_tabular(p)
                matrix = res["table"]
                length = res["length"]
                path_str = res["path"]

                rows = len(matrix)
                cols = len(matrix[0])
                row_hdrs = [str(r) for r in range(rows)]
                col_hdrs = [str(c) for c in range(cols)]

                # Traceback coordinates
                path_coords = []
                n = rows - 1
                def trace_mcm(i, j):
                    if i == j:
                        return
                    for k in range(i, j):
                        cost = matrix[i][k] + matrix[k+1][j] + p[i-1]*p[k]*p[j]
                        if matrix[i][j] == cost:
                            path_coords.append((i, j))
                            trace_mcm(i, k)
                            trace_mcm(k+1, j)
                            break
                if n >= 1:
                    trace_mcm(1, n)
                self.anim_path_coords = path_coords

                display_path_str = f"Min Multiplications: {length} | Scheme: {path_str}"
                complexity_label = "O(N^3)"
                poly_power = 3

            # Disable main inputs
            self.set_inputs_state("disabled")

            # Save state
            self.anim_path_str = display_path_str
            self.anim_complexity_label = complexity_label
            self.anim_poly_power = poly_power

            # Initialize grid
            self.animate_grid(matrix, row_hdrs, col_hdrs)

            # Run animation loop
            self.is_playing = True
            self.play_pause_btn.configure(text="⏸  Pause")
            self.status_dot.configure(text_color=_P["accent_green"])
            self.animate_loop()

        except Exception as e:
            # Re-enable inputs
            self.set_inputs_state("normal")
            self.info_lbl.configure(text="Error encountered!")
            self.status_dot.configure(text_color=_P["accent_pink"])
            self.path_lbl.configure(text=f"Error: {str(e)}")
            self.draw_no_data_plot(f"Analysis Error:\n{str(e)}")
            self.is_playing = False
            self.play_pause_btn.configure(text="▶  Play")
            if self.anim_timer_id:
                self.after_cancel(self.anim_timer_id)
                self.anim_timer_id = None

    def get_update_sequence(self, selected_algo, rows, cols):
        sequence = []
        if selected_algo == "0/1 Knapsack":
            for r in range(1, rows):
                for c in range(1, cols):
                    sequence.append((r, c))
        elif selected_algo == "Longest Common Subsequence":
            for r in range(1, rows):
                for c in range(1, cols):
                    sequence.append((r, c))
        elif selected_algo == "Coin Change":
            for r in range(1, rows):
                for c in range(1, cols):
                    sequence.append((r, c))
        elif selected_algo == "Matrix Chain Multiplication":
            n = rows - 1
            for L in range(2, n + 1):
                for i in range(1, n - L + 2):
                    j = i + L - 1
                    sequence.append((i, j))
        return sequence

    def get_heatmap_color(self, val, min_val, max_val):
        if val == 99999 or val == 999999:
            return _P["heatmap_low"], _P["accent_pink"]  # Infinity styling

        if max_val == min_val:
            ratio = 0.5
        else:
            ratio = float(val - min_val) / float(max_val - min_val)

        ratio = max(0.0, min(1.0, ratio))

        # Heatmap gradient: deep dark → accent blue
        r_start, g_start, b_start = 26, 26, 46   # _P["heatmap_low"]
        r_end, g_end, b_end = 124, 147, 245       # _P["heatmap_high"]

        r = int(r_start + ratio * (r_end - r_start))
        g = int(g_start + ratio * (g_end - g_start))
        b = int(b_start + ratio * (b_end - b_start))

        bg_color = f"#{r:02x}{g:02x}{b:02x}"
        text_color = "#0f0f1a" if ratio > 0.55 else _P["text_primary"]
        return bg_color, text_color

    def animate_grid(self, matrix, row_hdrs, col_hdrs):
        selected_algo = self.algo_menu.get()
        rows = len(matrix)
        cols = len(matrix[0])

        self.anim_matrix = matrix
        self.anim_step_index = 0
        self.anim_sequence = self.get_update_sequence(selected_algo, rows, cols)

        # Clear previous table grid
        for child in self.scrollable_inner_frame.winfo_children():
            child.destroy()

        # Draw headers
        header_lbl = customtkinter.CTkLabel(
            self.scrollable_inner_frame, text="", width=74, height=32,
            fg_color=_P["bg_elevated"], text_color=_P["text_secondary"],
            corner_radius=4
        )
        header_lbl.grid(row=0, column=0, padx=1, pady=1)

        for c in range(cols):
            lbl = customtkinter.CTkLabel(
                self.scrollable_inner_frame, text=str(col_hdrs[c]),
                width=74, height=32,
                fg_color=_P["bg_elevated"], text_color=_P["text_secondary"],
                corner_radius=4, font=self._font_cell_bold
            )
            lbl.grid(row=0, column=c+1, padx=1, pady=1)

        for r in range(rows):
            row_lbl = customtkinter.CTkLabel(
                self.scrollable_inner_frame, text=str(row_hdrs[r]),
                width=74, height=32,
                fg_color=_P["bg_elevated"], text_color=_P["text_secondary"],
                corner_radius=4, font=self._font_cell_bold
            )
            row_lbl.grid(row=r+1, column=0, padx=1, pady=1)

        # Instantiate grid cells
        self.anim_cells = [[None] * cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                is_base = False
                val_str = "—"
                cell_fg_color = _P["heatmap_low"]
                text_fg = _P["text_muted"]

                if selected_algo == "0/1 Knapsack":
                    if r == 0 or c == 0:
                        is_base = True
                        val_str = str(matrix[r][c])
                elif selected_algo == "Longest Common Subsequence":
                    if r == 0 or c == 0:
                        is_base = True
                        val_str = str(matrix[r][c])
                elif selected_algo == "Coin Change":
                    if r == 0 or c == 0:
                        is_base = True
                        val = matrix[r][c]
                        val_str = "∞" if val == 99999 else str(val)
                elif selected_algo == "Matrix Chain Multiplication":
                    if r == 0 or c == 0 or r > c:
                        is_base = True
                        val_str = ""
                        cell_fg_color = _P["bg_base"]
                    elif r == c:
                        is_base = True
                        val_str = "0"

                if is_base:
                    if cell_fg_color != _P["bg_base"]:
                        cell_fg_color = _P["bg_elevated"]
                        text_fg = _P["text_secondary"]

                lbl = customtkinter.CTkLabel(
                    self.scrollable_inner_frame,
                    text=val_str, width=74, height=32,
                    fg_color=cell_fg_color, text_color=text_fg,
                    corner_radius=4,
                    font=self._font_cell_bold if is_base else self._font_cell
                )
                lbl.grid(row=r+1, column=c+1, padx=1, pady=1)
                self.anim_cells[r][c] = lbl

        # Find min/max values excluding infinity and unused
        valid_vals = []
        for r in range(rows):
            for c in range(cols):
                if selected_algo == "Matrix Chain Multiplication" and (r == 0 or c == 0 or r >= c):
                    continue
                val = matrix[r][c]
                if val != 99999 and val != 999999:
                    valid_vals.append(val)

        self.anim_min_val = min(valid_vals) if valid_vals else 0
        self.anim_max_val = max(valid_vals) if valid_vals else 1

        self.path_lbl.configure(text="Calculating optimal path via dynamic programming…")
        self.info_lbl.configure(text=f"Step: 0/{len(self.anim_sequence)}")

        # Reset scroll viewport to top-left when a new grid is rendered
        self.table_canvas.xview_moveto(0)
        self.table_canvas.yview_moveto(0)
        self.update_scrollbars()

    def toggle_play_pause(self):
        if not hasattr(self, "anim_sequence") or not self.anim_sequence:
            self.run_algorithm()
            return

        if self.anim_step_index >= len(self.anim_sequence):
            self.run_algorithm()
            return

        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_pause_btn.configure(text="⏸  Pause")
            self.status_dot.configure(text_color=_P["accent_green"])
            self.animate_loop()
        else:
            self.play_pause_btn.configure(text="▶  Play")
            self.status_dot.configure(text_color=_P["accent_amber"])
            if self.anim_timer_id:
                self.after_cancel(self.anim_timer_id)
                self.anim_timer_id = None

    def next_step(self):
        if not hasattr(self, "anim_sequence") or not self.anim_sequence:
            self.run_algorithm()
            self.is_playing = False
            self.play_pause_btn.configure(text="▶  Play")
            if self.anim_timer_id:
                self.after_cancel(self.anim_timer_id)
                self.anim_timer_id = None
            return

        if self.anim_step_index >= len(self.anim_sequence):
            self.run_algorithm()
            self.is_playing = False
            self.play_pause_btn.configure(text="▶  Play")
            if self.anim_timer_id:
                self.after_cancel(self.anim_timer_id)
                self.anim_timer_id = None
            return

        if self.is_playing:
            self.is_playing = False
            self.play_pause_btn.configure(text="▶  Play")
            self.status_dot.configure(text_color=_P["accent_amber"])
            if self.anim_timer_id:
                self.after_cancel(self.anim_timer_id)
                self.anim_timer_id = None

        self.animate_step()

    def animate_step(self):
        if not hasattr(self, "anim_sequence") or not self.anim_sequence:
            return

        if self.anim_step_index >= len(self.anim_sequence):
            self.on_animation_complete()
            return

        # 1. Update previous active cell to its final heatmap color
        if self.anim_step_index > 0:
            prev_r, prev_c = self.anim_sequence[self.anim_step_index - 1]
            val = self.anim_matrix[prev_r][prev_c]
            color, text_color = self.get_heatmap_color(val, self.anim_min_val, self.anim_max_val)
            self.anim_cells[prev_r][prev_c].configure(fg_color=color, text_color=text_color)

        # 2. Make current cell active
        r, c = self.anim_sequence[self.anim_step_index]
        val = self.anim_matrix[r][c]
        val_str = "∞" if (val == 99999 or val == 999999) else str(val)

        self.anim_cells[r][c].configure(
            text=val_str, fg_color=_P["accent_green"],
            text_color="#0f0f1a", font=self._font_cell_bold
        )
        self.info_lbl.configure(text=f"Step: {self.anim_step_index + 1}/{len(self.anim_sequence)}")

        # Auto-scroll both ways to keep the active cell in view
        self.scroll_to_cell(r, c)

        self.anim_step_index += 1

    def animate_loop(self):
        if not self.is_playing:
            return

        delay_sec = self.speed_slider.get()
        delay_ms = int(delay_sec * 1000)

        self.animate_step()

        if self.anim_step_index < len(self.anim_sequence):
            self.anim_timer_id = self.after(delay_ms, self.animate_loop)
        else:
            self.anim_timer_id = self.after(delay_ms, self.on_animation_complete)

    def on_animation_complete(self):
        # 1. Update last cell
        if self.anim_sequence:
            last_r, last_c = self.anim_sequence[-1]
            val = self.anim_matrix[last_r][last_c]
            color, text_color = self.get_heatmap_color(val, self.anim_min_val, self.anim_max_val)
            self.anim_cells[last_r][last_c].configure(fg_color=color, text_color=text_color)

        # 2. Highlight optimal path traceback
        selected_algo = self.algo_menu.get()
        rows = len(self.anim_matrix)
        cols = len(self.anim_matrix[0])

        path_set = set(self.anim_path_coords) if hasattr(self, "anim_path_coords") and self.anim_path_coords else set()
        for r in range(rows):
            for c in range(cols):
                if (r, c) in path_set:
                    lbl = self.anim_cells[r][c]
                    if lbl:
                        lbl.configure(
                            fg_color=_P["accent_green"],
                            text_color="#0f0f1a",
                            font=self._font_cell_bold
                        )

        # 3. Update path label
        self.path_lbl.configure(text=self.anim_path_str)

        # 4. Benchmarking Graph - real results from benchmarker
        try:
            sizes, recursive_times, dp_times = benchmarker.benchmark_algorithm(selected_algo)

            self.ax.clear()
            self.ax.set_facecolor(_P["bg_base"])
            self._style_graph_axes()
            self.ax.set_title(f"Performance Analysis: {selected_algo}")

            # Filter valid times
            rec_sizes = [sizes[i] for i in range(len(sizes)) if recursive_times[i] is not None]
            rec_y = [recursive_times[i] for i in range(len(sizes)) if recursive_times[i] is not None]

            dp_sizes = [sizes[i] for i in range(len(sizes)) if dp_times[i] is not None]
            dp_y = [dp_times[i] for i in range(len(sizes)) if dp_times[i] is not None]

            if not dp_y:
                self.draw_no_data_plot("No benchmarking data available.")
            else:
                if rec_y:
                    self.ax.plot(
                        rec_sizes, rec_y, label="Recursive O(2^N)",
                        color=_P["accent_pink"], marker='o', linewidth=2,
                        markersize=5, alpha=0.9
                    )
                self.ax.plot(
                    dp_sizes, dp_y, label=f"DP {self.anim_complexity_label}",
                    color=_P["accent_blue"], marker='s', linewidth=2,
                    markersize=5, alpha=0.9
                )

                legend = self.ax.legend(
                    facecolor=_P["bg_card"], edgecolor=_P["border_subtle"],
                    fontsize=9
                )
                for text in legend.get_texts():
                    text.set_color(_P["text_primary"])
                self.canvas.draw()
        except Exception as e:
            self.draw_no_data_plot(f"Benchmarking Error:\n{str(e)}")

        # 5. Reset states
        self.set_inputs_state("normal")
        self.is_playing = False
        self.play_pause_btn.configure(text="▶  Play")
        self.info_lbl.configure(text="✓ Animation Complete!")
        self.status_dot.configure(text_color=_P["accent_cyan"])
        if self.anim_timer_id:
            self.after_cancel(self.anim_timer_id)
            self.anim_timer_id = None


if __name__ == "__main__":
    app = App()
    app.mainloop()
