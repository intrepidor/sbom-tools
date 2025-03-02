CREATE DATABASE GroceryStore;

USE GroceryStore;

CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(50) NOT NULL
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    ProductName VARCHAR(100) NOT NULL,
    CategoryID INT,
    Price DECIMAL(10, 2) NOT NULL,
    Stock INT NOT NULL,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

INSERT INTO Categories (CategoryName) VALUES
('Fruits'),
('Vegetables'),
('Dairy'),
('Bakery'),
('Beverages');

INSERT INTO Products (ProductName, CategoryID, Price, Stock)
VALUES
    ('Apple', 1, 0.50, 100),
    ('Banana', 1, 0.30, 150),
    ('Carrot', 2, 0.20, 200),
    ('Milk', 3, 1.50, 50),
    ('Bread', 4, 2.00, 80),
    ('Orange Juice', 5, 3.00, 60),
    ('Grapes', 1, 2.50, 120),
    ('Tomato', 2, 0.40, 180),
    ('Cheese', 3, 2.50, 40),
    ('Croissant', 4, 1.50, 70),
    ('Coffee', 5, 5.00, 90),
    ('Strawberry', 1, 3.00, 110),
    ('Lettuce', 2, 1.00, 130),
    ('Yogurt', 3, 1.00, 60),
    ('Bagel', 4, 1.20, 85),
    ('Tea', 5, 4.00, 75),
    ('Blueberry', 1, 4.00, 95),
    ('Cucumber', 2, 0.60, 170),
    ('Butter', 3, 2.00, 55),
    ('Muffin', 4, 1.80, 65),
    ('Soda', 5, 1.50, 100),
    ('Pineapple', 1, 3.50, 80),
    ('Spinach', 2, 1.20, 140),
    ('Cream', 3, 1.50, 45),
    ('Donut', 4, 1.00, 75),
    ('Water', 5, 1.00, 200),
    ('Mango', 1, 2.00, 90),
    ('Pepper', 2, 0.80, 160),
    ('Ice Cream', 3, 3.00, 50),
    ('Baguette', 4, 2.50, 60),
    ('Juice', 5, 2.50, 110),
    ('Peach', 1, 2.20, 100),
    ('Onion', 2, 0.50, 190),
    ('Milkshake', 3, 2.00, 70),
    ('Cake', 4, 3.00, 55),
    ('Energy Drink', 5, 3.50, 85),
    ('Plum', 1, 2.80, 105),
    ('Garlic', 2, 0.30, 210),
    ('Whipped Cream', 3, 1.80, 65),
    ('Pastry', 4, 2.20, 75),
    ('Smoothie', 5, 4.50, 95),
    ('Kiwi', 1, 3.00, 115),
    ('Broccoli', 2, 1.50, 150),
    ('Sour Cream', 3, 1.20, 60),
    ('Pie', 4, 3.50, 50),
    ('Lemonade', 5, 2.00, 130),
    ('Pear', 1, 2.50, 125),
    ('Zucchini', 2, 1.00, 160),
    ('Custard', 3, 2.20, 55),
    ('Biscuit', 4, 1.50, 70),
    ('Hot Chocolate', 5, 3.00, 90);
