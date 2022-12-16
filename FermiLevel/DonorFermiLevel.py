"""
В данной программе производим рассчет
заряженных частицы в полупроводнике.
Точнее считаем Nd-, p, n, Q

Пусть ширина запрещенной зоны Eg = 1.12eV
Jd = Ec - Eg = 50 meV

1) Уравнение электронейтральности:
    n + Nd-= p

2) Ef - уровень Ферми, Ec - дно зоны проводимости,
Ev - потолок валентной зоны
    n = Nc * exp(- (Ec - Ef)/kT )
    p = Nv * exp(- (Ef - Ev)/kT )

    Получаем Nd- = Nd/ (1 + 4 * exp((Ef - Eg)/kT ))

 Q = Nd- + n - p --> заряд в материале
I. Предположим, что Nd- = 0 -> полупроводник собственный:
    Ef+ = (Ec + Ev)/2 + 3/4 * kT * ln(me*/mh*)

II. Уровень Ферми совпадает с границей зоны проводимости при
Nd=10^17 -> статистика не вырожденная:
    Nc(Si, T=300K) ~ 10^19
Т.о. на втором участке заряд гарантировано отрицательный,
    Ef1 = (Ef+ - Ef-)/2
"""
from FermiLevel.CalculateParticles import *

me_effective = float
mh_effective = float
Kelvin = float
Nc = float
Nd = float
eV = float

def balance_func(n: float, p: float, nd_plus: float) -> float:
    return n - p - nd_plus


def find_fermi_level(me: me_effective, mh: mh_effective, t: Kelvin, Jd: eV, Efpl: eV, Efneg: eV, Ec: eV,
                     Ev: eV, Nd: float) -> float:
    """
    Расчет делаем методом дихотомии

    :param me: эффективная масса плотности состояний электронов
    :param mh: эффективная масса плотности состояний дырок
    :param t: температура
    :param Efpl: уровень Ферми совпадает с дном зоны проводимости,
    все электроны в зоне проводимости, а дырки в валентной
    :param Efng: уровень Ферми близок к потолку валентной зоны
    :return:
    """

    # nc = calc_Nc(me, t)
    # nv = calc_Nv(mh, t)

    nc = count_nc_nv(m_eff=me, t=t)
    nv = count_nc_nv(m_eff=mh, t=t)

    a, b = Efpl, Efneg

    Ef = (a + b) / 2.

    n = calc_n(nc=nc, Ef=Ef, Ec=Ec, t=t)
    p = calc_p(nv=nv, Ef=Ef, Ev=Ev, t=t)
    ndpl = calc_Ndplus(Nd=Nd, Eg=Ec, Ef=Ef, Ed=Ec - Jd, t=t)
    q = count_Q(n=n, p=p, Nd=ndpl)

    if np.abs(q/(p + ndpl)) < 1e-12:
    # if np.abs(balance_func(n=n, p=p, nd_plus= ndpl)) < 1e-12:
        return Ef
    else:
        if q > 0:
            return find_fermi_level(me=me, mh=mh, t=t, Jd=Jd, Ec=Ec, Ev=Ev, Nd=Nd, Efneg=Ef, Efpl=Efpl)
        elif q < 0:
            return find_fermi_level(me=me, mh=mh, t=t, Jd=Jd, Ec=Ec, Ev=Ev, Nd=Nd, Efneg=Efneg, Efpl=Ef)
