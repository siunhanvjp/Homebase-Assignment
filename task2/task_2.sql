
--Product Information TABLE
CREATE TABLE ProductInformation (
    ProductID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Price DECIMAL(10, 2) NOT NULL CHECK (Price >= 0),
    QuantityInStock INT NOT NULL CHECK (QuantityInStock >= 0),
    ProductType VARCHAR(50)
);

--Customer Information TABLE
CREATE TABLE CustomerInformation (
    CustomerID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Address VARCHAR(255),
    PhoneNumber VARCHAR(15)
);

-- Order Table
CREATE TABLE Order (
    OrderID SERIAL PRIMARY KEY,
    OrderDate DATE DEFAULT CURRENT_DATE,
    CustomerID INT REFERENCES CustomerInformation(CustomerID) ON DELETE CASCADE,
    OrderStatus VARCHAR(50) DEFAULT 'Pending' CHECK (OrderStatus IN ('Pending', 'Shipped', 'Delivered'))
);

-- OrderDetails Table
CREATE TABLE OrderDetails (
    OrderDetailID SERIAL PRIMARY KEY,
    OrderID INT REFERENCES Order(OrderID) ON DELETE CASCADE,
    ProductID INT REFERENCES ProductInformation(ProductID) ON DELETE CASCADE,
    QuantityOrdered INT NOT NULL CHECK (QuantityOrdered > 0)
);

-- InventoryTransaction Table
CREATE TABLE InventoryTransaction (
    TransactionID SERIAL PRIMARY KEY,
    ProductID INT REFERENCES ProductInformation(ProductID) ON DELETE CASCADE,
    TransactionDate DATE DEFAULT CURRENT_DATE,
    QuantityIn INT CHECK (QuantityIn >= 0),
    QuantityOut INT CHECK (QuantityOut >= 0)
);