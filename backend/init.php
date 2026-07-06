<?php
require 'db.php';

$tables = [
    "CREATE TABLE IF NOT EXISTS users (
        id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        password VARCHAR(100),
        role VARCHAR(50),
        phone VARCHAR(20),
        location VARCHAR(100)
    )",
    "CREATE TABLE IF NOT EXISTS properties (
        id VARCHAR(50) PRIMARY KEY,
        title VARCHAR(255),
        type VARCHAR(50),
        price INT,
        area VARCHAR(50),
        location VARCHAR(100),
        facing VARCHAR(50),
        floors INT,
        parking BOOLEAN,
        img TEXT,
        owner VARCHAR(100),
        contact VARCHAR(20)
    )",
    "CREATE TABLE IF NOT EXISTS property_inquiries (
        id VARCHAR(50) PRIMARY KEY,
        propertyTitle VARCHAR(255),
        propertyId VARCHAR(50),
        userId VARCHAR(50),
        date VARCHAR(50),
        ts BIGINT,
        status VARCHAR(50)
    )"
];

echo "<h2>Initializing Database</h2>";

foreach ($tables as $sql) {
    if ($conn->query($sql) === TRUE) {
        echo "<p style='color:green;'>Table created successfully or already exists.</p>";
    } else {
        echo "<p style='color:red;'>Error creating table: " . $conn->error . "</p>";
    }
}
echo "<p><b>Database Initialization Complete!</b></p>";
echo "<a href='api.php'>Test API</a>";
$conn->close();
?>
