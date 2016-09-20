.. _model_code:

**********
Model code
**********

The directory *src/model_code* contains source files that might differ by model and which are potentially used at various steps of the analysis.

Kernel Density Estimator
========================

The module ``kde.py`` contains the kernel density estimator for the Gaussian kernel function. Additionally, the log-transformed Gaussian kernel as described by Charpentier and Flachaire (2015, :cite:`Charpentier2015a`) is available. To use the log-Gaussian kernel, the data has to have been transformed before initialising the class. As the thesis' main concern is the bandwidth, the rationale behind the design of the estimator class is to create an instance once based on the data and then to be able to obtain the different estimates by specifying the respective bandwidth selection method. For this purpose, the class is constructed as follows:

.. autoclass:: src.model_code.kde.UnivariateKernelDensity
    :members:
    :private-members:

Creating an instance of this class takes the data sample as the only necessary argument. Optionally, the gridsize and the kernel function can be specified. Calling the instance like a function with the bandwidth as its only argument, i.e. ``instance(bandwidth)``, is equivalent to explicitly calling ``instance.estimate(bandwidth)``. Given that the bandwidth selection is the main focus of the thesis, this is convenient when comparing the results of the different procedures in the simulations and applications. The ``bandwidth`` argument can either be a float, integer, a rule of thumb string or the least-squares cross-validation string. Note that the class is designed such that any bandwidth selection procedure can easily be added by simply creating a new function and adding it to the for-loop in **_calc_bw()**.

The reason that the function calculating the optimal lscv bandwidth **_calc_opt_bw_lscv()** is based on the the R package `stats <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/00Index.html>`_ is that there is no statistical python package that implements this procedure. In addition, the optimal value obtained from the minimisation of the cross-validation criterion is heavily influenced by the chosen optimiser. In particular, this is already true for different implementations in R. The function uses ``bw.ucv`` as it is contained in the most basic version of R without having to load any additional package.
