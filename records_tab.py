import tkinter as tk
from tkinter import ttk

from gui.records_tab import RecordsTab

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical History Database System")
        self.root.geometry("900x600")

        # Notebook (tab layout)
        self.notebook = ttk.Notebook(self.root)

        # Tabs
        self.records_tab = ttk.Frame(self.notebook)
        RecordsTab(self.records_tab)

        self.reminders_tab = ttk.Frame(self.notebook)
        self.charts_tab = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.records_tab, text="Records")
        self.notebook.add(self.reminders_tab, text="Reminders")
        self.notebook.add(self.charts_tab, text="Health Charts")

        self.notebook.pack(expand=True, fill="both")

def launch_gui():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
