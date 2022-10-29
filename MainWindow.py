import tkinter as tk
from tkinter import ttk

class MainWindow:

    def __init__(self, window: tk.Tk) -> None:
        self.window = window
        self.canvas = None

    def draw_window(self) -> None:
        self.canvas = tk.Canvas(self.window, background='white', width=800, height=750)
        self.canvas.place(x=10, y=10)