<?php
// ONE-TIME CLEANUP: Remove current_user from shared DB (security fix)
// This prevents old stale session data from being synced to all users
require 'db.php';

$stmt = $conn->prepare("DELETE FROM app_state WHERE store_key = 'current_user'");
$stmt->execute();
$affected = $stmt->affected_rows;
$stmt->close();
$conn->close();

echo json_encode([
    "status" => "success",
    "msg" => "Removed current_user from shared DB. Rows deleted: " . $affected,
    "note" => "Sessions are now stored in sessionStorage (browser-only). Safe to delete this file after running."
]);
?>
