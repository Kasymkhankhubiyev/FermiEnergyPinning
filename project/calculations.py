import numpy as np
from fompy import constants, materials, models
from scipy.optimize import fsolve
from exceptions import SurfaceStatesValueException, ExternalFieldValueException, DonorConcentrationValueException
from exceptions import CantProcessCalculations, CantCalculateWDepth
from tkinter import messagebox

from FermiLevel.DonorFermiLevel import find_fermi_level


def _check_parameters(parameters, Nc, Nv):
    # message = 'ok'

    if parameters['E_as'] > parameters['E_gap']:
        raise SurfaceStatesValueException(e_as=parameters['E_as'], e_g=parameters['E_gap'])
    if parameters['E_out'] * 3.3 * 1e-5 > parameters['N_as'] * constants.e:
        raise ExternalFieldValueException(e_out=parameters['E_out'] * 3.3 * 1e-5, e_in=parameters['N_as'] * constants.e)
    if parameters['N_d0'] > Nc or parameters['N_d0'] > Nv:
        raise DonorConcentrationValueException(nd=parameters['N_d0'], nc=Nc, nv=Nv)
    # return message


def _equation_for_phi_left(x, parameters):
    x_erg = x * constants.eV
    return np.sqrt(parameters['epsilon'] * x_erg * parameters['N_d0'] / (2 * np.pi * pow(constants.e, 2)))


def _equation_for_phi_right(x, parameters):
    x_erg = x * constants.eV
    return (parameters['N_as'] * (1 / (1 + np.exp((parameters['E_as'] + x_erg - parameters['E_f'])
            / (constants.k * parameters['T'])))) + parameters['E_out'] / (4 * np.pi * constants.e))


def _equation_for_phi(x, parameters):
    return _equation_for_phi_left(x, parameters) - _equation_for_phi_right(x, parameters)


def W(phi, parameters):
    phi_erg = phi * constants.eV
    return np.sqrt(parameters['epsilon'] * phi_erg / (parameters['N_d0'] * 2 * np.pi * pow(constants.e, 2)))


def w_width(delta_phi: float, epsilon: float, nd: float) -> float:
    return np.sqrt(delta_phi * 1.6e-19 * 2 * 8.8e-14 * epsilon / (1.6e-19**2 * nd))


def solve_equation_find_phi(parameters):
    x_0 = 0.001
    phi, infodict, iter, mesg = fsolve(_equation_for_phi, x_0, args=parameters, full_output=True)
    if iter != 1:
        raise CantCalculateWDepth(mesg=mesg)
    return phi[0]


def data_for_graph(phi, W, parameters):  # phi [eV], W [cm]
    N = 30  # knot number
    h = 1e-5 * 2 / N
    if W != 0:
        h = W * 2 / N  # step

    a, b, c = None, None, None
    if W != 0:
        # parabola: ax ^ 2 + bx + c
        c = phi
        a = c / (W ** 2)
        b = -2 * W * a

    x_s = []  # Coordinate
    E_f_s = []  # Fermi energy
    E_v_s = []  # Valence band ceiling
    E_c_s = []  # Conduction band bottom
    E_d_s = []  # Donor energy
    E_as_s = []  # Energy of surface acceptors

    E_f = parameters['E_f'] / constants.eV
    E_gap = parameters['E_gap'] / constants.eV
    E_d = parameters['E_d'] / constants.eV
    E_as = parameters['E_as'] / constants.eV

    for i in range(N + 1):
        x_s.append(i * h)
        E_f_s.append(E_f)

        if W != 0:
            E_as_s.append(E_as+c)

            if np.sign(parameters['E_out']) < 0 and parameters['N_as'] == 0:
                if x_s[i] > W:  # flat zone
                    E_v_s.append(0)
                    E_c_s.append(E_gap)
                    E_d_s.append(E_d)

                else:  # zone with parabola: flat + parabola bend
                    bend = np.sign(parameters['E_out']) * (a * x_s[i] ** 2 + b * x_s[i] + c)
                    E_v_s.append(bend)
                    E_c_s.append(E_gap + bend)
                    E_d_s.append(E_d + bend)
            else:
                if x_s[i] > W:  # flat zone
                    E_v_s.append(0)
                    E_c_s.append(E_gap)
                    E_d_s.append(E_d)

                else:  # zone with parabola: flat + parabola bend
                    bend = a * x_s[i] ** 2 + b * x_s[i] + c
                    E_v_s.append(bend)
                    E_c_s.append(E_gap + bend)
                    E_d_s.append(E_d + bend)
        elif W == 0:
            E_as_s.append(E_as)

            E_v_s.append(0)
            E_c_s.append(E_gap)
            E_d_s.append(E_d)

    return x_s, E_f_s, E_v_s, E_c_s, E_d_s, E_as_s


