"""
Created on Mon Mar 15 18:04:13 2021.

@author: baskl
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import locale


def set_aestetics():
    """Set the graph aestetics to fancy."""
    # Set the general graph parameters
    # Set comma for decimals
    locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')
    plt.rcParams['axes.formatter.use_locale'] = True
    sns.set(rc={'text.usetex': True})  # Turn on the LaTeX interpreter
    sns.set_style('whitegrid')  # Set the graph grid to white


def create_fancy_graph(df, y1, y2=None, y1label='Grote pendulum',
                       y2label='Kleine pendulum', save_fig=False,
                       filename=None):
    """
    Create a nice and fancy graph of the given measurement data.

    Parameters
    ----------
    df : pandas DataFrame
        Dataframe with the measurement data.
    y1 : string
        Name of the column with the data for the first plot.
    y2 : string, optional
        Name of the column with the data for the second plot.
        The default is None.
    y1label : string, optional
        First plot label. The default is 'Grote pendulum'.
    y2label : string, optional
        Second plot label. The default is 'Kleine pendulum'.
    safe_fig : bool, optional
        Boolean for if the figure should be saved. The default is False.
    file_name : string, optional
        Filename for when the plot is saved. The default is None.

    Returns
    -------
    None.

    """
    # Create the plot
    sns.lineplot(data=df, x='Time (s)', y=y1, label=y1label,
                 color='Blue', lw=0.5, ls='--', alpha=0.3)
    sns.scatterplot(data=df, x='Time (s)', y=y1, color='Blue',
                    s=0.5)

    if y2 != None:
        sns.lineplot(data=df, x='Time (s)', y=y2, label=y2label,
                     color='Orange', lw=0.5, ls='--', alpha=0.3)
        sns.scatterplot(data=df, x='Time (s)', y=y2, color='Orange',
                        s=0.5)

    # Add the plot attributes
    plt.xlabel('$Tijd\\  \mathrm{(s)}$')
    plt.ylabel('$Hoek\\ \mathrm{(rad)}$')
    plt.legend(loc='best')

    if save_fig and filename != None:
        # Generate the a file with the graph
        plt.savefig(filename, dpi=500)
    else:
        plt.show()


if __name__ == '__main__':
    import os
    # Echo all the measurement folder names to the user and as wich one
    # should be analysed
    content = os.listdir(os.getcwd())
    print('Folders:')
    count = 0

    for i in content:
        if '.' not in i and ',' in i:
            print('{}. {}'.format(count, i))
        count += 1
    print(' ')

    while True:
        response = input('Which measurement should be processed: ')
        if response.isdigit():
            if int(response) >= 0 or int(response) < len(content):
                folder_name = content[int(response)]
                break
        print('Invalid input, please try again.')

    # Load the data
    df = pd.read_csv('{}/output.csv'.format(folder_name), index_col=False)

    # Create the graph
    create_fancy_graph(df, y1='grote hoek', y2='kleine hoek',
                       filename='Raw data.png', save_fig=True)
