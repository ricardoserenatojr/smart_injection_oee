<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Input - Injection Mold 01</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #2c3e50; color: white; display: flex; justify-content: center; padding: 50px; }
        .form-card { background: #34495e; padding: 30px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        select, input { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; }
        button { width: 100%; padding: 10px; background: #e74c3c; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="form-card">
        <h2>⚠️ Machine Downtime Report</h2>
        <form action="save.php" method="POST">
            <label>Machine ID:</label>
            <select name="line_id">
                <option value="INJ_01">Injection Machine 01</option>
                <option value="INJ_02">Injection Machine 02</option>
            </select>

            <label>Current Mold:</label>
            <select name="mold_id">
                <option value="MOLD_A_PANEL">Mold A - Panel</option>
                <option value="MOLD_B_TRIM">Mold B - Trim</option>
            </select>

            <label>Downtime Reason:</label>
            <select name="reason">
                <option value="Mold Change">Mold Change</option>
                <option value="Material Shortage">Material Shortage</option>
                <option value="Mechanical Failure">Mechanical Failure</option>
                <option value="Quality Adjustment">Quality Adjustment</option>
            </select>

            <label>Duration (Minutes):</label>
            <input type="number" name="duration" required>

            <button type="submit">Register Downtime</button>
        </form>
    </div>
</body>
</html>