def calc_phi_without_nas(parameters):
    print(np.sign(parameters['E_out']))
    return (parameters['E_out'] / 3.3e-5 / 1e2 / (4 * np.pi * 1.6e-19))**2 * (2 * np.pi * 1.6e-19**2 * 8.8e-14) / parameters['epsilon'] / parameters['N_d0'] * 1e19


def calculate(parameters) -> dict:
    semiconductor = models.Semiconductor(parameters['m_e'] * constants.me, parameters['m_h'] * constants.me,
                                         parameters['E_gap'] * constants.eV, eps=parameters['epsilon'], chi=None)
    pin_fermi = models.DopedSemiconductor(mat=semiconductor, Na=0, Nd=parameters['N_d0'], Ea=0, Ed=parameters['E_d']*constants.eV)
    T = parameters['T']
    try:
        # _check_parameters(parameters, semiconductor.Nc(T), semiconductor.Nv(T))
        results = dict(message='ok', x_s=0., E_f_s=0., E_v_s=0., E_c_s=0., E_d_s=0., E_as_s=0., phi=0., W=0.)

        # ??????
        parameters['E_gap'] = parameters['E_gap'] * constants.eV
        parameters['E_d'] = parameters['E_d'] * constants.eV
        parameters['E_as'] = parameters['E_as'] * constants.eV
        parameters['E_out'] = parameters['E_out'] * 3.3e-5  # 1 V/m = 3.3e-5 ????????-???? ????????????

        try:
            # parameters['E_f'] = find_fermi_level(me=parameters['m_e'], mh=parameters['m_h'],
            #                                      t=parameters['T'],
            #                                      Jd=(parameters['E_gap'] - parameters['E_d']) / constants.eV,
            #                                      Efpl=parameters['E_gap'] / constants.eV / 2,
            #                                      Efneg=parameters['E_gap'] / constants.eV,
            #                                      Ec=parameters['E_gap'] / constants.eV, Ev=0, Nd=parameters['N_d0'])
            # print(parameters['E_f'])
            # parameters['E_f'] *= constants.eV
            parameters['E_f'] = pin_fermi.fermi_level(T)
            results['E_f'] = parameters['E_f']
            if parameters['N_as'] != 0:
                results['phi'] = solve_equation_find_phi(parameters)  # eV
            elif parameters['N_as'] == 0:
                results['phi'] = calc_phi_without_nas(parameters)
            results['W'] = w_width(delta_phi=results['phi'], epsilon=parameters['epsilon'], nd=parameters['N_d0']) # W(results['phi'], parameters)  # cm
            print(f"width W:  {results['W']}")
            results['x_s'], results['E_f_s'], results['E_v_s'], results['E_c_s'], results['E_d_s'], \
                results['E_as_s'] = data_for_graph(results['phi'], results['W'], parameters)
            return results
        except Exception:
            raise Exception
    except SurfaceStatesValueException as e:
        messagebox.showerror(title='Error...', message=f'{e.args}')
        raise CantProcessCalculations
    except DonorConcentrationValueException as e:
        messagebox.showerror(title='Error...', message=f'{e.args}')
        raise CantProcessCalculations
    except ExternalFieldValueException as e:
        messagebox.showerror(title='Error...', message=f'{e.args}')
        raise CantProcessCalculations
    except CantCalculateWDepth as e:
        messagebox.showerror(title='Error...', message=f'{e.args}')
