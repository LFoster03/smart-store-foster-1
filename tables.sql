CREATE TABLE customer_dimension (
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(255),
    Region VARCHAR(255),
    JoinDate DATE,
    LoyaltyPoints INT,
    CustomerSegment VARCHAR(255),
    LastPurchaseDate DATE
);

CREATE TABLE product_dimension (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(255),
    Category VARCHAR(255),
    UnitPrice DECIMAL(10, 2),
    StockQuantity INT,
    Supplier VARCHAR(255),
    AverageRating DECIMAL(3, 2)
);

CREATE TABLE sales_fact (
    TransactionID INT PRIMARY KEY,
    SaleDate DATE,
    CustomerID INT,
    ProductID INT,
    SaleAmount DECIMAL(10, 2),
    DiscountPercent DECIMAL(5, 2),
    PaymentType VARCHAR(50),
    QuantitySold INT,
    FOREIGN KEY (CustomerID) REFERENCES customer_dimension(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES product_dimension(ProductID)
);
