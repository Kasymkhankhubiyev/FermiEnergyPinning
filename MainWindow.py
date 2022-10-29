import tkinter as tk
from tkinter import ttk

class MainWindow:

    def __init__(self, window: tk.Tk) -> None:
        self.window = window
        self.canvas = None

    def _select_template(self) -> None:
        pass

    def draw_window(self) -> None:
        self.canvas = tk.Canvas(self.window, background='white', width=650, height=600)
        self.canvas.place(x=10, y=10)

        font = ('Arial', 20)

        tk.Label(self.window, text='Шаблон полупроводника:', font=font).place(x=700, y=30)
        combobox = ttk.Combobox(self.window, values=['Кремний'], font=font)
        combobox.place(x=700, y=70)

        combobox.bind("<<ComboboxSelected>>", self._select_template)

        tk.Label(self.window, text='Mc/m0', font=('Arial', 18)).place(x=700, y=122)
        tk.Entry(self.window, font=font, width=5).place(x=780, y=120)

        tk.Label(self.window, text='Mv/m0', font=('Arial', 18)).place(x=870, y=122)
        tk.Entry(self.window, font=font, width=5).place(x=950, y=120)

        tk.Label(self.window, text='концентрация доноров Nd', font=font).place(x=700, y=180)
        tk.Spinbox(self.window, font=font).place(x=700, y=220)

        tk.Label(self.window, text='концентрация доноров Nas', font=font).place(x=700, y=280)
        tk.Spinbox(self.window, font=font).place(x=700, y=320)

        tk.Label(self.window, text='Eg', font=('Arial', 18)).place(x=700, y=382)  #+380
        tk.Entry(self.window, font=font, width=5).place(x=750, y=380)

        tk.Label(self.window, text='ε', font=('Arial', 20)).place(x=870, y=378)
        tk.Entry(self.window, font=font, width=5).place(x=900, y=380)

        tk.Label(self.window, text='Ed', font=('Arial', 18)).place(x=700, y=442)  # +380
        tk.Entry(self.window, font=font, width=5).place(x=750, y=440)

        tk.Label(self.window, text='T', font=('Arial', 18)).place(x=870, y=442)
        tk.Entry(self.window, font=font, width=5).place(x=900, y=440)

        tk.Label(self.window, text='Внешнее поле Eout [В/м]', font=('Arial', 18)).place(x=705, y=487)
        tk.Entry(self.window, font=font, width=20).place(x=700, y=525)

        tk.Button(self.window, text='Найти уровень Ферми', font=font, bg='SteelBlue1').place(x=700, y=565)




