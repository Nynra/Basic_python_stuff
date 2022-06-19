# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 23:29:30 2022.

@author: baskl
"""
import matplotlib.pyplot as plt


def quick_plot_fft(t, f, ffilt, L, freq, PSD, PSDclean, save_fig=False,
                   filename='quick_plot.png'):
    """
    Make an overvieuw plot of the data.

    Parameters
    ----------
    t : np.array
        1D numpy array containing the timestamp data in float.
    f : np.array
        1D numpy array containing the original data.
    ffilt : np.array
        1D numpy array containing the filtered data.
    L : TYPE
        DESCRIPTION.
    freq : TYPE
        DESCRIPTION.
    PSD : TYPE
        DESCRIPTION.
    PSDclean : TYPE
        DESCRIPTION.
    save_fig : TYPE, optional
        DESCRIPTION. The default is False.
    filename : TYPE, optional
        DESCRIPTION. The default is 'quick_plot.png'.

    Returns
    -------
    None.

    """
    # Plot some shit
    plt.rcParams['figure.figsize'] = [16, 12]
    plt.rcParams.update({'font.size': 18})
    fig, axs = plt.subplots(3, 1)

    # Plot all the data
    plt.sca(axs[0])
    plt.plot(t, f, color='c', lw=1.5, label='$Noisy$')
    plt.plot(t, ffilt, color='k', lw=2, label='$Filtered$')
    plt.xlabel('$Time\; \mathrm{(s)}$')
    plt.ylabel('$Signal\; \mathrm{(V)}$')
    plt.xlim(t[0], t[-1])
    plt.grid(True)
    plt.legend(loc='upper right')

    # Plot the filtered data
    plt.sca(axs[1])
    plt.plot(t, ffilt, color='k', lw=2, label='$Filtered$')
    plt.xlabel('$Time\; \mathrm{(s)}$')
    plt.ylabel('$Signal\; \mathrm{(V)}$')
    plt.xlim(t[0], t[-1])
    plt.grid(True)
    plt.legend(loc='upper right')

    # Plot the amplitude spectrum
    plt.sca(axs[2])
    plt.plot(freq[L], PSD[L], color='c', lw=2, label='$Noisy$')
    plt.plot(freq[L], PSDclean[L], color='k', lw=1.5, label='$Filtered$')
    plt.xlim(freq[L[0]], freq[L[-1]])
    plt.xlabel('$Frequency\; \mathrm{(Hz)}$')
    plt.ylabel('$Amplitude\; \mathrm{(-)}$')
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.tight_layout()

    if save_fig:
        plt.savefig(filename, dpi=1000)
    else:
        plt.show()
