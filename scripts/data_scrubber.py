import pandas as pd
from typing import List, Dict, Union

class DataScrubber:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DataScrubber with a DataFrame.
        
        Parameters:
            df (pd.DataFrame): The DataFrame to be scrubbed.
        """
        self.df = df

    def remove_duplicates(self) -> pd.DataFrame:
        """Remove duplicate rows."""
        self.df = self.df.drop_duplicates()
        return self.df

    def convert_column_to_new_data_type(self, column: str, new_type: type) -> pd.DataFrame:
        """Convert a specified column to a new data type."""
        try:
            self.df[column] = self.df[column].astype(new_type)
            return self.df
        except KeyError:
            raise ValueError(f"Column name '{column}' not found in the DataFrame.")

    def drop_columns(self, columns: List[str]) -> pd.DataFrame:
        """Drop specified columns."""
        for column in columns:
            if column not in self.df.columns:
                raise ValueError(f"Column name '{column}' not found in the DataFrame.")
        self.df = self.df.drop(columns=columns)
        return self.df

    def filter_column_outliers(self, column: str, lower_bound: Union[float, int], upper_bound: Union[float, int]) -> pd.DataFrame:
        """Filter outliers based on specified bounds."""
        try:
            self.df = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]
            return self.df
        except KeyError:
            raise ValueError(f"Column name '{column}' not found in the DataFrame.")

    def format_column_strings_to_lower_and_trim(self, column: str) -> pd.DataFrame:
        """Format string columns to lowercase and trim whitespaces."""
        try:
            self.df[column] = self.df[column].str.lower().str.strip()
            return self.df
        except KeyError:
            raise ValueError(f"Column name '{column}' not found in the DataFrame.")

    def format_column_strings_to_upper_and_trim(self, column: str) -> pd.DataFrame:
        """Format string columns to uppercase and trim whitespaces."""
        try:
            self.df[column] = self.df[column].str.upper().str.strip()
            return self.df
        except KeyError:
            raise ValueError(f"Column name '{column}' not found in the DataFrame.")

    def handle_missing_data(self, drop: bool = False, fill_value: Union[None, float, int, str] = None) -> pd.DataFrame:
        """Handle missing data by either dropping rows or filling values."""
        if drop:
            self.df = self.df.dropna()
        elif fill_value is not None:
            self.df = self.df.fillna(fill_value)
        return self.df

    def inspect_data(self) -> Dict[str, Union[str, pd.Series]]:
        """Return the summary of the data including info and describe."""
        info_str = self.df.info()
        describe_str = self.df.describe().to_string()
        return {"info": info_str, "describe": describe_str}

    def parse_dates_to_add_standard_datetime(self, column: str) -> pd.DataFrame:
        """Parse a column to standard datetime format."""
        try:
            self.df['StandardDateTime'] = pd.to_datetime(self.df[column])
            return self.df
        except KeyError:
            raise ValueError(f"Column name '{column}' not found in the DataFrame.")

    def rename_columns(self, column_mapping: Dict[str, str]) -> pd.DataFrame:
        """Rename columns in the DataFrame based on a mapping."""
        for old_name, new_name in column_mapping.items():
            if old_name not in self.df.columns:
                raise ValueError(f"Column '{old_name}' not found in the DataFrame.")
        self.df = self.df.rename(columns=column_mapping)
        return self.df

    def reorder_columns(self, columns: List[str]) -> pd.DataFrame:
        """Reorder columns in the DataFrame."""
        for column in columns:
            if column not in self.df.columns:
                raise ValueError(f"Column '{column}' not found in the DataFrame.")
        self.df = self.df[columns]
        return self.df
