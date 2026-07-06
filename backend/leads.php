<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { exit(0); }

require 'db.php';

// ── Create table if not exists ─────────────────────
$conn->query("CREATE TABLE IF NOT EXISTS property_leads (
    id VARCHAR(100) PRIMARY KEY,
    propertyTitle VARCHAR(255),
    propertyId VARCHAR(100),
    userName VARCHAR(100),
    userPhone VARCHAR(30),
    userMessage TEXT,
    date VARCHAR(50),
    ts BIGINT,
    status VARCHAR(50) DEFAULT 'Properties Selected',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)");

$method = $_SERVER['REQUEST_METHOD'];
$action = $_GET['action'] ?? '';

// ── POST: Add a new lead ───────────────────────────
if ($method === 'POST' && $action === 'add_lead') {
    $data = json_decode(file_get_contents('php://input'), true);

    if (!$data) {
        echo json_encode(["status" => "error", "msg" => "No data received"]);
        exit;
    }

    $id    = $data['id']            ?? ('INQ-' . time());
    $title = $data['propertyTitle'] ?? '';
    $pid   = $data['propertyId']    ?? '';
    $name  = $data['userName']      ?? 'Guest';
    $phone = $data['userPhone']     ?? '';
    $msg   = $data['userMessage']   ?? '';
    $date  = $data['date']          ?? date('d/m/Y');
    $ts    = $data['ts']            ?? time() * 1000;

    $stmt = $conn->prepare("INSERT INTO property_leads (id, propertyTitle, propertyId, userName, userPhone, userMessage, date, ts, status) VALUES (?,?,?,?,?,?,?,?,'Properties Selected')");
    $stmt->bind_param("sssssssi", $id, $title, $pid, $name, $phone, $msg, $date, $ts);

    if ($stmt->execute()) {
        echo json_encode(["status" => "success", "msg" => "Lead saved!"]);
    } else {
        echo json_encode(["status" => "error", "msg" => $stmt->error]);
    }
    $stmt->close();
}

// ── GET: Fetch all leads ───────────────────────────
elseif ($method === 'GET' && $action === 'get_leads') {
    $result = $conn->query("SELECT * FROM property_leads ORDER BY ts DESC");
    $leads = [];
    if ($result) {
        while ($row = $result->fetch_assoc()) {
            $leads[] = $row;
        }
    }
    echo json_encode(["status" => "success", "leads" => $leads]);
}

// ── GET: Update lead status ────────────────────────
elseif ($method === 'GET' && $action === 'update_status') {
    $id     = $_GET['id']     ?? '';
    $status = $_GET['status'] ?? '';

    if (!$id || !$status) {
        echo json_encode(["status" => "error", "msg" => "Missing id or status"]);
        exit;
    }

    $stmt = $conn->prepare("UPDATE property_leads SET status=? WHERE id=?");
    $stmt->bind_param("ss", $status, $id);

    if ($stmt->execute()) {
        echo json_encode(["status" => "success"]);
    } else {
        echo json_encode(["status" => "error", "msg" => $stmt->error]);
    }
    $stmt->close();
}

else {
    echo json_encode(["status" => "error", "msg" => "Invalid action"]);
}

$conn->close();
?>
