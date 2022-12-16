import numpy as np

me_effective = float
mh_effective = float
Kelvin = float
Nc = float
Nd = float
eV = float


def count_Q(n: float, p: float, Nd=None, Na=None) -> float:
    """
    :param n: кол-во негативных носителей
    :param p: кол-во положительных носителей
    :param Nd: кол-во ионизированных атомов
    :return: Q - заряд полупроводника
    """

    if Nd is not None:
        return n - p - Nd
    if Na is not None:
        return n + Na - p


def calc_n(nc: float, Ef: float, Ec: float, t: Kelvin) -> float:  # Nparticle:
    """
    n = Nc * exp(- (Ec - Ef)/kT)
    """
    k = 1.38e-16  # эрг/К

    expl = np.exp((Ef - Ec)/(k * 6.24e11 * t))
    n = nc * expl
    return n


def calc_p(nv: float, Ef: float, Ev: float, t: Kelvin) -> float:  # Nparticle:
    """
    p = Nv * exp((Ev - Ef)/kT)
    """
    k = 1.38e-16  # эрг/К

    expl = np.exp((Ev - Ef) / (k * 6.24e11 * t))
    p = nv * expl
    return p


def calc_Ndplus(Nd: float, Eg: float, Ef: eV, Ed: eV, t: Kelvin):
    k = 1.38e-16  # эрг/К

    ndpl = Nd / (1. + np.exp((Eg - Ef - Ed) / (k * 6.24e11 * t)))
    return ndpl


def calc_Naneg(Na: float, Ef: eV, Ea: eV, t: Kelvin):
    k = 1.38e-16  # эрг/К
    naneg = Na / (1. + .25 * np.exp((Ea - Ef)/(k * 6.24e11 * t)))
    return np.abs(naneg)


def calc_Nc(me: me_effective, t: Kelvin) -> float:  # Nparticle:
    """
    :math: $N_c=2(\frac{2\pi m_ckT}{h^2}^{3/2})$
    :param me: effective mass of electron
    :param t: temperature in Kelvin
    :return: electrons concentration 1/cm^3
    """
    k = 1.38e-023  # J/K
    h = 1.054e-034  # J*sec ~~ kg * m / sec
    m0 = 9.109e-031  # kg ~ 0.511MeV

    Nc = 2 * ((2 * np.pi * me * m0 * k * t) / (h ** 2)) ** 1.5  # 1/m^3
    Nc /= 10**6  # 1/cm^3
    return Nc


def calc_Nv(mh: mh_effective, t: Kelvin) -> float:  # Nparticle:
    """
    :math: $N_v=2(\frac{2\pi m_ckT}{h^2}^{3/2})$
    :param me: effective mass of electron
    :param t: temperature in Kelvin
    :return: protons concentration 1/cm^3
    """
    k = 1.38e-023  # J/K
    h = 1.054e-034  # kg * m /sec^2
    m0 = 9.109e-031  # kg ~ 0.511MeV

    Nv = 2 * ((2 * np.pi * mh * m0 * k * t) / (h ** 2)) ** 1.5  # 1/m^3
    Nv /= 10 ** 6  # 1/cm^3
    return Nv


def convert_charges(charge: float) -> str:
    factor = round(np.log10(charge))
    body = charge / 10 ** factor
    return '{:.2f}'.format(body)+f'e{factor}'


def count_nc_nv(m_eff: float, t: float) -> float:
    return 2.51e19 * m_eff**1.5 * (t/300)**1.5
