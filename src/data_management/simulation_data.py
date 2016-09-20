"""Draw simulated samples for the simulation. The sample sizes are obtained
from JSON files in src/model_specs.

"""

import json
import pickle
import numpy as np
from scipy.stats import norm
from scipy.stats import burr
from scipy.stats import burr12

from bld.project_paths import project_paths_join as ppj

# Load sample sizes for samples in simulation.
with open(ppj('IN_MODEL_SPECS', 'samples.json')) as f_samples:
    samples = json.load(f_samples)

# Load the number of samples to be drawn.
with open(ppj('IN_MODEL_SPECS', 'draws.json')) as f_draws:
    draws = json.load(f_draws)

# Load density parameters.
with open(ppj('IN_MODEL_SPECS', 'densities.json')) as f_densities:
    densities = json.load(f_densities)

# Set the seed for replicability.
np.random.seed(123)

simulation_data = {}

for s in sorted(samples.keys()):
    sample_size = '{}'.format(s)
    simulation_data[sample_size] = {}

    for i in sorted(densities.keys()):
        density = '{}'.format(i)
        simulation_data[sample_size][density] = {}

        if densities[density]['distribution'] in ('normal', 'standard_normal'):
            for d in range(draws['configuration_0']):
                sample = 'sample_{}'.format(d)

                simulation_data[sample_size][density][sample] = (
                    np.concatenate(
                        [norm(
                            densities[density]['mu_1'],
                            densities[density]['sigma_1']
                        ).rvs(
                            densities[density]['alpha'] * samples[sample_size]
                        ), norm(
                            densities[density]['mu_2'],
                            densities[density]['sigma_2']
                        ).rvs(
                            densities[density]['beta'] * samples[sample_size]
                        ), norm(
                            densities[density]['mu_3'],
                            densities[density]['sigma_3']
                        ).rvs(
                            densities[density]['gamma'] * samples[sample_size]
                        )]
                    )
                )
        elif densities[density]['distribution'] == 'burr3':
            for d in range(draws['configuration_0']):
                sample = 'sample_{}'.format(d)

                simulation_data[sample_size][density][sample] = (
                    np.concatenate(
                        [burr(
                            densities[density]['c_1'],
                            densities[density]['d_1']
                        ).rvs(
                            densities[density]['alpha'] * samples[sample_size]
                        ), burr(
                            densities[density]['c_2'],
                            densities[density]['d_2']
                        ).rvs(
                            densities[density]['beta'] * samples[sample_size]
                        )]
                    )
                )
        elif densities[density]['distribution'] == 'burr12':
            for d in range(draws['configuration_0']):
                sample = 'sample_{}'.format(d)

                simulation_data[sample_size][density][sample] = (
                    np.concatenate(
                        [burr12(
                            densities[density]['c_1'],
                            densities[density]['d_1'],
                            scale=densities[density]['q_1']
                        ).rvs(
                            densities[density]['alpha'] * samples[sample_size]
                        ), burr12(
                            densities[density]['c_2'],
                            densities[density]['d_2'],
                            scale=densities[density]['q_2']
                        ).rvs(
                            densities[density]['beta'] * samples[sample_size]
                        )]
                    )
                )

# Save the results in pickle object.
with open(
    ppj('OUT_DATA', 'simulation_data.pickle'), 'wb'
) as f_results:
    pickle.dump(simulation_data, f_results)
