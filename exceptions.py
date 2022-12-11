class CantProcessCalculations(Exception):
    'Cannot process calculations for a given data'


class ParamsValueException(Exception):
    pass


class SurfaceStatesValueException(ParamsValueException):
    """Error! The surface states do NOT fall into the energy gap of the semiconductor"""
    def __init__(self, e_as, e_g):
        # self.e_as, self.e_g = e_as, e_g
        super().__init__(
            f'The surface states do NOT fall into the energy gap.'
            f'{e_as} > {e_g}')


class ExternalFieldValueException(ParamsValueException):
    def __init__(self, e_out, e_in):
        # self.e_out, self.e_in = e_out, e_in  # для assert
        super().__init__(
            f'The external field is larger than the field created by surface acceptors'
            f'{e_out} > {e_in}'
        )


class DonorConcentrationValueException(ParamsValueException):
    def __init__(self, nd, nc, nv):
        super().__init__(
            f'The Nd > Nc or Nd > Nv'
            f'Nd = {nd}, Nc = {nc}, Nv = {nv}'
        )


class CantCalculateWDepth(CantProcessCalculations):
    def __init__(self, mesg):
        super().__init__(
            f'Cannot solve an equation to find W'
            f'{mesg}'
        )


class CantMatchMethod(Exception):
    def __init__(self, message, methods):
        super().__init__(
            f'Cannot math a method: {message} '
            f'choose one from {methods}'
        )


class CantRunDichotomyMethod(Exception):
    def __init__(self, phi0, phi1):
        super().__init__(
            f'Cannot run the dichotomy method \t'
            f'with wrong borders: [{phi0}, {phi1}]\t'
            f'req: [a, b]: a < b'
        )


class CatchZeroDelta(Exception):
    def __init__(self, phi0, phi1):
        super().__init__(
            f'Delta cannot be equal zero'
        )
