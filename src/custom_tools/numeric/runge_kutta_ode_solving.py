# -*- coding: utf-8 -*-
"""
Created on Sun May 29 13:19:52 2022.

@author: baskl
"""
import numpy as np


def euler(x, f, f0):
    """
    Use the Euler solving method.

    Just a wrapper for the first order Runge Kutta method.
    """
    return first_order_runge_kutta(x, f, f0)


def first_order_runge_kutta(t, f, f0):
    """
    Calculate firs order runge kutta estimation of the given fuinction.

    Parameters
    ----------
    t : np.array
        Numpy array containing the timestamp in float.
    f : function object
        Function object representing the equation that shoult be solved.
    f0 : floar
        The initial condition of the given function.

    Returns
    -------
    xpoints : np.array
        Numpy array containing the numeric data representing the solved
        equation.
    """
    # Initial parameters
    a = t[0]
    b = t[-1]
    N = len(t)
    h = (b - a) / N
    x = f0

    xpoints = []
    for ti in t:
        xpoints.append(x)
        x += h * f(x, ti)

    return xpoints


def second_order_runge_kutta(t, f, f0):
    """
    Calculate second order runge kutta estimation of the given fuinction.

    Parameters
    ----------
    t : np.array
        Numpy array containing the timestamp in float.
    f : function object
        Function object representing the equation that shoult be solved.
    f0 : floar
        The initial condition of the given function.

    Returns
    -------
    xpoints : np.array
        Numpy array containing the numeric data representing the solved
        equation.
    """
    # Initial parameters
    a = t[0]
    b = t[-1]
    N = len(t)
    h = (b - a) / N
    x = f0

    xpoints = []
    for ti in t:
        xpoints.append(x)
        k1 = h * f(x, ti)
        k2 = h * f(x + 0.5 * k1, ti + 0.5 * h)
        x += k2

    return xpoints


def fourth_order_runge_kutta(t, f, f0):
    """
    Calculate fourth order runge kutta estimation of the given fuinction.

    Parameters
    ----------
    t : np.array
        Numpy array containing the timestamp in float.
    f : function object
        Function object representing the equation that shoult be solved.
    f0 : floar
        The initial condition of the given function.

    Returns
    -------
    xpoints : np.array
        Numpy array containing the numeric data representing the solved
        equation.
    """
    # Initial parameters
    a = t[0]
    b = t[-1]
    N = len(t)
    h = (b - a) / N
    x = f0

    xpoints = []
    for ti in t:
        xpoints.append(x)
        k1 = h * f(x, ti)
        k2 = h * f(x + 0.5 * k1, ti + 0.5 * h)
        k3 = h * f(x + 0.5 * k2, ti + 0.5 * h)
        k4 = h * f(x + k3, ti + h)
        x += (k1 + 2 * k2 + 2 * k3 + k4) / 6

    return xpoints


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # Example function
    def f(x, t): return -x**3 + np.sin(t)

    # Example estimation
    x = np.linspace(0, 100, 10000)
    y = second_order_runge_kutta(x, f)
    plt.plot(x, y)
    plt.grid(True)
    plt.show()
