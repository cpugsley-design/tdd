import os
import sys
import unittest
import fire_gdp 
from pathlib import Path
from tempfile import TemporaryDirectory

TEST_FILE = Path(__file__).resolve().parent / "data" / "test_co2.csv"

class TestGetColumnIndex(unittest.TestCase):

    def test_no_query(self):
        "No query should return all data rows."
        result = fire_gdp.get_data(TEST_FILE)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 153)
        self.assertTrue(all(isinstance(row, list) for row in result))
        self.assertEqual(result[0][0], "Australia")
        self.assertEqual(result[0][1], "1990")

if __name__ == '__main__':
    unittest.main()
