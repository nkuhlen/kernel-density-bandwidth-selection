"""This class implements the univariate kernel density estimator (KDE).

References
----------
Li, Q. and J. S. Racine (2007) "Nonparametric econometrics", Princeton
    University Press, Princeton.

Silverman, B. W. (1986): Density estimation for statistics and data analysis,
    CRC press.

"""

import numpy as np
import math
import rpy2.robjects as robjects


class UnivariateKernelDensity:

    """Univariate Kernel Density Estimator.

    Args:
        data : array-like
            The data points used for the estimation.

        gridsize : int
            If gridsize is None, max(len(data), 50) is used.

        kernel : str
            The kernel function to be used in the estimation. Implemented
            kernels:

            - "gaussian" for Gaussian
            - "log_gaussian" for log-transformed Gaussian

    """

    def __init__(self, data, gridsize=None, kernel='gaussian'):
        """Initialize the estimator with the data, the gridsize and kernel
        function.

        """

        self.data = np.asarray(data)
        self.gridsize = gridsize
        self.no_observations = len(self.data)
        self.kernel = kernel

    def _density_value(self, x, bandwidth):
        """Calculate value of either the Gaussian or log-transformed Gaussian
        kernel density estimate (specified when creating an instance of the
        estimator class) at point x for a given bandwidth.

        Args:
            bandwidth : float, str
                The value of the bandwidth or a string of an implemented
                bandwidth selection method.

            x : int, float
                The point at which the density should be estimated.


        """

        if self.kernel == 'gaussian':
            density_value = (
                (self.no_observations * self._calc_bw(bandwidth)) **
                (-1)) * (sum(
                    ((2 * math.pi)**(-0.5)) * np.exp(((-0.5) * ((
                        (self.data - x) / self._calc_bw(bandwidth)) ** 2)))
                )
            )
        elif self.kernel == 'log_gaussian':
            density_value = (
                (self.no_observations * self._calc_bw(bandwidth)) **
                (-1)) * (sum(
                    ((2 * math.pi)**(-0.5)) * np.exp(((-0.5) * ((
                        (self.data - x) / self._calc_bw(bandwidth)) ** 2))) *
                    (1 / x)
                )
            )
        else:
            raise ValueError("Kernel not implemented.")

        return density_value

    def _calc_opt_bw_silverman(self):
        """Calculate the optimal bandwidth according to Silverman's rule of
        thumb for a Gaussian Kernel [Silverman (1986), p.48].

        """

        bw_silverman = (
            0.9 * np.std(self.data) / (self.no_observations ** (1 / 5))
        )

        return bw_silverman

    def _calc_opt_bw_lscv(self):
        """Use the built-in unbiased cross validation from R package stats to
        calculate the optimal band width based on the least-squares cross
        validation procedure.

        """

        rucv = robjects.r('bw.ucv')
        bw_lscv = float(np.asarray(rucv(robjects.FloatVector(self.data[:]))))

        return bw_lscv

    def _calc_bw(self, bandwidth):
        """Calculate the bandwidth according to the method specified by the
        bandwidth argument.

        Args:
            bandwidth : float, str
                The value of the bandwidth or a string of an implemented
                bandwidth selection method.

        """

        if type(bandwidth) in [float, int]:
            if bandwidth <= 0:
                raise ValueError("Bandwidth must be greater than 0.")
            else:
                self.bw = bandwidth
        elif bandwidth == "silverman":
            self.bw = self._calc_opt_bw_silverman()
        elif bandwidth == "lscv":
            self.bw = self._calc_opt_bw_lscv()

        return self.bw

    def estimate(self, bandwidth, stretch=4):
        """Estimate the density using a Gaussian kernel and the bandwidth as
        specified.

        Args:
            bandwidth : float, str
                The value of the bandwidth or a string of an implemented
                bandwidth selection method.

            stretch : float
                Adjusts the grid to ensure that the estimated density reaches
                zero past the max/min value of the data.

        """

        if self.gridsize is None:
            gridsize = max(self.no_observations, 50)
        else:
            gridsize = self.gridsize

        lower_bound = (
            np.min(self.data, axis=0) - stretch * self._calc_bw(bandwidth)
        )
        upper_bound = (
            np.max(self.data, axis=0) + stretch * self._calc_bw(bandwidth)
        )

        gridpoints = np.linspace(lower_bound, upper_bound, gridsize)
        estimated_density = [0] * gridsize

        for i in range(gridsize):
            estimated_density[i] = self._density_value(
                gridpoints[i], bandwidth
            )

        self.estimated_density = estimated_density
        self.support = gridpoints

    def __call__(self, bandwidth, stretch=4):
        return self.estimate(bandwidth, stretch)
