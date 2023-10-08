### Configuration
###############################################################################
# Import packages
import unittest
import re

# Import modules
from src import regex_helper as rh
from src import patterns



### Test Patterns
###############################################################################
class TestPhoneNumberPattern(unittest.TestCase):

    def setUp(self):
        self.pattern = patterns.phone_number

    def test_valid_numbers(self):
        valid_numbers = [
            '+1 (555) 555-5555',
            '555-555-5555',
            '555.555.5555',
            '+1 234 567 8912',
            '1234567891',
            '(123) 456 7891',
            '555 555 5555',
            '555-555.5555',
            '1 555 555 5555',
            '+15555555555',
            '1-555-555-5555',
            '1.555.555.5555',
            '15555555555'
        ]
        for number in valid_numbers:
            with self.subTest(number=number):
                actual = rh.is_match(number, self.pattern)
                self.assertTrue(actual, f'Expected match for {number}, but got {actual}')
                
    def test_invalid_numbers(self):
        invalid_numbers = [
            '555',
            '+11234567890abc',
            '123-456',
            '555)-555-5555',
            '555-(555-5555'
        ]
        for number in invalid_numbers:
            with self.subTest(number=number):
                actual = rh.is_match(number, self.pattern)
                self.assertFalse(actual, f'Expected no match for {number}, but got {actual}')


class TestDollarAmountPattern(unittest.TestCase):

    def setUp(self):
        self.pattern = patterns.dollar_amount

    def test_valid_amounts(self):
        valid_amounts = [
            '$1',
            '$1.00',
            '$1.57 M',
            '$1,000',
            '$1,000.00',
            '$1,000,000',
            '$1,000,000.00',
            '1B USD',
            '5 million dollars'
            
        ]
        for amount in valid_amounts:
            with self.subTest(amount=amount):
                actual = rh.is_match(amount, self.pattern)
                self.assertTrue(actual, f'Expected match for {amount}, but got {actual}')
    
    def test_invalid_amounts(self):
        invalid_amounts = [
            '1,00',
            '1.',
            '.1',
            '$',
            '1,000.00.00',
            '1000000.00'
        ]
        for amount in invalid_amounts:
            with self.subTest(amount=amount):
                actual = rh.is_match(amount, self.pattern)
                self.assertFalse(actual, f'Expected no match for {amount}, but got {actual}')

    
if __name__ == "__main__":
    unittest.main()
