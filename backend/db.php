<?php
// db.php - Database connection
$host = "localhost";
$user = "u816361417_FPiWm2QlK_2dbazar";
$pass = "2Dbazar@2026!";
$dbname = "u816361417_FPiWm2QlK_2dbazar";

$conn = new mysqli($host, $user, $pass, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$conn->set_charset("utf8mb4");
?>
