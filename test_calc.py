import unittest
from lyca import Calculator
import sys
from io import StringIO

class TestCalc(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()
        self.capturedOutput = StringIO()          # Create StringIO object
        sys.stdout = self.capturedOutput

    def tearDown(self):
        self.capturedOutput.close()

    def test_temp_conversions(self):
        self.calc.default("11 mm in ft")
        self.assertEqual(float(self.capturedOutput.getvalue()), 0.03609)

    def test_direct_conversion(self):
        self.calc.default("3 m in mm")
        self.assertEqual(float(self.capturedOutput.getvalue()), 3000)

    def test_reverse_conversions1(self):
        self.calc.default("7 mm in m")
        self.assertEqual(float(self.capturedOutput.getvalue()), 0.007)

    def test_addition(self):
        self.calc.default("11.4 + 3")
        self.assertEqual(float(self.capturedOutput.getvalue()), 14.4)

    def test_multiplication(self):
        self.calc.default("7 * 1.5")
        self.assertEqual(float(self.capturedOutput.getvalue()), 10.5)

    def test_bracket_completion(self):
        self.calc.default("sin(pi/2 + 1")
        self.assertEqual(float(self.capturedOutput.getvalue()), 0.5403)

    def test_bracket_completion2(self):
        self.calc.default("sin(pi/2 - 2(")
        self.assertEqual(float(self.capturedOutput.getvalue()), -0.41615)

    def test_convert_currency(self):
        self.calc.default("1 usd in ils")
        ans = float(self.capturedOutput.getvalue())
        print("-----------", ans)
        self.assertLess(ans, 4)
        # self.assertGreater(ans, 3)

    def test_aliases(self):
        self.calc.default("1 meter in feet")
        self.assertEqual(float(self.capturedOutput.getvalue()), 3.28084)
if __name__ == "__main__":
    unittest.main()
