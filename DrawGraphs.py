#здесь должна юыть реализована логика отрисовки графиков
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from matplotlib.figure import Figure


class FermiCanvas:
    def __init__(self, canvas: tk.Canvas) -> None:
        self.window = canvas
        self.fig = Figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, self.window)
        self.ax.grid()
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw(self) -> None:
        pass
