"""
mc - эффективная масса плотности состояний в долинах для электронов [эВ]
mv - эффективная масса плотности состояний в долинах для дырок [эВ]
Eg - ширина запрещенной зоны [эВ]
epsilon - ε диэлектрическая постоянная
lattice - постоянная решетки

"""


class Si:
    def __init__(self) -> None:
        self.mc = 0.36
        self.mv = 0.81
        self.Eg = 1.12
        self.epsilon = 11.7
        self.lattice = 5.431e-8


class Ge:
    def __init__(self) -> None:
        self.mc = 0.36
        self.mv = 0.81
        self.Eg = 0.65
        self.epsilon = 16.2
        self.lattice = 5.658e-8


class GaAs:
    def __init__(self) -> None:
        self.mc = 0.36
        self.mv = 0.81
        self.Eg = 4.97
        self.epsilon = 10.9
        self.lattice = 5.65e-8


class AlAs:
    def __init__(self) -> None:
        self.mc = 0.36
        self.mv = 0.81
        self.Eg = 5.82
        self.epsilon = 8.16
        self.lattice = 5.66e-8


class GaP:
    def __init__(self) -> None:
        self.mc = 0.36
        self.mv = 0.81
        self.Eg = 2.26
        self.epsilon = 11.1
        self.lattice = 5.4505e-8


class InP:
    def __init__(self) -> None:
        self.mc = 0.36
        self.mv = 0.81
        self.Eg = 1.344
        self.epsilon = 12.5
        self.lattice = 5.8687e-8


class GaSb:
    def __init__(self) -> None:
        self.mc = 0.36
        self.mv = 0.81
        self.Eg = 0.726
        self.epsilon = 15.7
        self.lattice = 6.09e-8


class InSb:
    def __init__(self) -> None:
        self.mc = 0.36
        self.mv = 0.81
        self.Eg = 0.726
        self.epsilon = 16.8
        self.lattice = 6.479e-8