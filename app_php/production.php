<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Production Input - Injection</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #2c3e50; color: white; display: flex; justify-content: center; padding: 50px; }
        .form-card { background: #34495e; padding: 30px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); width: 350px; }
        select, input { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="form-card">
        <h2>📦 Production Report</h2>
        <form action="save_production.php" method="POST">
            <label>Machine ID:</label>
            <select name="machine_id">
                <option value="INJ_01">Injection Machine 01</option>
                <option value="INJ_02">Injection Machine 02</option>
            </select>

            <label>Mold ID:</label>
            <select name="mold_id">
                <option value="MOLD_A_PANEL">Mold A - Panel</option>
                <option value="MOLD_B_TRIM">Mold B - Trim</option>
            </select>

            <label>Good Parts Produced:</label>
            <input type="number" name="good_parts" required>

            <label>Rejected Parts:</label>
            <input type="number" name="rejected_parts" required>

            <button type="submit">Submit Production Data</button>
        </form>
    </div>
</body>
</html>