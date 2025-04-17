import pandas as pd
import sqlite3
import pathlib

# Constants
DW_DIR = pathlib.Path("C:/Projects/smart-store-foster-1/data/dw")
DB_PATH = DW_DIR / "smart_sales.db"

# Absolute paths to prepared CSV files
CUSTOMERS_CSV = pathlib.Path("C:/Projects/smart-store-foster-1/data/prepared/customers_data_prepared.csv")
PRODUCTS_CSV = pathlib.Path("C:/Projects/smart-store-foster-1/data/prepared/products_data_prepared.csv")
SALES_CSV = pathlib.Path("C:/Projects/smart-store-foster-1/data/prepared/sales_data_prepared.csv")

def create_schema(cursor: sqlite3.Cursor) -> None:
    """Create product, customer, and sale tables with correct schema."""

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            ProductID INTEGER PRIMARY KEY,
            ProductName TEXT,
            Category TEXT,
            UnitPrice REAL,
            StockQuantity INTEGER,
            Supplier TEXT,
            AverageRating REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            CustomerID INTEGER PRIMARY KEY,
            Name TEXT,
            Region TEXT,
            JoinDate TEXT,
            LoyaltyPoints INTEGER,
            CustomerSegment TEXT,
            LastPurchaseDate TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale (
            TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
            SaleDate TEXT,
            CustomerID INTEGER,
            ProductID INTEGER,
            StoreID INTEGER,
            CampaignID INTEGER,
            SaleAmount REAL,
            DiscountPercent REAL,
            PaymentType TEXT,
            FOREIGN KEY (CustomerID) REFERENCES customer (CustomerID),
            FOREIGN KEY (ProductID) REFERENCES product (ProductID)
        )
    """)

def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records from the tables."""
    cursor.execute("DELETE FROM sale")
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")

def insert_data(df: pd.DataFrame, table_name: str, cursor: sqlite3.Cursor) -> None:
    """Insert a DataFrame into the specified table."""
    df.to_sql(table_name, cursor.connection, if_exists="append", index=False)

def load_data_to_db() -> None:
    try:
        # Ensure the DW directory exists
        DW_DIR.mkdir(parents=True, exist_ok=True)

        # Connect to SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Setup schema and clear existing records
        create_schema(cursor)
        delete_existing_records(cursor)

        # Read in the data
        customers_df = pd.read_csv(CUSTOMERS_CSV)
        products_df = pd.read_csv(PRODUCTS_CSV)
        sales_df = pd.read_csv(SALES_CSV)

        # Insert into the database
        insert_data(customers_df, "customer", cursor)
        insert_data(products_df, "product", cursor)
        insert_data(sales_df, "sale", cursor)  # No TransactionID needed here

        conn.commit()
        print("✅ Data successfully loaded into smart_sales.db")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    load_data_to_db()
