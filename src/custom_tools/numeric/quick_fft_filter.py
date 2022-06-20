# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 14:42:15 2021.

@author: Nynra & Wolf de Kwant
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy
from custom_tools.plotting import fft_filter_plot, set_aestetics


def fft_filter(col, samplerate, PSD_cutoff=None, f_high_cutoff=None,
               f_low_cutoff=None, f_cutoff_bands=[]):
    """
    Use an FFT filter to filter out some noise.

    Parameters
    ----------
    col : np.array or pd.Series
        Array containing the data that should be filtered.
    samplerate : int
        The used samplerate in Hz.
    PSD_cutoff : int, optional
        The amplitude at wich a frequency should be filtered out. The default
        is None.
    f_high_cutoff : [(int, int)], optional
        List containing the frequency bands that should be filtered out.
        The default is None.
    f_low_cutoff : int, optional
        Frequency below wich everything will be filtered out. The default
        is None.
    f_cutoff_bands : int, optional
        Frequency above wich everything will be filtered out. The default
        is None.

    Returns
    -------
    ffilt : np.array
        Array containing the filtered data.
    L : TYPE
        DESCRIPTION.
    freq : TYPE
        DESCRIPTION.
    PSD : np.array
        1D np.array containing the original amplitude spectrum.
    PSDclean : np.array
        1D np.array containing the filtered amplitude spectrum.

    """
    # Compute the FFT
    dt = 1 / samplerate
    n = len(col)
    fhat = np.fft.fft(col, n)  # Compute the FFT

    # Compute power density spectrum (amplitude)
    PSD = fhat * np.conj(fhat) / n
    PSDclean = copy.deepcopy(PSD)
    freq = (1 / (dt * n)) * np.arange(n)  # Create the x axis
    L = np.arange(1, np.floor(n / 2), dtype='int')  # Only plot first half

    # Use PSD to filter out noise
    if not(type(PSD_cutoff) is type(None)):
        indices = PSD > PSD_cutoff  # Find all the freqs with large power
        PSDclean = PSD * indices  # Zero out all the options
        fhat = indices * fhat  # Zero out the small fourier coefficients

    # Apply the frequency and band filters
    if not(type(f_low_cutoff) is type(None)):
        cut_off = int(f_low_cutoff * len(fhat) * dt / 2)  # Calc cut off index
        fhat[:cut_off] = 0
        PSDclean[:cut_off] = 0
    if not(type(f_high_cutoff) is type(None)):
        cut_off = int(f_high_cutoff * len(fhat) * dt / 2)  # Calc cut off index
        fhat[cut_off:] = 0
        PSDclean[cut_off:] = 0
    for band in f_cutoff_bands:
        lc = int(band[0] * len(fhat) * dt / 2)  # Calc cut off index
        hc = int(band[1] * len(fhat) * dt / 2)  # Calc cut off index
        fhat[lc:hc] = 0
        PSDclean[lc:hc] = 0

    ffilt = np.fft.ifft(fhat)  # Inverse FFT filtered time signal

    return ffilt, L, freq, PSD, PSDclean


def quick_process(df, samplerate, timestamp='Time (s)', data_col='Sensor (V)',
                  PSD_cutoff=None, f_high_cutoff=None, f_low_cutoff=None,
                  f_cutoff_bands=[], fancy_pants=False):
    """Calculate some things about the data."""
    if fancy_pants:
        set_aestetics()
    ffilt, L, freq, PSD, PSDclean = fft_filter(df[data_col], samplerate,
                                               PSD_cutoff, f_high_cutoff,
                                               f_low_cutoff, f_cutoff_bands)
    fft_filter_plot.quick_plot_fft(list(df[timestamp]), df[data_col], ffilt,
                                   L, freq, PSD, PSDclean)


if __name__ == '__main__':
    # Load the data
    from random import randint
    samplerate = 1200
    x = np.linspace(0, 2, samplerate)
    noise = (randint(0, 2) * np.sin(2 * np.pi * randint(100, 500) * x) +
             randint(0, 2) * np.sin(2 * np.pi * randint(100, 500) * x) +
             randint(0, 2) * np.sin(2 * np.pi * randint(100, 500) * x))
    y = 3 * np.sin(2 * np.pi * 2 * x) + 2 * np.cos(2 * np.pi * 5 * x) + noise

    # Get the sampelrate and timestamp
    df = pd.DataFrame([x, y]).transpose()
    df.columns = ['Time (s)', 'Sensor (V)']

    # Process the data
    quick_process(df, samplerate, timestamp='Time (s)', data_col='Sensor (V)',
                  PSD_cutoff=None, f_high_cutoff=10)
