"""Programme to create histograms of the bandwidths of the estimated densities
obtained from density_estimation_simulated_data.py.

"""

import pickle
import json
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt

from bld.project_paths import project_paths_join as ppj

# Load estimated densities for simulated data.
with open(
    ppj('OUT_ANALYSIS', 'estimated_densities_simulated_data.pickle'), 'rb'
) as f_results:
    estimated_densities = pickle.load(f_results)

# Load sample sizes for samples in simulation.
with open(ppj('IN_MODEL_SPECS', 'samples.json')) as f_samples:
    samples = json.load(f_samples)

# Load density parameters.
with open(ppj('IN_MODEL_SPECS', 'densities.json')) as f_densities:
    densities = json.load(f_densities)

# Load bandwidths methods as they need to be specified before the first
# for-loop.
with open(
    ppj('OUT_ANALYSIS', 'bw_methods_simulation_data.pickle'), 'rb'
) as f_bw:
    bw_methods = pickle.load(f_bw)

# Load optimal bandwidth for Dagum distribution.
with open(ppj('OUT_ANALYSIS', 'opt_bw_dagum.pickle'), 'rb') as f_opt_bw:
    opt_bw_dagum = pickle.load(f_opt_bw)

# Load optimal bandwidth for Gaussian mixture distribution.
with open(ppj('OUT_ANALYSIS', 'opt_bw_gaussian.pickle'), 'rb') as f_opt_bw:
    opt_bw_gaussian = pickle.load(f_opt_bw)

# Create dictionary containing bandwidths from samples in simulation.
bandwidths = {}
for sample_size in sorted(estimated_densities.keys()):
    bandwidths[sample_size] = {}

    for density in sorted(estimated_densities[sample_size].keys()):
        bandwidths[sample_size][density] = {}

        for method in bw_methods:
            bw = []

            for sample in sorted(
                estimated_densities[sample_size][density].keys()
            ):
                bw.append(
                    estimated_densities[sample_size][density][sample][method][
                        'bandwidth']
                )

            bandwidths[sample_size][density][method] = bw

# Specify plot parameters.
plot_params = {
    'colour_bw': {'lscv': 'grey', 'silverman': 'black'},
    'figure_size': (12, 9),
    'font_size_labels': 25,
    'font_size_legend': 20,
    'font_size_ticks': 23,
    'line_width': 2.5,
    'y_axis': {
        'density_0': [-5, 600],
        'density_1': [-5, 500],
        'density_2': [-5, 600],
    }
}

# Create empty dictionary for bins.
bins = {}

# Create histograms of bandwidths over samples.
for sample_size in sorted(bandwidths.keys()):
    for density in sorted(bandwidths[sample_size].keys()):
        # Use latex font.
        rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
        rc('text', usetex=True)

        # Create figure.
        fig, ax = plt.subplots()

        # Remove frame.
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        # Set axis labels.
        ax.set_xlabel(
            'Bandwidth', fontsize=plot_params['font_size_labels']
        )
        ax.set_ylabel(
            'Frequency', fontsize=plot_params['font_size_labels']
        )

        # Adjust ticks.
        ax.tick_params(
            axis='x', labelsize=plot_params['font_size_ticks'], direction='out'
        )
        ax.tick_params(
            axis='y', labelsize=plot_params['font_size_ticks'], direction='out'
        )

        # Set desired number of ticks.
        plt.locator_params(nbins=8)

        # Use same bin size for both histograms.
        b = bandwidths[sample_size][density]['lscv']
        a = bandwidths[sample_size][density]['silverman']

        # Use bins from first sample for all samples.
        if sample_size == 'sample_size_0':
            bins[density] = np.histogram(np.hstack((a, b)), bins=40)[1]

        # Set axis limits.
        ax.set_ylim(plot_params['y_axis'][density])

        # Plot the histograms.
        plt.hist(
            bandwidths[sample_size][density]['silverman'], bins[density],
            alpha=0.65, label='silverman', histtype='stepfilled',
            edgecolor='none', color=plot_params['colour_bw']['silverman']
        )

        plt.hist(
            bandwidths[sample_size][density]['lscv'], bins[density],
            alpha=0.65, label='lscv', histtype='stepfilled', edgecolor='none',
            color=plot_params['colour_bw']['lscv']
        )

        # Include line for optimal bandwidth.
        if densities[density]['distribution'] == 'standard_normal':
            opt_bw = 1.06 * samples[sample_size] ** (-0.2)
            plt.axvline(
                opt_bw, color='red', linestyle='solid', linewidth=2,
                label='optimal'
            )

        elif densities[density]['distribution'] == 'normal':
            plt.axvline(
                opt_bw_gaussian, color='red', linestyle='solid', linewidth=2,
                label='optimal'
            )

        elif densities[density]['distribution'] == 'burr3':
            plt.axvline(
                opt_bw_dagum, color='red', linestyle='solid', linewidth=2,
                label='optimal'
            )

        # Add line for average of bandwidths.
        avg_bw_silverman = (
            sum(bandwidths[sample_size][density]['silverman']) /
            len(bandwidths[sample_size][density]['silverman'])
        )
        plt.axvline(
            avg_bw_silverman, color='white', linestyle='dashed', linewidth=1.5
        )

        avg_bw_lscv = (
            sum(bandwidths[sample_size][density]['lscv']) /
            len(bandwidths[sample_size][density]['lscv'])
        )
        plt.axvline(
            avg_bw_lscv, color='white', linestyle='dashed', linewidth=1.5
        )

        # Add a legend to first two plots.
        if density.endswith('0'):
            plt.legend(
                fontsize=plot_params['font_size_legend'], ncol=3,
                loc='upper center', bbox_to_anchor=(0.5, 1.2)
            )

        # Save figure to pdf file.
        plt.savefig(
            ppj(
                'OUT_FIGURES',
                'fig_simulation_hist_{}_{}.pdf'.format(
                    sample_size, density
                )
            ),
            bbox_inches="tight"
        )

        # Clear figure.
        plt.close(fig)
