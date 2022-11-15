#здесь должна юыть реализована логика отрисовки графиков
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from matplotlib.figure import Figure


class FermiCanvas:
    def __init__(self, canvas: tk.Canvas) -> None:
        self.window = canvas
        self.fig = Figure()
        self.fig.set_figheight(10)   # Задаю размер графа
        self.fig.set_figwidth(14)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, self.window)
        self.ax.grid()
        self.ax.set_xlabel("x [cm]")
        self.ax.set_ylabel("E [eV]")
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw(self, data: dict) -> None:
        self.ax.cla()
        self.ax.plot(data['x'], data['Ec'], c='red', label='Conduction Band')
        self.ax.plot(data['x'], data['Ef'], c='darkorange', label='Fermi Energy')
        self.ax.plot(data['x'], data['Ea'], c='green', label='Acceptor Energy')
        self.ax.plot(data['x'], data['Ed'], c='blue', label='Donor Energy')
        self.ax.plot(data['x'], data['Ev'], c='purple', label='Valence Band')

        self.ax.axhline(data['phi'], c='k', linestyle='dashed')
        self.ax.axvline(data['W'], c='k', linestyle='dashed')

        self.ax.legend(fontsize=10, loc='right')
        self.canvas.draw()