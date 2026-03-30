<?php
require 'db_connect.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $machine_id = $_POST['line_id'];
    $reason = $_POST['reason'];
    $duration = $_POST['duration'];

    try {
        $sql = "INSERT INTO downtime_log (machine_id, reason, duration_min) VALUES (?, ?, ?)";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$machine_id, $reason, $duration]);

        echo "<h2>✅ Downtime Registered!</h2>";
        echo "<a href='index.php'>Go Back</a>";
    } catch (PDOException $e) {
        echo "Error: " . $e->getMessage();
    }
}
?>