""""Programme to estimate density functions based on simulated data using
different bandwidth selection procedures.

"""

import json
import pickle

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

# Specify bandwidth selection methods to be used in estimation.
bw_methods = ['lscv', 'silverman']
pickeled_estimated_densities = {}

for s in sorted(samples.keys()):
    sample_size = '{}'.format(s)
    pickeled_estimated_densities[sample_size] = {}

    for i in sorted(densities.keys()):
        density = '{}'.format(i)
        pickeled_estimated_densities[sample_size][density] = {}

        for d in range(draws['configuration_0']):
            estimated_densities = {}

            sample = 'sample_{}'.format(d)

            # Initialise estimator.
            kde = UnivariateKernelDensity(
                simulation_data[sample_size][density][sample]
            )

            for m in bw_methods:
                kde(m)

                estimated_densities[m] = {
                    'support': kde.support,
                    'density': kde.estimated_density,
                    'bandwidth': kde.bw
                }

            pickeled_estimated_densities[
                sample_size][density][sample] = estimated_densities

# Save the results in pickle object.
with open(
    ppj('OUT_ANALYSIS', 'estimated_densities_simulated_data.pickle'), 'wb'
) as f_results:
    pickle.dump(pickeled_estimated_densities, f_results)

with open(
    ppj('OUT_ANALYSIS', 'bw_methods_simulation_data.pickle'), 'wb'
) as f_bw:
    pickle.dump(bw_methods, f_bw)
