import numpy as np
from typing import NamedTuple

me_effective = float
mh_effective = float
Kelvin = float
eV = float


def _calcNc() -> float:
    pass


def _calc_Nc(me: me_effective, t: Kelvin) -> float:  # Nparticle:
    k = 1.38 * 10**-23  # J/K
    h = 1.054 * 10**-34  # kg * m /sec^2
    m0 = 9.109 * 10**-31  # kg ~ 0.511MeV

    Nc = 2.51e19 * me**1.5 * (t/300.)**1.5

    # Nc /= 10**6  # 1/cm^3

    return Nc


def _calc_Nv(mh: mh_effective, t: Kelvin) -> float:  # Nparticle:
    k = 1.38 * 10 ** -23  # J/K
    h = 1.054 * 10 ** -34  # kg * m /sec^2
    m0 = 9.109 * 10 ** -31  # kg ~ 0.511MeV

    Nv = 2 * ((2 * np.pi * mh * m0 * k * t)/((2 * np.pi * h)**2)) ** 1.5  # 1/m^3

    Nv /= 10 ** 6  # 1/cm^3

    return Nv


def _calc_Ndplus(Nd: float, myu: eV, Ed: eV, Eg: eV, t: Kelvin):
    k = 1.38e-16  # эрг/К

    ndpl = Nd / (1. + np.exp((Eg - Ed - myu)/(k * 6.24e11 * t)))

    return ndpl


def calc_Naspl(Nas: float, myu: float, phi: float, Eas: eV, t: Kelvin):
    k = 1.38e-16  # эрг/К

    naspl = Nas / (1. + np.exp((Eas + phi - myu)/(k * 6.24e11 * t)))

    return naspl


def calc_n(myu: eV, Eg: eV, nc: float, t: Kelvin) -> float:
    k = 1.38e-16  # эрг/К

    n = nc * np.exp((myu - Eg) / (k * 6.24e11 * t))
    return n


def calc_p(myu: eV, nv: float, t: Kelvin) -> float:
    k = 1.38e-16  # эрг/К

    p = nv * np.exp(-1. * myu/(k * 6.24e11 * t))
    return p
