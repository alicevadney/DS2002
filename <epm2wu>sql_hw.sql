-- Question 1
SELECT * FROM `country` WHERE country.Continent = "South America";

-- Question 2
SELECT Name, Population from country WHERE Name = 'Germany';

-- Question 3
SELECT Name from city WHERE CountryCode = ‘JPN’;

-- Question 4
SELECT * from country WHERE country.Continent = 'Africa' ORDER BY Population DESC LIMIT 3;

-- Question 5
SELECT Name, LifeExpectancy from country 
WHERE country.Population BETWEEN 1000000 AND 5000000;

-- Question 6
SELECT country.Name FROM country
JOIN countrylanguage ON country.Code = countrylanguage.CountryCode
WHERE countrylanguage.Language = 'French';

-- Question 7
SELECT * FROM Album WHERE ArtistId = 1;

-- Question 8
SELECT Customer.FirstName, Customer.LastName, Customer.Email FROM Customer 
WHERE Customer.Country = 'Brazil';

-- Question 9
SELECT DISTINCT Playlist.Name FROM `Playlist`;

-- Question 10
SELECT Name FROM Playlist;
SELECT COUNT(*) FROM Track
JOIN Genre ON Track.GenreID = Genre.GenreID
WHERE Genre.Name = 'Rock';

-- Question 11
SELECT e1.EmployeeID, e1.FirstName, e1.LastName FROM Employee e1 
JOIN Employee e2 ON e1.ReportsTo = e2.EmployeeID 
WHERE e2.FirstName = 'Nancy' AND e2.LastName = 'Edwards';

-- Question 12
SELECT Customer.CustomerID, Customer.FirstName, Customer.LastName, SUM(Invoice.Total)
FROM Customer
JOIN Invoice ON Customer.CustomerID = Invoice.CustomerID
GROUP BY Customer.CustomerID, Customer.FirstName, Customer.LastName;

-- PART 2: I designed a bakery

-- Question 1: the database will have three tables: Customer, Product, and Order
CREATE DATABASE Bakery;

-- Question 2

-- Customer
CREATE TABLE Customer ( CustomerID INT PRIMARY KEY, FirstName VARCHAR(50), 
LastName VARCHAR(50), Phone VARCHAR(15)); 

-- Product
CREATE TABLE Product ( ProductID INT PRIMARY KEY, ProductName VARCHAR(50), 
Category VARCHAR(50), Price DECIMAL(10, 2) ); 

-- Orders
CREATE TABLE Orders ( OrderID INT PRIMARY KEY, CustomerID INT, ProductID INT, 
OrderDate DATE, Quantity INT, FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID), 
FOREIGN KEY (ProductID) REFERENCES Products(ProductID) );

-- Question 3
-- Customer
INSERT INTO Customer (CustomerID, FirstName, LastName, Phone, Email) 
VALUES (1, John, 'Smith', '123-456-7890'), (2, 'Bob', 'Jones', '234-567-8901'), 
(3, Avery, 'Williams', '345-678-9012'), (4, 'David', 'Brown', '456-789-0123'), 
(5, 'Emma', 'Jones', '567-890-1234'); 

-- Products
INSERT INTO Products (ProductID, ProductName, Category, Price) 
VALUES (1, 'Chocolate Cake', 'Cake', 15.99), (2, 'Croissant', 'Pastry', 2.99), 
(3, 'Blueberry Muffin', 'Muffin', 3.49), (4, 'Bagel', 'Bread', 1.99), 
(5, 'Apple Pie', 'Pie', 12.49);

-- Orders
INSERT INTO Orders (OrderID, CustomerID, ProductID, OrderDate, Quantity) 
VALUES (1, 1, 1, '2024-09-01', 1), (2, 2, 2, '2024-09-02', 3), 
(3, 3, 3, '2024-09-03', 2), (4, 4, 4, '2024-09-04', 5), (5, 5, 5, '2024-09-05', 1);


-- Question 4

-- Query 1: find the total quantity ordered of each product
SELECT Product.ProductName, SUM(Orders.Quantity) AS TotalQuantity
FROM Orders
JOIN Product ON Orders.ProductID = Product.ProductID
GROUP BY Product.ProductName;

-- Query 2: find all customers who ordered a croissant
SELECT DISTINCT Customer.FirstName, Customer.LastName
FROM Orders
JOIN Customer ON Orders.CustomerID = Customer.CustomerID
JOIN Product ON Orders.ProductID = Product.ProductID
WHERE Product.ProductName = 'Chocolate Cake';

-- Query 3: find the total revenue for the bakery
SELECT SUM(Orders.Quantity * Product.Price)
FROM Orders
JOIN Product ON Orders.ProductID = Product.ProductID;