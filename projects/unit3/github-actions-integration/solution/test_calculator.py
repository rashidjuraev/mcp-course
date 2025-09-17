"""
Test suite for Calculator module
"""

import unittest
import time
import pytest
from calculator import Calculator, factorial, fibonacci, is_prime


class TestCalculator(unittest.TestCase):
    """Test cases for Calculator class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calc = Calculator()
    
    def test_add(self):
        """Test addition functionality."""
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0.1, 0.2), pytest.approx(0.3))
    
    def test_subtract(self):
        """Test subtraction functionality."""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(-1, -1), 0)
        self.assertEqual(self.calc.subtract(0.5, 0.1), pytest.approx(0.4))
    
    def test_multiply(self):
        """Test multiplication functionality."""
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 5), -10)
        self.assertEqual(self.calc.multiply(0, 100), 0)
    
    def test_divide(self):
        """Test division functionality."""
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(-6, 3), -2)
        self.assertEqual(self.calc.divide(1, 3), pytest.approx(0.333333))
    
    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)
    
    def test_power(self):
        """Test power functionality."""
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertEqual(self.calc.power(3, 2), 9)
    
    def test_square_root(self):
        """Test square root functionality."""
        self.assertEqual(self.calc.square_root(9), 3)
        self.assertEqual(self.calc.square_root(16), 4)
        self.assertEqual(self.calc.square_root(2), pytest.approx(1.414213))
    
    def test_square_root_negative(self):
        """Test square root of negative number raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.square_root(-1)
    
    def test_history(self):
        """Test calculation history functionality."""
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertIn("1 + 2 = 3", history)
        self.assertIn("3 * 4 = 12", history)
    
    def test_clear_history(self):
        """Test clearing calculation history."""
        self.calc.add(1, 2)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)


class TestMathFunctions(unittest.TestCase):
    """Test cases for standalone math functions."""
    
    def test_factorial(self):
        """Test factorial function."""
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(3), 6)
    
    def test_factorial_negative(self):
        """Test factorial with negative number raises ValueError."""
        with self.assertRaises(ValueError):
            factorial(-1)
    
    def test_fibonacci(self):
        """Test Fibonacci function."""
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(3), 2)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(8), 21)
    
    def test_fibonacci_negative(self):
        """Test Fibonacci with negative number raises ValueError."""
        with self.assertRaises(ValueError):
            fibonacci(-1)
    
    def test_is_prime(self):
        """Test prime number checking."""
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertFalse(is_prime(4))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(17))
        self.assertFalse(is_prime(25))


class TestSlowOperations(unittest.TestCase):
    """Test cases that take longer to run (for testing long-running jobs)."""
    
    def test_slow_calculation(self):
        """Test that simulates a slow calculation."""
        time.sleep(2)  # Simulate slow operation
        calc = Calculator()
        result = calc.add(1, 1)
        self.assertEqual(result, 2)
    
    def test_fibonacci_large(self):
        """Test Fibonacci with larger numbers (slower)."""
        time.sleep(1)
        result = fibonacci(10)
        self.assertEqual(result, 55)
    
    def test_prime_checking_large(self):
        """Test prime checking with larger numbers."""
        time.sleep(1)
        self.assertTrue(is_prime(97))
        self.assertFalse(is_prime(99))


# Tests that will FAIL (for testing failed builds)
class TestFailingScenarios(unittest.TestCase):
    """Test cases designed to fail (comment out when you want passing builds)."""
    
    @unittest.skip("Skip this test to avoid failure")
    def test_intentional_failure(self):
        """This test is designed to fail."""
        self.assertEqual(1, 2, "This should fail")
    
    @unittest.skip("Skip this test to avoid failure")
    def test_syntax_error_simulation(self):
        """This test simulates catching a syntax error."""
        # Uncomment the line below to cause a NameError
        # undefined_variable + 1
        pass
    
    @unittest.skip("Skip this test to avoid failure")
    def test_assertion_failure(self):
        """This test will fail with assertion error."""
        calc = Calculator()
        result = calc.add(2, 2)
        self.assertEqual(result, 5, "2 + 2 should equal 5 (intentional failure)")


if __name__ == '__main__':
    unittest.main()