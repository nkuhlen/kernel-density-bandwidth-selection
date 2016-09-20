.. _final:

************************************
Visualisation and results formatting
************************************

Documentation of the code in **final**. 

Simulation
==========

:file:`fig_simulation_histograms.py`:

	This file creates histograms of the bandwidths bandwidths of the estimated densities obtained from ``density_estimation_simulated_data.py``. Additionally, the optimal bandwidths obtained from the corresponding modules in **analysis** are shown.

:file:`fig_simulation_true_densities.py`:

	This file creates plots of the underlying densities used in the simulation studies. 


Application
===========

:file:`fig_map_included_countries.r`:

	This R file creates a map of the countries included in the estimation of the world income distributions. The list is obtained from ``density_estimation_pwt_71.py``.

:file:`fig_map_included_countries_2010.r`:

	This R file creates a map of the countries included in the estimation of the world income distributions in 2010. The list is obtained from ``density_estimation_pwt_71_2010.py``.

:file:`fig_world_incom_distribution.py`:

	This file plots the estimated world income distributions from ``density_estimation_pwt_71.py`` for different years and bandwidths obtained from the specified bandwidth selection procedures.

:file:`fig_world_incom_distribution_2010.py`:

	This file plots the estimated world income distributions from ``density_estimation_pwt_71_2010.py`` for different years and bandwidths obtained from the specified bandwidth selection procedures.
