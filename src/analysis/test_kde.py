"""Provide tests for the module kde.py.

"""

import numpy as np
from nose.tools import *
from src.model_code.kde import UnivariateKernelDensity
from numpy.testing.utils import assert_array_almost_equal


class TestUnivariateKernelDensity:

    def test_calc_bw_positive_bandwidth(self):
        np.random.seed(1)
        data = np.random.normal(size=50)
        kde = UnivariateKernelDensity(data)
        bandwidth = 5.0
        result = 5.0

        kde(bandwidth)
        assert_equal(kde.bw, result, 1)

    def test_calc_bw_negative_bandwidth(self):
        np.random.seed(1)
        data = np.random.normal(size=50)
        kde = UnivariateKernelDensity(data)

        assert_raises_regexp(
            ValueError,
            "Bandwidth must be greater than 0.",
            kde,
            -5.0
        )

    def test_calc_bw_zero_bandwidth(self):
        np.random.seed(1)
        data = np.random.normal(size=50)
        kde = UnivariateKernelDensity(data)

        assert_raises_regexp(
            ValueError,
            "Bandwidth must be greater than 0.",
            kde,
            0
        )

    def test_calc_opt_bw_silverman(self):
        np.random.seed(1)
        data = np.random.normal(size=50)
        kde = UnivariateKernelDensity(data)
        result = 0.46965781464812373

        kde("silverman")
        assert_equal(kde.bw, result, 8)

    def test_calc_opt_bw_lscv(self):
        np.random.seed(1)
        data = np.random.normal(size=50)
        kde = UnivariateKernelDensity(data)
        result = 0.4052407

        kde("lscv")
        assert_equal(round(kde.bw, 7), result, 6)

if __name__ == '__main__':
    from nose.core import runmodule
    runmodule(exit=False)
