"""Programme to approximate the optimal bandwidth for the Gaussian mixture used
in the simulation. The approximation is based on estimating the mean integrated
squared error when using the kernel density estimator with a Gaussian kernel.

"""

import numpy as np
import json
import pickle
from scipy.stats import norm
from scipy.integrate import quad

from bld.project_paths import project_paths_join as ppj
from src.model_code.kde import UnivariateKernelDensity

# Load data from simulation.
with open(ppj('OUT_DATA', 'simulation_data.pickle'), 'rb') as f_results:
    simulation_data = pickle.load(f_results)

# Load sample sizes for samples in simulation.
with open(ppj('IN_MODEL_SPECS', 'samples.json')) as f_samples:
    samples = json.load(f_samples)

# Load the number of samples to be drawn.
with open(ppj('IN_MODEL_SPECS', 'draws.json')) as f_draws:
    draws = json.load(f_draws)

# Load density parameters.
with open(ppj('IN_MODEL_SPECS', 'densities.json')) as f_densities:
    densities = json.load(f_densities)

# Create empty list for ISE, and dictionaries for MISE and the optimal
# bandwidth.
ise = []
mise = {}
optimal_bandwidth = {}

# Create grid of bandwidths
gridsize = 100
bandwidths = np.linspace(0.01, 1, gridsize).tolist()

for i in range(gridsize):
    bandwidth = bandwidths[i]
    mise[bandwidth] = {}

    for d in range(draws['configuration_0']):
        sample = 'sample_{}'.format(d)

        # Initialise the kernel density estimator with the current sample.
        kde = UnivariateKernelDensity(
            simulation_data['sample_size_1']['density_1'][sample]
        )

        # Define a the integrated squared error as a function that can be
        # integrated with respect to x.
        def integrand(x):
            return ((kde._density_value(x, bandwidth) - (
                densities['density_1']['alpha'] *
                norm.pdf(x,
                    densities['density_1']['mu_1'],
                    densities['density_1']['sigma_1']) +
                densities['density_1']['beta'] *
                norm.pdf(x,
                    densities['density_1']['mu_2'],
                    densities['density_1']['sigma_2'])
            )) ** 2)

        # Integrate the function from minus infinity to plus infinity.
        ise_calc, err = quad(integrand, -np.inf, np.inf)
        ise.append(ise_calc)

    mise[bandwidth] = sum(ise) / len(ise)

# Find the bandwidth which minimises the MISE criterion.
opt_bw_gaussian = min(mise, key=mise.get)

# Save the results in pickle object.
with open(ppj('OUT_ANALYSIS', 'opt_bw_gaussian.pickle'), 'wb') as f_results:
    pickle.dump(opt_bw_gaussian, f_results)
