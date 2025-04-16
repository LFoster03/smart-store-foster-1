import unittest
import pandas as pd
from data_scrubber import DataScrubber  # Adjust the import path based on your project structure

class TestDataScrubber(unittest.TestCase):
    def setUp(self):
        # Example data to test
        data = {
            'CustomerID': [1, 2, 3],
            'JoinDate': ['2020-01-01', '2021-05-20', '2022-08-15'],
        }
        self.df = pd.DataFrame(data)
        self.scrubber = DataScrubber(self.df)

    def test_parse_dates_to_add_standard_datetime(self):
        # Apply the method
        cleaned_df = self.scrubber.parse_dates_to_add_standard_datetime('JoinDate')

        # Check that the 'StandardDateTime' column was added
        self.assertIn('StandardDateTime', cleaned_df.columns)

        # Check if the 'StandardDateTime' column is indeed in datetime format
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(cleaned_df['StandardDateTime']))

        # Check that there are no NaT values in 'StandardDateTime'
        self.assertTrue(cleaned_df['StandardDateTime'].notna().all())  # Ensure no NaT (Not a Time) values

# Run the test
if __name__ == '__main__':
    unittest.main()
