.. _analysis:

************************************
Main model estimations / simulations
************************************

The *src/analysis* directory contains the main modules for the density estimation and the approximation of the optimal bandwidths for distributions other than the standard normal distribution. 

Density Estimation
==================

The modules beginning with ``density_estimation_pwt_71`` contain the density estimations for the world income distributions. The module reads the data and the specified years from the data management process and calculates the density for every year. The results are stored in a JSON file for the visualisation step.

The module ``density_estimation_simulated_data.py`` calculates the density for the simulation data. The data is obtained from the data management step. The results are stored in pickle objects for the visualisation step.


Optimal Bandwidths
==================

The modules beginning with ``mise_optimal_bandwidth`` estimate the optimal bandwidth for the selection procedures where a direct calculation of the theoretically optimal bandwidth is not possible. The results are stored in pickle objects for the visualisation step.


Testing
=======

The module ``test_kde.py`` contains a limited test suite for the kernel density estimator in ``kde.py``.
