# GUI/visualizer.py
import tkinter as tk
from tkinter import ttk

class DPTableVisualizer(ttk.Frame):
    """
    A custom scrollable canvas widget to render DP tables with custom cell colors,
    headers, and highlighted paths.
    """
    def __init__(self, parent, cell_width=70, cell_height=35, **kwargs):
        super().__init__(parent, **kwargs)
        self.cell_width = cell_width
        self.cell_height = cell_height
        
        # Grid layout for Canvas + Scrollbars
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Canvas with modern dark background
        self.canvas = tk.Canvas(self, bg="#1e1e2e", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbars styled for dark theme
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.hsb.grid(row=1, column=0, sticky="ew")
        
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        # Mouse wheel scrolling bindings
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Shift-MouseWheel>", self._on_shift_mousewheel)
        
    def _on_mousewheel(self, event):
        # Scroll vertically
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_shift_mousewheel(self, event):
        # Scroll horizontally
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def clear(self):
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=(0, 0, 0, 0))
        
    def draw_table(self, dp_table, row_headers, col_headers, path=None, draw_arrows=True):
        """
        Draws the DP table.
        
        dp_table: 2D list of numbers/values.
        row_headers: Labels for each row (length matching len(dp_table)).
        col_headers: Labels for each column (length matching len(dp_table[0])).
        path: List of coordinates (i, j) that are part of the reconstruction path.
        draw_arrows: Boolean to enable/disable drawing arrows along the path.
        """
        self.clear()
        
        num_rows = len(dp_table)
        num_cols = len(dp_table[0]) if num_rows > 0 else 0
        
        if num_rows == 0 or num_cols == 0:
            return
            
        # Total size of the table (including headers at index 0)
        total_width = (num_cols + 1) * self.cell_width
        total_height = (num_rows + 1) * self.cell_height
        
        # Theme colors (Catppuccin Mocha style)
        bg_header = "#313244"
        fg_header = "#cdd6f4"
        bg_cell = "#181825"
        fg_cell = "#a6adc8"
        bg_path = "#a6e3a1"      # Green for path
        fg_path = "#11111b"
        bg_infinity = "#f38ba8"  # Red/pink for infinity
        border_color = "#45475a"
        
        # Convert path to set for O(1) lookup
        path_set = set(path) if path else set()
        
        # 1. Draw Col Headers (Row 0)
        self.canvas.create_rectangle(
            0, 0, self.cell_width, self.cell_height,
            fill=bg_header, outline=border_color
        )
        
        for j in range(num_cols):
            x1 = (j + 1) * self.cell_width
            y1 = 0
            x2 = x1 + self.cell_width
            y2 = self.cell_height
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_header, outline=border_color)
            self.canvas.create_text(
                (x1 + x2) / 2, (y1 + y2) / 2,
                text=str(col_headers[j]), fill=fg_header, font=("Courier New", 10, "bold")
            )
            
        # 2. Draw Rows (Row Headers + Cells)
        for i in range(num_rows):
            # Row Header
            y1 = (i + 1) * self.cell_height
            x1 = 0
            y2 = y1 + self.cell_height
            x2 = self.cell_width
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_header, outline=border_color)
            self.canvas.create_text(
                (x1 + x2) / 2, (y1 + y2) / 2,
                text=str(row_headers[i]), fill=fg_header, font=("Courier New", 10, "bold")
            )
            
            # Row Cells
            for j in range(num_cols):
                cx1 = (j + 1) * self.cell_width
                cy1 = (i + 1) * self.cell_height
                cx2 = cx1 + self.cell_width
                cy2 = cy1 + self.cell_height
                
                val = dp_table[i][j]
                
                # Check formatting of values
                if val == float('inf'):
                    val_str = "∞"
                    cell_fill = bg_cell
                    cell_fg = bg_infinity
                elif val == -1:
                    val_str = "-1"
                    cell_fill = bg_cell
                    cell_fg = fg_cell
                else:
                    val_str = str(val)
                    cell_fill = bg_cell
                    cell_fg = fg_cell
                
                # Check if this cell is in the path
                if (i, j) in path_set:
                    cell_fill = bg_path
                    cell_fg = fg_path
                
                self.canvas.create_rectangle(cx1, cy1, cx2, cy2, fill=cell_fill, outline=border_color)
                self.canvas.create_text(
                    (cx1 + cx2) / 2, (cy1 + cy2) / 2,
                    text=val_str, fill=cell_fg, font=("Courier New", 10, "bold" if (i, j) in path_set else "normal")
                )
                
        # 3. Draw Path arrows if path is present and consecutive cells exist
        if draw_arrows and path and len(path) > 1:
            for idx in range(len(path) - 1):
                i1, j1 = path[idx]
                i2, j2 = path[idx+1]
                
                # Canvas coordinates of centers of the cells
                start_x = (j1 + 1.5) * self.cell_width
                start_y = (i1 + 1.5) * self.cell_height
                end_x = (j2 + 1.5) * self.cell_width
                end_y = (i2 + 1.5) * self.cell_height
                
                # Draw arrow from start to end (direction of reconstruction)
                self.canvas.create_line(
                    start_x, start_y, end_x, end_y,
                    arrow=tk.LAST, fill="#f9e2af", width=2.5,
                    arrowshape=(10, 12, 4)
                )

        # Update scroll region
        self.canvas.configure(scrollregion=(0, 0, total_width + 40, total_height + 40))