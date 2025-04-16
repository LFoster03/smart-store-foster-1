import pandas as pd
import os

# Define base paths
raw_data_path = r"C:\Projects\smart-store-foster-1\data\raw"
prepared_data_path = r"C:\Projects\smart-store-foster-1\data\prepared"

# Make sure output folder exists
os.makedirs(prepared_data_path, exist_ok=True)

# File configuration (updated column names)
files_info = {
    "customers_data.csv": {
        "expected_columns": [
            "CustomerID", "Name", "Region", "JoinDate",
            "LoyaltyPoints", "CustomerSegment", "LastPurchaseDate"
        ]
    },
    "products_data.csv": {
        "expected_columns": [
            "ProductId", "ProductName", "Category", "UnitPrice",
            "StockQuantity", "Supplier", "AverageRating"
        ]
    },
    "sales_data.csv": {
        "expected_columns": [
            "TransactionId", "SaleDate", "CustomerID", "ProductID", "StoreID",
            "CampaignID", "SaleAmount", "DiscountPercent", "PaymentType", "DiscountPercent"  # Note: Duplicate
        ]
    }
}

# Remove outliers using IQR method
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

# Remove duplicate columns
def remove_duplicate_columns(df):
    duplicated_cols = df.columns[df.columns.duplicated()].tolist()
    if duplicated_cols:
        print(f"   ⚠️ Duplicate columns found and removed: {duplicated_cols}")
    return df.loc[:, ~df.columns.duplicated()]

# Format all date-like columns
def format_date_columns(df):
    date_cols = [col for col in df.columns if "date" in col.lower()]
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            df[col] = df[col].dt.strftime('%Y-%m-%d')
        except Exception as e:
            print(f"   ⚠️ Could not format date column '{col}': {e}")
    return df

# Process files
for filename, info in files_info.items():
    print(f"\n📂 Processing {filename}...")

    try:
        raw_file = os.path.join(raw_data_path, filename)
        df = pd.read_csv(raw_file)
        print(f"   🔍 Original shape: {df.shape}")

        # Remove duplicate columns first
        df = remove_duplicate_columns(df)

        # Keep only expected columns (remove duplicates from config too)
        expected_cols = list(dict.fromkeys(info["expected_columns"]))  # removes dupes like DiscountPercent
        df = df[[col for col in expected_cols if col in df.columns]]
        print(f"   📌 Columns retained: {list(df.columns)}")

        # Remove duplicate rows
        df = df.drop_duplicates()
        print(f"   🧹 Rows after dropping duplicates: {len(df)}")

        # Format any date columns
        df = format_date_columns(df)

        # Remove outliers from numeric columns
        numeric_cols = df.select_dtypes(include=["number"]).columns
        df = remove_outliers(df, numeric_cols)
        print(f"   📉 Rows after removing outliers: {len(df)}")

        # Save cleaned file
        prepared_file = os.path.join(prepared_data_path, filename.replace(".csv", "_prepared.csv"))
        df.to_csv(prepared_file, index=False)
        print(f"✅ Cleaned file saved to {prepared_file}")

    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")
