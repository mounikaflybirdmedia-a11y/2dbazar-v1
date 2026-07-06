<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

require 'db.php';

// Create a generic key-value store table if not exists for state syncing
$conn->query("CREATE TABLE IF NOT EXISTS app_state (
    store_key VARCHAR(100) PRIMARY KEY,
    store_value LONGTEXT
)");

$action = $_GET['action'] ?? '';

if ($action === 'set') {
    $key = $_GET['key'] ?? '';
    if (!$key) die(json_encode(["status"=>"error", "msg"=>"Missing key"]));
    
    $json = file_get_contents('php://input');
    
    $stmt = $conn->prepare("INSERT INTO app_state (store_key, store_value) VALUES (?, ?) ON DUPLICATE KEY UPDATE store_value=?");
    $stmt->bind_param("sss", $key, $json, $json);
    
    if ($stmt->execute()) {
        echo json_encode(["status"=>"success"]);
    } else {
        echo json_encode(["status"=>"error", "msg"=>$stmt->error]);
    }
    $stmt->close();
} 
elseif ($action === 'get_all') {
    $result = $conn->query("SELECT store_key, store_value FROM app_state");
    $db = [];
    if ($result) {
        while($row = $result->fetch_assoc()) {
            $db[$row['store_key']] = json_decode($row['store_value'], true);
        }
    }
    echo json_encode(["status"=>"success", "db"=>$db]);
}
else {
    echo json_encode(["status"=>"error", "msg"=>"Invalid action"]);
}
$conn->close();
?>
