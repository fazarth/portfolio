<?php
session_start();

// Simple configuration
$PASSWORD = 'admin123'; // Change this!
$DATA_FILE = '../data.json';

// Handle Logout
if (isset($_GET['logout'])) {
    session_destroy();
    header('Location: index.php');
    exit;
}

// Handle Login
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['password'])) {
    if ($_POST['password'] === $PASSWORD) {
        $_SESSION['logged_in'] = true;
    } else {
        $error = "Password salah!";
    }
}

// Handle Save Data
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['data']) && isset($_SESSION['logged_in'])) {
    // Validate JSON
    $json = $_POST['data'];
    $decoded = json_decode($json);
    if ($decoded === null) {
        $error = "Invalid JSON data!";
    } else {
        file_put_contents($DATA_FILE, json_encode($decoded, JSON_PRETTY_PRINT));
        $success = "Data berhasil disimpan!";
    }
}

// Read Data
$currentData = file_exists($DATA_FILE) ? file_get_contents($DATA_FILE) : '{"products":[]}';

// Login Page
if (!isset($_SESSION['logged_in'])) {
?>
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio Admin</title>
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f0f2f5; }
        .login-box { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        input { padding: 8px; margin-bottom: 10px; width: 100%; box-sizing: border-box; }
        button { padding: 10px; width: 100%; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .error { color: red; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Admin Login</h2>
        <?php if (isset($error)) echo "<div class='error'>$error</div>"; ?>
        <form method="post">
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
<?php
    exit;
}
?>

<!-- Editor Page -->
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio Editor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f4f6f8; padding-bottom: 50px; }
        .editor-container { max-width: 800px; margin: 30px auto; }
        .card { margin-bottom: 20px; }
        textarea { font-family: monospace; min-height: 400px; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <span class="navbar-brand mb-0 h1">Portfolio Admin</span>
            <a href="?logout" class="btn btn-outline-light btn-sm">Logout</a>
        </div>
    </nav>

    <div class="container editor-container">
        <?php if (isset($success)) echo "<div class='alert alert-success'>$success <a href='../index.html' target='_blank'>Lihat Website</a></div>"; ?>
        <?php if (isset($error)) echo "<div class='alert alert-danger'>$error</div>"; ?>
        
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Edit Content (JSON)</h5>
                <small class="text-muted">Be careful with syntax!</small>
            </div>
            <div class="card-body">
                <form method="post">
                    <div class="mb-3">
                        <textarea class="form-control" name="data" id="jsonEditor"><?php echo htmlspecialchars($currentData); ?></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                </form>
            </div>
        </div>

        <div class="card">
            <div class="card-header">Preview</div>
            <div class="card-body">
                <pre id="preview" class="bg-light p-3 border rounded"></pre>
            </div>
        </div>
    </div>

    <script>
        const textarea = document.getElementById('jsonEditor');
        const preview = document.getElementById('preview');

        function updatePreview() {
            try {
                const obj = JSON.parse(textarea.value);
                preview.textContent = JSON.stringify(obj, null, 2);
                preview.style.color = 'black';
                textarea.classList.remove('is-invalid');
            } catch (e) {
                preview.textContent = "Invalid JSON: " + e.message;
                preview.style.color = 'red';
                textarea.classList.add('is-invalid');
            }
        }

        textarea.addEventListener('input', updatePreview);
        updatePreview();
    </script>
</body>
</html>
