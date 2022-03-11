# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 14:42:15 2021.

@author: Bas Klein Ikkink & Wolf de Kwant
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def create_timestamp(n, samplerate):
    """Return a timestamp column."""
    return [i * 1 / samplerate for i in range(n)]


def quick_plot(t, f, ffilt, L, freq, PSD, PSDclean, save_fig=False,
               filename='quick_plot.png'):
    """Make an overvieuw plot of the data."""
    # Plot some shit
    plt.rcParams['figure.figsize'] = [16, 12]
    plt.rcParams.update({'font.size': 18})
    fig, axs = plt.subplots(3, 1)

    plt.sca(axs[0])
    plt.plot(t, f, color='c', lw=1.5, label='Noisy')
    plt.plot(t, ffilt, color='k', lw=2, label='Filtered')
    plt.xlabel('Time (s)')
    plt.ylabel('Signal (V)')
    plt.xlim(t[0], t[-1])
    plt.grid(True)
    plt.legend()

    plt.sca(axs[1])
    plt.plot(t, ffilt, color='k', lw=2, label='Filtered')
    plt.xlabel('Time (s)')
    plt.ylabel('Signal (V)')
    plt.xlim(t[0], t[-1])
    plt.grid(True)
    plt.legend()

    plt.sca(axs[2])
    plt.plot(freq[L], PSD[L], color='c', lw=2, label='Noisy')
    plt.plot(freq[L], PSDclean[L], color='k', lw=1.5, label='Filtered')
    plt.xlim(freq[L[0]], freq[L[-1]])
    plt.ylim([0, 250])
    plt.xlim([0, 250000])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude (-)')
    plt.grid(True)
    plt.legend()

    if save_fig:
        plt.savefig(filename, dpi=1000)
    else:
        plt.show()


def fft_filter(col, samplerate, PSD_cutoff=None, f_cutoff=None):
    """Use an FFT filter to filter out some noise."""
    # Compute the FFT
    dt = 1 / samplerate
    n = len(col)
    fhat = np.fft.fft(col, n)  # Compute the FFT

    # Compute power density spectrum (amplitude)
    PSD = fhat * np.conj(fhat) / n
    PSDclean = PSD
    freq = (1 / (dt * n)) * np.arange(n)  # Create the x axis
    L = np.arange(1, np.floor(n / 2), dtype='int')  # Only plot first half

    # Use PSD to filter out noise
    if not(type(PSD_cutoff) is type(None)):
        indices = PSD > PSD_cutoff  # Find all the freqs with large power
        PSDclean = PSD * indices  # Zero out all the options
        fhat = indices * fhat  # Zero out the small fourier coefficients
    if not(type(f_cutoff) is type(None)):
        cut_off = int(f_cutoff * len(fhat) * dt / 2)  # Calc cut off index
        fhat[cut_off:] = 0
        PSDclean[cut_off:] = 0

    ffilt = np.fft.ifft(fhat)  # Inverse FFT filtered time signal

    return ffilt, L, freq, PSD, PSDclean


def quick_process(df, samplerate, timestamp='Time (s)', col='Sensor (V)',
                  PSD_cutoff=None, f_cutoff=None):
    """Calculate some things about the data."""
    ffilt, L, freq, PSD, PSDclean = fft_filter(df[col], samplerate, PSD_cutoff,
                                               f_cutoff)
    quick_plot(list(df[timestamp]), df[col], ffilt, L, freq, PSD, PSDclean)


if __name__ == '__main__':
    # Load the data
    filename = 'drip_lazer_500000Hz.csv'
    df = pd.read_csv(filename, index_col=0).iloc[100:, :]

    # Get the sampelrate and timestamp
    samplerate = int(filename.split('_')[-1:][0].split('H')[:-1][0])
    df['Time (s)'] = create_timestamp(len(df['Sensor (V)']), samplerate)

    # Process the data
    quick_process(df, samplerate, timestamp='Time (s)', col='Sensor (V)',
                  PSD_cutoff=0, f_cutoff=10000)
