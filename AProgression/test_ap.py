import unittest
from AP_in_Python import canMakeArithmeticProgression

class TestArithmeticProgression(unittest.TestCase):

    def test_valid_progression(self):
        self.assertTrue(
            canMakeArithmeticProgression([3, 5, 1])
        )

    def test_invalid_progression(self):
        self.assertFalse(
            canMakeArithmeticProgression([1, 2, 4])
        )

    def test_negative_numbers(self):
        self.assertTrue(
            canMakeArithmeticProgression([-5, -3, -1])
        )

    def test_duplicates(self):
        self.assertTrue(
            canMakeArithmeticProgression([2, 2, 2])
        )

    def test_single_element(self):
        self.assertTrue(
            canMakeArithmeticProgression([10])
        )

if __name__ == "__main__":
    unittest.main()