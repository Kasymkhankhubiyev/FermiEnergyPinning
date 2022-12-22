import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import SemoconductorsTemplates as st
import DrawGraphs as dg
from project import calculations
from exceptions import CantProcessCalculations
from fompy.constants import eV

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
        self.eg_sbox, self.epsilon_sbox, self.eas_sbox = None, None, None
        self.ed_sbox, self.eout_sbox, self.temp_sbox = None, None, None
        self.field_sign = tk.IntVar()

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

        # Calculations
        try:
            data = self._calculate()
            self.fermi_canvas.draw(data)
        except CantProcessCalculations:
            pass
            # messagebox.showerror(message='Cannot process calculations for a given data')

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
        self.eout_sbox.insert(0, 1.0)

        self.fermi_canvas.draw(self._calculate())

    def _set_templetes_combobox_block(self, font_label, font_sbox) -> None:
        tk.Label(self.window, text='Полупроводник: ', font=font_label).grid(row=0, column=1, columnspan=3, sticky=tk.W)
        self.combobox = ttk.Combobox(self.window, values=['Si', 'Ge', 'GaAs', 'AlAs', 'GaP', 'InP', 'GaSb', 'InSb'],
                                     font=font_sbox, width=5)
        self.combobox.grid(row=0, column=4, sticky=tk.W + tk.E)
        self.combobox.bind("<<ComboboxSelected>>", self._select_template)

    def _set_effective_electron_mass_sbox(self, font_label, font_sbox) -> None:
        # эффективная масса плотности состояний электронов
        tk.Label(self.window, text='Mc = ', font=font_label, width=5).grid(row=1, column=1, sticky=tk.E)
        self.mc_sbox = tk.Spinbox(self.window, font=font_sbox, width=5, from_=0, to=1000, increment=0.01,
                                  command=self._sbox_handler)
        self.mc_sbox.bind("<KeyRelease>", self._sbox_handler)
        self.mc_sbox.grid(row=1, column=2, sticky=tk.W + tk.E)

    def _set_effective_hole_mass_sbox(self, font_label, font_sbox) -> None:
        # эффективная масса плотности состояний дырок
        tk.Label(self.window, text='Mv = ', font=font_label, width=5).grid(row=1, column=3, sticky=tk.E)
        self.mv_sbox = tk.Spinbox(self.window, font=font_sbox, width=5, from_=0, to=1000, increment=0.01,
                                  command=self._sbox_handler)
        self.mv_sbox.bind("<KeyRelease>", self._sbox_handler)
        self.mv_sbox.grid(row=1, column=4, sticky=tk.W + tk.E)

    def _set_donors_concentration_sbox(self, font_label, font_sbox) -> None:
        # концентрация доноров, то же самое что и N_{d0}
        tk.Label(self.window, text='Nd = ', font=font_label).grid(row=2, column=1, sticky=tk.W)
        self.nd_sbox = tk.Spinbox(self.window, font=font_sbox, width=5, from_=0, to=100, increment=0.1,
                                  command=self._sbox_handler)
        self.nd_sbox.grid(row=2, column=2, sticky=tk.W + tk.E)
        self.nd_sbox.bind("<KeyRelease>", self._sbox_handler)

        # порядок концентрации доноров
        tk.Label(self.window, text=' * 10 ^', font=font_label).grid(row=2, column=3, sticky=tk.W + tk.E)
        self.nd_pwr_sbox = tk.Spinbox(self.window, font=font_sbox, width=5, from_=0, to=100,
                                      command=self._sbox_handler)
        self.nd_pwr_sbox.grid(row=2, column=4, sticky=tk.W + tk.E)
        self.nd_pwr_sbox.bind("<KeyRelease>", self._sbox_handler)

    def _set_acceptors_concentration_sbox(self, font_label, font_sbox) -> None:
        # концентрация акцепторов N_{a}
        tk.Label(self.window, text='Nas = ', font=font_label).grid(row=3, column=1, sticky=tk.W)
        self.nas_sbox = tk.Spinbox(self.window, font=font_sbox, width=5, from_=0, to=100, increment=0.1,
                                   command=self._sbox_handler)
        self.nas_sbox.grid(row=3, column=2, sticky=tk.W + tk.E)
        self.nas_sbox.bind("<KeyRelease>", self._sbox_handler)

        # порядок концентрации акцепторов
        tk.Label(self.window, text=' * 10 ^', font=font_label).grid(row=3, column=3, sticky=tk.W + tk.E)
        self.nas_pwr_sbox = tk.Spinbox(self.window, font=font_sbox, width=5, from_=0, to=100,
                                       command=self._sbox_handler)
        self.nas_pwr_sbox.grid(row=3, column=4, sticky=tk.W + tk.E)
        self.nas_pwr_sbox.bind("<KeyRelease>", self._sbox_handler)

    def _set_energy_gap_sbox(self, font_label, font_sbox) -> None:
        # ширина запрещенной зоны E_{g} отсчитывается от потолка валентной зоны,
        # измеряется в эВ
        tk.Label(self.window, text='Eg = ', font=font_label).grid(row=4, column=1, sticky=tk.E)
        self.eg_sbox = tk.Spinbox(self.window, font=font_sbox, width=5, from_=0, to=100, increment=0.01,
                                  command=self._sbox_handler)
        self.eg_sbox.grid(row=4, column=2, sticky=tk.W + tk.E)
        self.eg_sbox.bind("<KeyRelease>", self._sbox_handler)

    def _set_epsilon_sbox(self, font_label, font_sbox) -> None:
        # диэлектрическая проницаемость полупроводника
        tk.Label(self.window, text='ε = ', font=font_label).grid(row=4, column=3, sticky=tk.E)
        self.epsilon_sbox = tk.Spinbox(self.window, font=font_sbox, width=5, from_=0, to=100, increment=0.1,
                                       command=self._sbox_handler)
        self.epsilon_sbox.grid(row=4, column=4, sticky=tk.E + tk.W)
        self.epsilon_sbox.bind("<KeyRelease>", self._sbox_handler)

    def _set_donors_energy_level_sbox(self, font_label, font_sbox) -> None:
        # уровень энергии доноров, отсчитывается от дна зоны проводимости, измеряется в эВ
        tk.Label(self.window, text='Ed = ', font=font_label).grid(row=5, column=1, sticky=tk.E)
        self.ed_sbox = tk.Spinbox(self.window, font=font_sbox, width=5, from_=0, to=100, increment=0.01,
                                  command=self._sbox_handler)
        self.ed_sbox.grid(row=5, column=2, sticky=tk.W + tk.E)
        self.ed_sbox.bind("<KeyRelease>", self._sbox_handler)

    def _set_surface_acceptors_energy_level_sbox(self, font_label, font_sbox) -> None:
        # уровень энергии доноров, отсчитывается от дна зоны проводимости, измеряется в эВ
        tk.Label(self.window, text='Eas = ', font=font_label).grid(row=6, column=1, sticky=tk.E)
        self.eas_sbox = tk.Spinbox(self.window, font=font_sbox, width=5, from_=0, to=100, increment=0.01,
                                   command=self._sbox_handler)
        self.eas_sbox.grid(row=6, column=2, sticky=tk.W + tk.E)
        self.eas_sbox.bind("<KeyRelease>", self._sbox_handler)

    def _set_temperature_sbox(self, font_label, font_sbox) -> None:
        # Температура в Кельвинах
        tk.Label(self.window, text='T = ', font=font_label).grid(row=5, column=3, sticky=tk.E)
        self.temp_sbox = tk.Spinbox(self.window, font=font_sbox, width=5, from_=0, to=math.inf,
                                    command=self._sbox_handler)
        self.temp_sbox.grid(row=5, column=4, sticky=tk.W + tk.E)
        self.temp_sbox.bind("<KeyRelease>", self._sbox_handler)

    def _set_external_field_value_sbox(self, font_label, font_sbox) -> None:
        # Величина внешнего поля
        # tk.Label(self.window, text='Внешнее поле', font=font_sbox).grid(row=10, column=1, columnspan=4, sticky=tk.W)
        tk.Label(self.window, text='Eout = ', font=font_label).grid(row=7, column=1, sticky=tk.E)
        tk.Checkbutton(self.window, text='-1 * ', variable=self.field_sign, onvalue=1, offvalue=0, \
            command=self._button_handler, font=font_label).grid(row=7, column=2, sticky='e')
        self.eout_sbox = tk.Spinbox(self.window, font=font_sbox, width=5, from_=0, to=1e10,
                                    command=self._sbox_handler, increment=0.01)
        self.eout_sbox.grid(row=7, column=3, sticky=tk.W + tk.E)
        tk.Label(self.window, text='* 10^9 V/m', font=font_label).grid(row=7, column=4, sticky=tk.W)

        # tk.Label(self.window, text='', font=font_label).grid(row=7, column=4, columnspan=4, sticky=tk.W)
        self.eout_sbox.bind("<KeyRelease>", self._sbox_handler)

    def draw_window(self) -> None:
        self.canvas = tk.Canvas(self.window, background='white')
        self.canvas.grid(row=0, column=0, rowspan=18, padx=10, pady=10, sticky="news")
        self.fermi_canvas = dg.FermiCanvas(canvas=self.canvas)

        font_label = ('Arial', 18)
        font_sbox = ('Arial', 20)

        self._set_templetes_combobox_block(font_sbox=font_sbox, font_label=font_label)
        self._set_effective_electron_mass_sbox(font_sbox=font_sbox, font_label=font_label)
        self._set_effective_hole_mass_sbox(font_sbox=font_sbox, font_label=font_label)
        self._set_donors_concentration_sbox(font_sbox=font_sbox, font_label=font_label)
        self._set_acceptors_concentration_sbox(font_sbox=font_sbox, font_label=font_label)
        self._set_energy_gap_sbox(font_sbox=font_sbox, font_label=font_label)
        self._set_epsilon_sbox(font_sbox=font_sbox, font_label=font_label)
        self._set_donors_energy_level_sbox(font_sbox=font_sbox, font_label=font_label)
        self._set_temperature_sbox(font_sbox=font_sbox, font_label=font_label)
        self._set_surface_acceptors_energy_level_sbox(font_label=font_label, font_sbox=font_sbox)
        self._set_external_field_value_sbox(font_sbox=font_sbox, font_label=font_label)

        self.calc_button = tk.Button(self.window, text='Найти уровень Ферми', font=font_sbox, bg='SteelBlue1')
        self.calc_button.grid(row=8, column=1, columnspan=4)
        self.calc_button.config(command=self._button_handler)

        self._set_default()

    def _calculate(self) -> dict:
        args = {
            "E_gap": float(self.eg_sbox.get()),  # Band gap [eV]
            "epsilon": float(self.epsilon_sbox.get()),  # Dielectric permittivity
            "m_h": float(self.mv_sbox.get()),  # Effective hole mass [m_0]
            "m_e": float(self.mc_sbox.get()),  # Effective electron mass [m_0]
            "E_d": float(self.ed_sbox.get()),  # Donors level [eV]
            "N_d0": float(self.nd_sbox.get()) * 10 **int(self.nd_pwr_sbox.get()),  # Concentration of donors [cm^(-3)]
            "E_as": float(self.eas_sbox.get()),  # Surface acceptors level [eV]
            "N_as": float(self.nas_sbox.get()) * 10**int(self.nas_pwr_sbox.get()),  # Concentration of surface acceptors [cm^(-3)]
            "T": float(self.temp_sbox.get()),  # Temperature [K]
            "E_out": float(float(self.eout_sbox.get()) * 1e9 * (-1)**self.field_sign.get())  # External electric field
        }
        print(args['E_out'])

        args['E_d'] = args['E_gap'] - args['E_d']
        data = calculations.calculate(args)
        # print(data)
        w = data['W']
        Ef = data['E_f']/eV
        phi = data['phi']

        w = float("{:.3e}".format(w))
        Ef = float("{:.3e}".format(Ef))
        phi = float("{:.3e}".format(phi))

        tk.Label(self.window, text=f"W = {w}; phi = {phi}; Ef = {Ef}", font=('Arial', 18)).grid(row=18, column=0,
                                                                                                sticky=tk.W + tk.E)

        return data

    def _button_handler(self) -> None:
        # print("Handled")
        try:
            data = self._calculate()
            self.fermi_canvas.draw(data)
        except CantProcessCalculations:
            pass
            # messagebox.showerror(message='Cannot process calculations for a given data')

    def _sbox_handler(self, event=None):
        try:
            data = self._calculate()
            self.fermi_canvas.draw(data)
        except CantProcessCalculations:
            pass
            # messagebox.showerror(message='Cannot process calculations for a given data')
