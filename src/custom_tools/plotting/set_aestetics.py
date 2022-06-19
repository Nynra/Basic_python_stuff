# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 18:04:13 2021.

@author: Nynra
"""
import matplotlib.pyplot as plt
import locale
import seaborn as sns


def set_aestetics(theme='whitegrid', use_tex=True):
    """
    Set the graph aestetics to fancy.

    Parameters
    ----------
    theme : str, optional
        Theme that is set for seaborn. The default is 'whitegrid'.
    use_tex : bool, optional
        Boolean indicating if the system latex should be
        used (True) or the matplotlib version (False). The default is True.

    Returns
    -------
    None.

    """
    # Set the general graph parameters
    # Set comma for decimals
    locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')
    plt.rcParams['axes.formatter.use_locale'] = True
    sns.set(rc={'text.usetex': use_tex})  # Turn on the LaTeX interpreter
    sns.set_style(theme)  # Set the graph grid to white
