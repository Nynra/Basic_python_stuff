# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 16:49:33 2022.

@author: baskl
"""
import numpy as np


def trap_error_array(x, y, xerr, yerr):
    """
    Calculate the most likely error and surface when is numericly integrated.

    Calculate the most likely error when the the data is numerically integrated
    using the trapezium method.

    Parameters
    ----------
    x : np.array
        1D numpy array met de data van de onafhankelijke variabele.
    y : np.array
        1D numpy array met de data van de afhankelijke variabele.
    xerr : np.array
        1D numpy array met de fout van elke waarde in x.
    yerr : np.array
        1D numpy array met de fout van elke waatde in y.

    Returns
    -------
    opp : np.array
        The numerically integrated data.
    dopp : np.array
        The error of the integrated data.

    """
    # Check if the arrays have the same lenght
    if not (len(x) == len(y) and len(x) == len(xerr) and len(x) == len(yerr)):
        print('Niet alle input arrays hebben dezelfde lengte dus de integraal'
              ' en de fout kunnen niet berekend worden.')
        return

    # Define the output lists
    opp = [0]
    dopp = [0]

    for i in range(len(x) - 1):
        # Calculate the sub-areas
        xi = x[i + 1] - x[i]
        yi = 0.5 * (abs(y[i]) + abs(y[i + 1]))
        opp.append(opp[-1] + xi * yi)

        # Calculate the error in the sub-areas
        dyi = 0.5 * np.sqrt(yerr[i]**2 + yerr[i + 1]**2)
        dxi = np.sqrt(xerr[i + 1]**2 + xerr[i]**2)

        # Calculate the error in the total area
        doppi = abs(xi * yi) * np.sqrt((dyi / yi)**2 + (dxi / xi)**2)
        dopp.append(doppi + dopp[-1])

    return opp, dopp
