"""Programme to plot the estimated world income distributions from
density_estimation_pwt_71.py for different years and bandwidths obtained from
the specified procedures.

"""

import json
from matplotlib import rc
import matplotlib.pyplot as plt

from bld.project_paths import project_paths_join as ppj

# Load estimated densities for pwt data set.
with open(
    ppj('OUT_ANALYSIS', 'estimated_densities_pwt71_2010.json'), 'r'
) as f_results:
    estimated_densities = json.load(f_results)

# Specify plot parameters.
plot_params = {
    'colour_bw': {'lscv': '#9C9C9C', 'silverman': '#484748'},
    'colour_bw_presentation': {'lscv': 'blue', 'silverman': 'black'},
    'figure_width': 10,
    'figure_height': 7.5,
    'font_size_labels': 28,
    'font_size_legend': 28,
    'font_size_ticks': 30,
    'line_width': 3.5,
    'title_size': 28
}

# Loop over all years and the specified bandwidth selection
# methods to plot estimated densities.
for year in sorted(estimated_densities.keys()):
    # Create figure.
    fig, ax = plt.subplots(
        figsize=(plot_params['figure_width'], plot_params['figure_height'])
    )

    for method in sorted(estimated_densities[year].keys()):
        # Use latex font.
        rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
        rc('text', usetex=True)

        # Create plot.
        ax.plot(
            estimated_densities[year][method]['support'],
            estimated_densities[year][method]['density'],
            color=plot_params['colour_bw'][method],
            label=method,
            linewidth=plot_params['line_width']
        )

        # Set axis limits.
        ax.set_xlim([-30000, 120000])
        ax.set_ylim([-0.000003, 0.0001])

        # Set axis labels.
        ax.set_xlabel(
            'GDP per Worker (Intl.\$)',
            fontsize=plot_params['font_size_labels']
        )
        ax.set_ylabel(
            'Density of Countries [$10^{{-4}}$]',
            fontsize=plot_params['font_size_labels']
        )

        # Set axis ticks and tick labels.
        plt.xticks(
            [-20000, 0, 20000, 40000, 60000, 80000, 100000, 120000],
            ['-20K', '0', '20K', '40K', '60K', '80K', '100K', '120K']
        )
        ax.tick_params(
            axis='x', labelsize=plot_params['font_size_ticks'], direction='out'
        )
        ax.tick_params(
            axis='y', labelsize=plot_params['font_size_ticks'], direction='out'
        )

        # Use scientific notation for y axis.
        yfm = ax.yaxis.get_major_formatter()
        yfm.set_powerlimits([-4, 4])
        offset = ax.get_yaxis().get_offset_text()
        offset.set_visible(False)

        # Remove frame.
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        # Add a legend.
        ax.legend(fontsize=plot_params['font_size_legend'], frameon=False)

        # Add a year as title.
        # plt.title(year, fontsize=plot_params['title_size'])

    # Remove whitespace around figure.
    plt.tight_layout()

    # Save figure to pdf file.
    fig.savefig(
        ppj(
            'OUT_FIGURES',
            'fig_world_income_distribution_{}_all_countries.pdf'.format(year))
    )

    # Clear figure.
    plt.close(fig)
