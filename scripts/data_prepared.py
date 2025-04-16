import pandas as pd
import os

# Define base paths
raw_data_path = r"C:\Projects\smart-store-foster-1\data\raw"
prepared_data_path = r"C:\Projects\smart-store-foster-1\data\prepared"

# Make sure the output directory exists
os.makedirs(prepared_data_path, exist_ok=True)

# File configuration
files_info = {
    "customers_data.csv": {
        "expected_columns": ["CustomerID", "Name", "Region", "JoinDate", "LoyaltyPoints", "CustomerSegment", "LastPurchaseDate"]
    },
    "products_data.csv": {
        "expected_columns": ["ProductId", "ProductName", "Category", "UnitPrice", "StockQuantity", "Supplier", "AverageRating"]
    },
    "sales_data.csv": {
        "expected_columns": ["TransactionId", "SaleDate", "CustomerID", "ProductID", "StoreID", "CampaignID", "SaleAmount", "DiscountPercent", "PaymentType", "DiscountPercent" ]
    }
}

# Function to remove outliers using IQR
def remove_outliers(df, numeric_cols):
    for col in numeric_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower) & (df[col] <= upper)]
    return df

# Process each file
for filename, info in files_info.items():
    print(f"Processing {filename}...")

    try:
        raw_file = os.path.join(raw_data_path, filename)
        df = pd.read_csv(raw_file)

        # Keep only expected columns
        expected_cols = info["expected_columns"]
        df = df[[col for col in expected_cols if col in df.columns]]

        # Remove duplicates
        df = df.drop_duplicates()

        # Remove outliers from numeric columns
        numeric_cols = df.select_dtypes(include=["number"]).columns
        df = remove_outliers(df, numeric_cols)

        # Save cleaned file
        prepared_file = os.path.join(prepared_data_path, filename.replace(".csv", "_prepared.csv"))
        df.to_csv(prepared_file, index=False)
        print(f"Saved cleaned data to {prepared_file}\n")

    except Exception as e:
        print(f"❌ Error processing {filename}: {e}\n")
