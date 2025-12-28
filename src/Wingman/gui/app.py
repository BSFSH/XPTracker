import tkinter as tk
from tkinter import ttk
from Wingman.core.session import GameSession


class XPTrackerApp:
    def __init__(self, session: GameSession):
        self.session = session

        self.root = tk.Tk()
        self.root.title("Wingman - Olmran")
        self.root.geometry("500x350")  # Widened slightly for the columns
        self.root.attributes("-topmost", True)

        self.var_total_xp = tk.StringVar(value="Total XP: 0")
        self.var_xp_hr = tk.StringVar(value="XP/Hr: 0")
        self.var_duration = tk.StringVar(value="Time: 00:00:00")

        self.setup_ui()
        self.update_gui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Top Stats Row ---
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))

        # Column 1: Totals
        col1 = ttk.Frame(stats_frame)
        col1.pack(side=tk.LEFT, padx=5)
        ttk.Label(col1, textvariable=self.var_total_xp, font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(col1, textvariable=self.var_xp_hr).pack(anchor="w")

        # Column 2: Time & Reset
        col2 = ttk.Frame(stats_frame)
        col2.pack(side=tk.RIGHT, padx=5)
        ttk.Label(col2, textvariable=self.var_duration, font=("Consolas", 10)).pack(anchor="e")
        ttk.Button(col2, text="Reset", command=self.reset_stats, width=6).pack(pady=2)

        # --- Group Dashboard (Treeview) ---
        lbl_dash = ttk.Label(main_frame, text="Group Status:", font=("Segoe UI", 10, "bold"))
        lbl_dash.pack(anchor="w", pady=(5, 0))

        # Define Columns
        columns = ("cls", "lvl", "name", "hp", "fat", "pwr")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)

        # Setup Headings
        self.tree.heading("cls", text="Class")
        self.tree.heading("lvl", text="Lvl")
        self.tree.heading("name", text="Name")
        self.tree.heading("hp", text="HP")
        self.tree.heading("fat", text="Fatigue")
        self.tree.heading("pwr", text="Power")

        # Setup Columns Widths
        self.tree.column("cls", width=50, anchor="center")
        self.tree.column("lvl", width=40, anchor="center")
        self.tree.column("name", width=100, anchor="w")
        self.tree.column("hp", width=80, anchor="center")
        self.tree.column("fat", width=80, anchor="center")
        self.tree.column("pwr", width=80, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def reset_stats(self):
        self.session.reset()
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)

    def update_gui(self):
        # 1. Process Queue (Standard XP logs still happen in background)
        # We assume session.process_queue() handles parsing internally
        self.session.process_queue()

        # 2. Update Group Dashboard
        # You need to implement get_latest_group_data() in your session!
        group_data = self.session.get_latest_group_data()
        if group_data:
            self._refresh_tree(group_data)

        # 3. Update Variables
        current_xp = self.session.total_xp
        current_rate = self.session.get_xp_per_hour()

        self.var_total_xp.set(f"Total: {current_xp:,}")
        self.var_xp_hr.set(f"{current_rate:,} /hr")
        self.var_duration.set(self.session.get_duration_str())

        self.root.after(100, self.update_gui)

    def _refresh_tree(self, members):
        """Clears and refills the treeview."""
        # Clear current list
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Refill
        for m in members:
            # Match keys from parser dictionary
            values = (m['cls'], m['lvl'], m['name'], m['hp'], m['fat'], m['pwr'])
            self.tree.insert("", tk.END, values=values)

    def run(self):
        self.root.mainloop()