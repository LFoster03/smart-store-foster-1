import pandas as pd
import sqlite3
import pathlib
import sys

# Setup paths
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

DW_DIR = pathlib.Path("data").joinpath("dw")
DW_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DW_DIR.joinpath("smart_sales.db")
PREPARED_DATA_DIR = pathlib.Path("data").joinpath("prepared")

# ---------- CREATE SCHEMA ----------
def create_schema(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_dimension (
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
        CREATE TABLE IF NOT EXISTS product_dimension (
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
        CREATE TABLE IF NOT EXISTS sales_fact (
            TransactionID INTEGER PRIMARY KEY,
            SaleDate TEXT,
            CustomerID INTEGER,
            ProductID INTEGER,
            StoreID INTEGER,
            CampaignID INTEGER,
            SaleAmount REAL,
            DiscountPercent REAL,
            PaymentType TEXT,
            QuantitySold INTEGER,
            FOREIGN KEY (CustomerID) REFERENCES customer_dimension(CustomerID),
            FOREIGN KEY (ProductID) REFERENCES product_dimension(ProductID)
        )
    """)

# ---------- CLEAN PREVIOUS RECORDS ----------
def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    cursor.execute("DELETE FROM sales_fact")
    cursor.execute("DELETE FROM customer_dimension")
    cursor.execute("DELETE FROM product_dimension")

# ---------- INSERT FUNCTIONS ----------
def insert_customers(df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    df.to_sql("customer_dimension", cursor.connection, if_exists="append", index=False)

def insert_products(df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    df.to_sql("product_dimension", cursor.connection, if_exists="append", index=False)

def insert_sales(df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    if 'QuantitySold' not in df.columns:
        df['QuantitySold'] = 1  # default if missing
    df.to_sql("sales_fact", cursor.connection, if_exists="append", index=False)

# ---------- MAIN ETL FUNCTION ----------
def load_data_to_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        create_schema(cursor)
        delete_existing_records(cursor)

        # Load cleaned data
        customers_df = pd.read_csv(PREPARED_DATA_DIR / "C:\Projects\smart-store-foster-1\data\prepared\customers_data_prepared.csv")
        products_df = pd.read_csv(PREPARED_DATA_DIR / "C:\Projects\smart-store-foster-1\data\prepared\products_data_prepared.csv")
        sales_df = pd.read_csv(PREPARED_DATA_DIR / "C:\Projects\smart-store-foster-1\data\prepared\sales_data_prepared.csv")

        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        conn.commit()
        print("✅ Data successfully loaded into smart_sales.db.")
    except Exception as e:
        print("❌ Error:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    load_data_to_db()
