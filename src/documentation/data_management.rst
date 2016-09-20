.. _data_management:

Data management
===============

The data management part consists of two parts. The first simulates and prepares data for the simulation studies. The second part prepares data from the Penn World Table 7.1 for the estimation of the world income distribution. In particular, the data management is split up across the following modules:

``data_preparation_pwt71.py``

	.. automodule:: src.data_management.data_preparation_pwt71
	    :members:

``data_preparation_pwt71.py_2010``

	.. automodule:: src.data_management.data_preparation_pwt71_2010
	    :members:

``simulation_data.py``

	.. automodule:: src.data_management.simulation_data
	    :members:

More specifically, ``simulation_data.py`` reads the required parameters for the simulation from *src/model_specs*. First, it reads the samples sizes from ``samples.json``. Then, it determines the number of samples to be drawn from these samples from ``draws.json``. Finally, it obtains the parameters for the specification of the densities from ``densities.json``.
