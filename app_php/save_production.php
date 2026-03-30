<?php
require 'db_connect.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $machine_id = $_POST['machine_id'];
    $mold_id = $_POST['mold_id'];
    $good_parts = $_POST['good_parts'];
    $rejected_parts = $_POST['rejected_parts'];

    try {
        $sql = "INSERT INTO production_log (machine_id, mold_id, good_parts, rejected_parts) VALUES (?, ?, ?, ?)";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$machine_id, $mold_id, $good_parts, $rejected_parts]);

        echo "<h2>✅ Production Data Saved!</h2>";
        echo "<a href='production.php'>Go Back</a>";
    } catch (PDOException $e) {
        echo "Error: " . $e->getMessage();
    }
}
?>