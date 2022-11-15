import math
import tkinter as tk
from tkinter import ttk
import SemoconductorsTemplates as st
import DrawGraphs as dg

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import numpy as np


class MainWindow:

    def __init__(self, window: tk.Tk) -> None:
        self.window = window
        self.canvas, self.fermi_canvas, self.combobox = None, None, None

        self.mc_sbox, self.mv_sbox = None, None
        self.nd_sbox, self.nd_pwr_sbox = None, None
        self.nas_sbox, self.nas_pwr_sbox = None, None
        self.eg_sbox, self.epsilon_sbox = None, None
        self.ed_sbox, self.eout_sbox, self.temp_sbox = None, None, None

        self.calc_button = None

    def _clear_entry(self, entry: tk.Entry) -> None:
        entry.delete(0, tk.END)

    def _set_template_attributes(self, template) -> None:
        self._clear_entry(entry=self.mc_sbox)
        self.mc_sbox.insert(0, template.mc)

        self._clear_entry(entry=self.mv_sbox)
        self.mv_sbox.insert(0, template.mv)

        self._clear_entry(entry=self.eg_sbox)
        self.eg_sbox.insert(0, template.Eg)

        self._clear_entry(entry=self.epsilon_sbox)
        self.epsilon_sbox.insert(0, template.epsilon)

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

    def _set_default(self) -> None:
        self.combobox.current(0)  # Default value
        self._set_template_attributes(template=st.Si())

        self._clear_entry(entry=self.nd_sbox)
        self.nd_sbox.insert(0, 1)

        self._clear_entry(entry=self.nd_pwr_sbox)
        self.nd_pwr_sbox.insert(0, 17)

        self._clear_entry(entry=self.nas_sbox)
        self.nas_sbox.insert(0, 1)

        self._clear_entry(entry=self.nas_pwr_sbox)
        self.nas_pwr_sbox.insert(0, 18)

        self._clear_entry(entry=self.ed_sbox)
        self.ed_sbox.insert(0, 0.01)

        self._clear_entry(entry=self.temp_sbox)
        self.temp_sbox.insert(0, 300)

        self._clear_entry(entry=self.eout_sbox)
        self.eout_sbox.insert(0, 1000)

        self.fermi_canvas.draw(self.calculate())

    def draw_window(self) -> None:
        # Надо будет поставить более-менее адекватные пределы и размеры шага

        self.canvas = tk.Canvas(self.window, background='white', width=650, height=600)
        self.canvas.grid(row=0, column=0, rowspan=12, padx=10, pady=10)
        self.fermi_canvas = dg.FermiCanvas(canvas=self.canvas)

        font = ('Arial', 20)

        tk.Label(self.window, text='Полупроводник: ', font=font).grid(row=1, column=1, columnspan=3, sticky=tk.W)
        self.combobox = ttk.Combobox(self.window, values=['Si', 'Ge', 'GaAs', 'AlAs', 'GaP', 'InP', 'GaSb', 'InSb'],
                                     font=font, width=5)
        self.combobox.grid(row=1, column=4, sticky=tk.W + tk.E)
        self.combobox.bind("<<ComboboxSelected>>", self._select_template)

        tk.Label(self.window, text='Mc = ', font=('Arial', 18), width=5).grid(row=2, column=1, sticky=tk.E)
        self.mc_sbox = tk.Spinbox(self.window, font=font, width=5, from_=0, to=1000, increment=0.01,
                                  command=self.sbox_handler)
        self.mc_sbox.bind("<KeyRelease>", self.sbox_handler)
        self.mc_sbox.grid(row=2, column=2, sticky=tk.W + tk.E)

        tk.Label(self.window, text='Mv = ', font=('Arial', 18), width=5).grid(row=2, column=3, sticky=tk.E)
        self.mv_sbox = tk.Spinbox(self.window, font=font, width=5, from_=0, to=1000, increment=0.01,
                                  command=self.sbox_handler)
        self.mv_sbox.bind("<KeyRelease>", self.sbox_handler)
        self.mv_sbox.grid(row=2, column=4, sticky=tk.W + tk.E)

        tk.Label(self.window, text='Концентрация доноров Nd', font=font).grid(row=3, column=1, columnspan=4,
                                                                              sticky=tk.W)
        self.nd_sbox = tk.Spinbox(self.window, font=font, width=5, from_=0, to=100, increment=0.1,
                                  command=self.sbox_handler)
        self.nd_sbox.grid(row=4, column=2, sticky=tk.W + tk.E)
        self.nd_sbox.bind("<KeyRelease>", self.sbox_handler)

        tk.Label(self.window, text=' * 10 ^', font=font).grid(row=4, column=3, sticky=tk.W + tk.E)
        self.nd_pwr_sbox = tk.Spinbox(self.window, font=font, width=5, from_=0, to=100,
                                      command=self.sbox_handler)
        self.nd_pwr_sbox.grid(row=4, column=4, sticky=tk.W + tk.E)
        self.nd_pwr_sbox.bind("<KeyRelease>", self.sbox_handler)

        tk.Label(self.window, text='Концентрация акцепторов Nas', font=font).grid(row=5, column=1, columnspan=4,
                                                                                  sticky=tk.W)
        self.nas_sbox = tk.Spinbox(self.window, font=font, width=5, from_=0, to=100, increment=0.1,
                                   command=self.sbox_handler)
        self.nas_sbox.grid(row=6, column=2, sticky=tk.W + tk.E)
        self.nas_sbox.bind("<KeyRelease>", self.sbox_handler)

        tk.Label(self.window, text=' * 10 ^', font=font).grid(row=6, column=3, sticky=tk.W + tk.E)
        self.nas_pwr_sbox = tk.Spinbox(self.window, font=font, width=5, from_=0, to=100,
                                       command=self.sbox_handler)
        self.nas_pwr_sbox.grid(row=6, column=4, sticky=tk.W + tk.E)
        self.nas_pwr_sbox.bind("<KeyRelease>", self.sbox_handler)

        tk.Label(self.window, text='Eg = ', font=('Arial', 18)).grid(row=7, column=1, sticky=tk.E)
        self.eg_sbox = tk.Spinbox(self.window, font=font, width=5, from_=0, to=100, increment=0.01,
                                  command=self.sbox_handler)
        self.eg_sbox.grid(row=7, column=2, sticky=tk.W + tk.E)
        self.eg_sbox.bind("<KeyRelease>", self.sbox_handler)

        tk.Label(self.window, text='ε = ', font=('Arial', 20)).grid(row=7, column=3, sticky=tk.E)
        self.epsilon_sbox = tk.Spinbox(self.window, font=font, width=5, from_=0, to=100, increment=0.1,
                                       command=self.sbox_handler)
        self.epsilon_sbox.grid(row=7, column=4, sticky=tk.E + tk.W)
        self.epsilon_sbox.bind("<KeyRelease>", self.sbox_handler)

        tk.Label(self.window, text='Ed = ', font=('Arial', 18)).grid(row=8, column=1, sticky=tk.E)
        self.ed_sbox = tk.Spinbox(self.window, font=font, width=5, from_=0, to=100, increment=0.01,
                                  command=self.sbox_handler)
        self.ed_sbox.grid(row=8, column=2, sticky=tk.W + tk.E)
        self.ed_sbox.bind("<KeyRelease>", self.sbox_handler)

        tk.Label(self.window, text='T = ', font=('Arial', 18)).grid(row=8, column=3, sticky=tk.E)
        self.temp_sbox = tk.Spinbox(self.window, font=font, width=5, from_=0, to=math.inf,
                                    command=self.sbox_handler)
        self.temp_sbox.grid(row=8, column=4, sticky=tk.W + tk.E)
        self.temp_sbox.bind("<KeyRelease>", self.sbox_handler)

        tk.Label(self.window, text='Внешнее поле', font=font).grid(row=9, column=1, columnspan=4, sticky=tk.W)
        tk.Label(self.window, text='Eout = ', font=('Arial', 18)).grid(row=10, column=3, sticky=tk.E)
        self.eout_sbox = tk.Spinbox(self.window, font=font, width=5, from_=0, to=float(math.inf),
                                    command=self.sbox_handler)
        self.eout_sbox.grid(row=10, column=4, sticky=tk.W + tk.E)
        self.eout_sbox.bind("<KeyRelease>", self.sbox_handler)

        self.calc_button = tk.Button(self.window, text='Найти уровень Ферми', font=font, bg='SteelBlue1')
        self.calc_button.grid(row=11, column=1, columnspan=4)
        self.calc_button.config(command=self.button_handler)

        self._set_default()

    # Два разных хендлера, мб пригодитя по-отдельности использовать
    def button_handler(self) -> None:
        self.fermi_canvas.draw(self.calculate())

    def sbox_handler(self, event=None):
        self.fermi_canvas.draw(self.calculate())

    def calculate(self) -> dict:
        # Сюда надо будет запихать кусок, который считает и пакует всё в dict
        x = np.arange(0, 5, step=0.1)  # Just for test
        exps = np.exp(x)

        data = {'x': x,
                'Ec': exps,
                'Ef': (exps + 1.0),
                'Ea': (exps + 5.0),
                'Ed': (exps + 10.0),
                'Ev': 10 * x ** 2,
                'W': 1,
                'phi': 0}

        return data
