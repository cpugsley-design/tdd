import os
import sys
import unittest
from src import fire_gdp 
from pathlib import Path
from tempfile import TemporaryDirectory

TEST_FILE = Path(__file__).resolve().parent.parent / "data" / "test_co2.csv"

class TestGetColumnIndex(unittest.TestCase):

    def setUp(self):
        """Define paths to the test datasets."""
        self.co2_file = (
            Path(__file__).resolve().parent.parent
            / "data" / "test_co2.csv"
        )

        self.gdp_file = (
            Path(__file__).resolve().parent.parent
            / "data" / "test_gdp.csv"
        )    

    def test_no_query(self):
        "No query should return all data rows."
        result = fire_gdp.get_data(TEST_FILE)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 153)
        self.assertTrue(all(isinstance(row, list) for row in result))
        self.assertEqual(result[0][0], "Australia")
        self.assertEqual(result[0][1], "1990")

    def test_empty_file(self):
        """An empty input file should produce exit code 1."""
        with TemporaryDirectory() as directory:
            empty_file = Path(directory) / "empty.csv"
            empty_file.touch()

            with self.assertRaises(SystemExit) as error:
                fire_gdp.get_data(empty_file)

            self.assertEqual(error.exception.code, 1)
    
    def test_query_by_index(self):
        """A column index and value should filter rows."""
        result = fire_gdp.get_data(
            TEST_FILE,
            query_column=0,
            query_value="Australia"
        )

        self.assertEqual(len(result), 31)
        self.assertTrue(
            all(row[0] == "Australia" for row in result)
        )

    def test_query_by_name(self):
        """A column name and value should filter rows."""
        result = fire_gdp.get_data(
            TEST_FILE,
            query_column="Year",
            query_value="1990"
        )

        self.assertEqual(len(result), 4)
        self.assertTrue(
            all(row[1] == "1990" for row in result)
        )

    def test_no_matching_query(self):
        """A valid query with no matches returns an empty list."""
        result = fire_gdp.get_data(
            TEST_FILE,
            query_column="Area",
            query_value="Brazil"
        )

        self.assertEqual(result, [])

    def test_missing_query_column(self):
        """A missing query column should produce exit code 2."""
        with self.assertRaises(SystemExit) as error:
            fire_gdp.get_data(
                TEST_FILE,
                query_value="Australia"
            )

        self.assertEqual(error.exception.code, 2)

    def test_missing_query_value(self):
        """A missing query value should produce exit code 2."""
        with self.assertRaises(SystemExit) as error:
            fire_gdp.get_data(
                TEST_FILE,
                query_column="Area"
            )

        self.assertEqual(error.exception.code, 2)

    def test_query_with_header(self):
        """The header should precede the matching rows."""
        result = fire_gdp.get_data(
            TEST_FILE,
            query_column="Area",
            query_value="Australia",
            return_header=True
        )

        self.assertEqual(len(result), 32)
        self.assertEqual(result[0][0], "Area")
        self.assertEqual(result[0][1], "Year")
        self.assertEqual(result[0][3], "Forest fires")

        self.assertTrue(
            all(row[0] == "Australia" for row in result[1:])
        )

    def test_no_query_with_header(self):
        """The header should be included with all rows."""
        result = fire_gdp.get_data(TEST_FILE, return_header=True)

        self.assertEqual(len(result), 154)
        self.assertEqual(result[0][0], "Area")
        self.assertEqual(result[1][0], "Australia")

    def test_first_column(self):
        """Return index zero for the first column."""
        header = ["Area", "Year", "Forest fires"]

        result = fire_gdp.get_column_index(header, "Area")

        self.assertEqual(result, 0)

    def test_other_column(self):
        """Return the correct index for another column."""
        header = ["Area", "Year", "Forest fires"]

        result = fire_gdp.get_column_index(
            header, "Forest fires"
        )

        self.assertEqual(result, 2)

    def test_missing_column(self):
        """Return None when a column is not present."""
        header = ["Area", "Year", "Forest fires"]

        result = fire_gdp.get_column_index(header, "GDP")

        self.assertIsNone(result)

    def test_empty_header(self):
        """Return None when the header list is empty."""
        header = []

        result = fire_gdp.get_column_index(header, "Year")

        self.assertIsNone(result)

    def test_case_sensitivity(self):
        """Column names must match case exactly."""
        header = ["Area", "Year", "Forest fires"]

        result = fire_gdp.get_column_index(header, "year")

        self.assertIsNone(result)

    def test_complete_data(self):
        """Test matching years and values for Australia."""
        result = fire_gdp.get_fire_gdp_year_data(
            self.co2_file, self.gdp_file, "Australia"
        )

        self.assertEqual(len(result), 31)

        self.assertEqual(
            result[0], [1990, 4240.9972, 413659.0]
        )

        self.assertEqual(
            result[-1], [2020, 10985.2467, 1972898.0]
        )

        for row in result:
            self.assertIsInstance(row[0], int)
            self.assertIsInstance(row[1], float)
            self.assertIsInstance(row[2], float)

    def test_georgia_missing_gdp(self):
        """Test that missing early GDP values are skipped."""
        result = fire_gdp.get_fire_gdp_year_data(
            self.co2_file, self.gdp_file, "Georgia"
        )

        self.assertEqual(len(result), 25)

        self.assertEqual(
            result[0], [1996, 8.4549, 3868.48]
        )

        years = [row[0] for row in result]

        for year in [1992, 1993, 1994, 1995]:
            self.assertNotIn(year, years)

    def test_ireland_missing_gdp(self):
        """Test that missing GDP values are excluded."""
        result = fire_gdp.get_fire_gdp_year_data(
            self.co2_file, self.gdp_file, "Ireland"
        )

        self.assertEqual(len(result), 26)

        self.assertEqual(
            result[0], [1995, 0.4185, 54758.74]
        )

        years = [row[0] for row in result]

        for year in range(1990, 1995):
            self.assertNotIn(year, years)

    def test_nonexistent_country(self):
        """Test a country absent from both datasets."""
        result = fire_gdp.get_fire_gdp_year_data(
            self.co2_file, self.gdp_file, "Brazil"
        )

        self.assertEqual(result, [])

    def test_missing_fires_and_year(self):
        """Test missing emissions and unmatched GDP years."""
        with TemporaryDirectory() as directory:
            directory = Path(directory)

            co2_file = directory / "co2.csv"
            gdp_file = directory / "gdp.csv"

            co2_file.write_text(
                "Area,Year,Forest fires\n"
                "Testland,2000,10.5\n"
                "Testland,2001,\n"
                "Testland,2002,30.0\n"
                "Testland,2003,40.0\n",
                encoding="utf-8"
            )

            gdp_file.write_text(
                "Country,2000,2001,2002\n"
                "Testland,100.0,200.0,\n",
                encoding="utf-8"
            )

            result = fire_gdp.get_fire_gdp_year_data(
                co2_file, gdp_file, "Testland"
            )

            self.assertEqual(
                result, [[2000, 10.5, 100.0]]
            )
if __name__ == '__main__':
    unittest.main()
