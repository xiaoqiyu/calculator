import unittest
from fractions import Fraction
from bh_calc import *


class TestBhCalc(unittest.TestCase):

    def test_bh_calc_result(self):
        self.assertEqual(bh_calc('3+4'), '7')
        self.assertEqual(bh_calc ('99999999999/100000000000'),'99999999999/100000000000')
        self.assertEqual(bh_calc('1/7+1/7+1/7+1/7+1/7+1/7+1/7'),'1')
        self.assertEqual(bh_calc('1/(1/(3+4))'),'7')
        self.assertEqual(bh_calc('-2.*(1.2e+02+1.2e+02)'),'-480')
        self.assertEqual(bh_calc(''),None)
        self.assertEqual(bh_calc(None),None)
        self.assertEqual(bh_calc('3*+4'),'12')
        self.assertEqual(bh_calc('480.0/(-1.2e+02+-1.2e+02)'),'-2')
        self.assertEqual(bh_calc('3e+03+---4e+03'),'-1000')
    def test_bh_calc_exception(self):
        with self.assertRaises(ValueError):
            bh_calc('3+*4')
        with self.assertRaises(ValueError):
            bh_calc('3*((4+')
        with self.assertRaises(ValueError):
            bh_calc('*3+4')

if  __name__ == '__main__':
    unittest.main()
