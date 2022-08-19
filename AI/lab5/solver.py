# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!

"""

from table import Table as tb


def getValues(x, key, value_type):
    if value_type == tb.THETA:
        l, mid, r = tb.theta_ranges[key]
    elif value_type == tb.OMEGA:
        l, mid, r = tb.omega_ranges[key]
    else:
        return None

    if l is not None and l <= x < mid:
        return (x - l) / (mid - l)
    elif r is not None and mid <= x < r:
        return (r - x) / (r - mid)
    elif l is None and x <= mid:
        return 1
    elif r is None and x >= mid:
        return 1
    else:
        return 0


def solver(t, w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or
    
    None :if we have a division by zero

    """

    theta_values = {}
    for key in tb.theta_ranges:
        theta_values[key] = getValues(t, key, tb.THETA)

    omega_values = {}
    for key in tb.omega_ranges:
        omega_values[key] = getValues(w, key, tb.OMEGA)

    f_values = {}
    for theta_key in tb.fuzzy_table:
        for omega_key, f_value in tb.fuzzy_table[theta_key].items():
            value = min(theta_values[theta_key], omega_values[omega_key])

            if f_value not in f_values:
                f_values[f_value] = value
            else:
                f_values[f_value] = max(value, f_values[f_value])

    s, sum = 0, 0
    for f_value in f_values.values():
        s += f_value
    for key in f_values.keys():
        sum = f_values[key] * tb.bValues[key]

    if s == 0:  # Division by 0
        return None

    return sum / s
