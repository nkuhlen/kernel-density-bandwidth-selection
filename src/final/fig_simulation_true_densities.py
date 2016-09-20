"""Programme to plot the underlying densities used in the simulation study.

"""

import json
# import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from scipy.stats import burr
from scipy.stats import burr12
from scipy.stats.distributions import norm

from bld.project_paths import project_paths_join as ppj

# Load density parameters.
with open(ppj('IN_MODEL_SPECS', 'densities.json')) as f_densities:
    densities = json.load(f_densities)

# Specify plot parameters.
plot_params = {
    'figure_width': 10,
    'figure_height': 7.5,
    'font_size_labels': 23,
    'font_size_legend': 20,
    'font_size_ticks': 40,
    'line_width': 3.5
}

for d in sorted(densities.keys()):
    density = '{}'.format(d)

    # Set grid.
    if densities[density]['distribution'] == 'standard_normal':
        x_grid = np.linspace(-3, 3, 1000)
    elif densities[density]['distribution'] == 'normal':
        x_grid = np.linspace(-0, 5, 1000)
    elif densities[density]['distribution'] == 'burr3':
        x_grid = np.linspace(-0, 5, 1000)

    # Calculate densities.
    if densities[density]['distribution'] in ('normal', 'standard_normal'):
        pdf_true = (
            densities[density]['alpha'] * norm(
                densities[density]['mu_1'],
                densities[density]['sigma_1']
            ).pdf(x_grid) +
            densities[density]['beta'] * norm(
                densities[density]['mu_2'],
                densities[density]['sigma_2']
            ).pdf(x_grid) +
            densities[density]['gamma'] * norm(
                densities[density]['mu_3'],
                densities[density]['sigma_3']
            ).pdf(x_grid)
        )
    elif densities[density]['distribution'] == 'burr3':
        pdf_true = (
            densities[density]['alpha'] * burr(
                densities[density]['c_1'],
                densities[density]['d_1']
            ).pdf(x_grid) +
            densities[density]['beta'] * burr(
                densities[density]['c_2'],
                densities[density]['d_2']
            ).pdf(x_grid)
        )
    elif densities[density]['distribution'] == 'burr12':
        pdf_true = (
            densities[density]['alpha'] * burr12(
                densities[density]['c_1'],
                densities[density]['d_1'],
                scale=densities[density]['q_1']
            ).pdf(x_grid) +
            densities[density]['beta'] * burr12(
                densities[density]['c_2'],
                densities[density]['d_2'],
                scale=densities[density]['q_2']
            ).pdf(x_grid)
        )

    # Create figure.
    fig, ax = plt.subplots(
        figsize=(plot_params['figure_width'], plot_params['figure_height'])
    )

    ax.plot(
        x_grid, pdf_true, color='black', linewidth=plot_params['line_width']
    )

    # Set tick size.
    ax.tick_params(
        axis='x', labelsize=plot_params['font_size_ticks'], direction='out'
    )
    ax.tick_params(
        axis='y', labelsize=plot_params['font_size_ticks'], direction='out'
    )

    # Remove frame.
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Use latex font.
    rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    rc('text', usetex=True)

    # Remove whitespace around figure.
    plt.tight_layout()

    # Save figure to pdf file.
    fig.savefig(
        ppj('OUT_FIGURES', 'fig_simulation_true_{}.pdf'.format(density))
    )

    # Clear figure.
    plt.close(fig)
