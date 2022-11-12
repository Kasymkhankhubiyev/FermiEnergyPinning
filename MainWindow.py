import tkinter as tk
from tkinter import ttk
import SemoconductorsTemplates as st
import DrawGraphs as dg

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class MainWindow:

    def __init__(self, window: tk.Tk) -> None:
        self.window = window
        self.canvas, self.fermi_canvas, self.combobox = None, None, None
        self.mc_entry, self.mv_entry, self.nd_entry = None, None, None
        self.nas_entry, self.eg_entry, self.epsilon_entry = None, None, None
        self.ed_entry, self.eout_entry, self.temp_entry = None, None, None

    def _clear_entry(self, entry: tk.Entry) -> None:
        entry.delete(0, tk.END)

    def _set_template_attributes(self, template) -> None:
        self._clear_entry(entry=self.mc_entry)
        self.mc_entry.insert(0, template.mc)

        self._clear_entry(entry=self.mv_entry)
        self.mv_entry.insert(0, template.mv)

        self._clear_entry(entry=self.eg_entry)
        self.eg_entry.insert(0, template.Eg)

        self._clear_entry(entry=self.epsilon_entry)
        self.epsilon_entry.insert(0, template.epsilon)

    def _select_template(self, event) -> None:
        selected = self.combobox.get()
        if selected == 'Si':
            self._set_template_attributes(template=st.Si())
        elif selected == 'Ge':
            self._set_template_attributes(template=st.Ge())
        elif selected == 'GaAs':
            self._set_template_attributes(template=st.GaAs())
        elif selected == 'AlAs':
            self._set_template_attributes(template=st.AlAs())
        elif selected == 'GaP':
            self._set_template_attributes(template=st.GaP())
        elif selected == 'InP':
            self._set_template_attributes(template=st.InP())
        elif selected == 'GaSb':
            self._set_template_attributes(template=st.GaSb())
        elif selected == 'InSb':
            self._set_template_attributes(template=st.InSb())

    def draw_window(self) -> None:
        self.canvas = tk.Canvas(self.window, background='white', width=650, height=600)
        self.canvas.place(x=10, y=10)
        self.fermi_canvas = dg.FermiCanvas(canvas=self.canvas)

        font = ('Arial', 20)

        tk.Label(self.window, text='Шаблон полупроводника:', font=font).place(x=700, y=30)
        self.combobox = ttk.Combobox(self.window, values=['Si', 'Ge', 'GaAs', 'AlAs', 'GaP', 'InP', 'GaSb', 'InSb'], font=font)
        self.combobox.place(x=700, y=70)

        self.combobox.bind("<<ComboboxSelected>>", self._select_template)

        tk.Label(self.window, text='Mc/m0', font=('Arial', 18)).place(x=700, y=122)
        self.mc_entry = tk.Entry(self.window, font=font, width=5)
        self.mc_entry.place(x=780, y=120)

        tk.Label(self.window, text='Mv/m0', font=('Arial', 18)).place(x=870, y=122)
        self.mv_entry = tk.Entry(self.window, font=font, width=5)
        self.mv_entry.place(x=950, y=120)

        tk.Label(self.window, text='концентрация доноров Nd', font=font).place(x=700, y=180)
        self.nd_entry = tk.Entry(self.window, font=font)
        self.nd_entry.place(x=700, y=220)
        # tk.Spinbox(self.window, font=font).place(x=700, y=220)

        tk.Label(self.window, text='концентрация доноров Nas', font=font).place(x=700, y=280)
        self.nas_entry = tk.Entry(self.window, font=font)
        self.nas_entry.place(x=700, y=320)
        # tk.Spinbox(self.window, font=font).place(x=700, y=320)

        tk.Label(self.window, text='Eg', font=('Arial', 18)).place(x=700, y=382)  #+380
        self.eg_entry = tk.Entry(self.window, font=font, width=5)
        self.eg_entry.place(x=750, y=380)

        tk.Label(self.window, text='ε', font=('Arial', 20)).place(x=870, y=378)
        self.epsilon_entry = tk.Entry(self.window, font=font, width=5)
        self.epsilon_entry.place(x=900, y=380)

        tk.Label(self.window, text='Ed', font=('Arial', 18)).place(x=700, y=442)  # +380
        self.ed_entry = tk.Entry(self.window, font=font, width=5)
        self.ed_entry.place(x=750, y=440)

        tk.Label(self.window, text='T', font=('Arial', 18)).place(x=870, y=442)
        self.temp_entry = tk.Entry(self.window, font=font, width=5)
        self.temp_entry.place(x=900, y=440)

        tk.Label(self.window, text='Внешнее поле Eout [В/м]', font=('Arial', 18)).place(x=705, y=487)
        self.eout_entry = tk.Entry(self.window, font=font, width=20)
        self.eout_entry.place(x=700, y=525)

        tk.Button(self.window, text='Найти уровень Ферми', font=font, bg='SteelBlue1').place(x=700, y=565)




