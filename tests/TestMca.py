#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TestMca.py: Tests for the `mcareader` module.
"""

import unittest

import numpy as np
import os

import mcareader as mca


class TestMca(unittest.TestCase):
    def test_mca(self):
        f = mca.Mca(os.path.join(os.path.dirname(__file__), "demo.mca"))

        for method in ["bestfit", "interpolation"]:
            xx, yy = f.get_points(trim_zeros=False, calibration_method=method)
            self.assertEqual(True, isinstance(xx, np.ndarray))
            self.assertEqual(True, isinstance(yy, np.ndarray))
            self.assertEqual(xx.shape, yy.shape)

        self.assertNotEqual("", f.get_section("DATA"))
        self.assertEqual("", f.get_section("UNEXISTING_SECTION"))

    def test_variables(self):
        f = mca.Mca(os.path.join(os.path.dirname(__file__), "demo.mca"))
        # Check the fixed values in the demo file
        # Check all the patterns in the file
        self.assertEqual("3", f.get_variable("GAIN"))
        self.assertEqual("80", f.get_variable("CLCK"))
        self.assertEqual("32°C", f.get_variable("Board Temp"))
        self.assertEqual("", f.get_variable("UNEXISTING_VARIABLE"))

    def test_background(self):
        f = mca.Mca(os.path.join(os.path.dirname(__file__), "demo.mca"))
        f2 = mca.Mca(os.path.join(os.path.dirname(__file__), "demo2.mca"))
        # demo2 has the same counts in double time. Hence, subtraction must yield half of the original counts

        xx, yy = f.get_points()
        xx2, yy2 = f.get_points(background=f2)
        for y, y2 in zip(yy, yy2):
            self.assertAlmostEqual(y, y2*2)

    def test_fit(self):
        f = mca.Mca(os.path.join(os.path.dirname(__file__), "demo.mca"))
        g = f.get_calibration_function(method="bestfit")
        # Values calculated independently
        self.assertAlmostEqual(g(0), 1./6.)
        self.assertAlmostEqual(g(1)-g(0), 0.05)

    def test_counts(self):
        f = mca.Mca(os.path.join(os.path.dirname(__file__), "demo.mca"))
        # Values calculated independently using a spreadsheet
        self.assertAlmostEqual(f.get_counts(), 96897)
        self.assertAlmostEqual(f.get_total_energy(), 978116.75)


if __name__ == "__main__":
    unittest.main()
