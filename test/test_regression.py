import unittest
import mytools.regression as reg
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_sigmoid_first_derivative(self):
        sigm_model = (66.9894743685211, 10.744363529183987, 1085.4874378851223, 0.3511726187832844)
        thresholds = [.1, .5, 1, 2]
        for t in thresholds:
            fd = reg.sigmoid_first_derivative_less_than(sigm_model, t)
            r = reg.sigmoid_first_derivative(sigm_model, np.array(fd))
            self.assertAlmostEqual(r[0], t)
            self.assertAlmostEqual(r[1], t)


if __name__ == '__main__':
    unittest.main()
