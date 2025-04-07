<?php
include('db.php');

// 🛡️ Check before accessing
$page = $_GET['page'] ?? null;
$user = $_GET['user'] ?? null;


if ($page) {
    include("pages/$page");
}

if ($user) {
    $sql = "SELECT * FROM users WHERE username = '$user'";
    $result = mysqli_query($conn, $sql);
    while ($row = mysqli_fetch_assoc($result)) {
        echo $row['username'] . "<br>";
    }
}
?>

