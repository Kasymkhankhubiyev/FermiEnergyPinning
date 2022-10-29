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

