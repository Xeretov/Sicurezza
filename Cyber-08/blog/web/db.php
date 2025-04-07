<?php
$conn = mysqli_connect('db', 'root', 'root', 'test');
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
?>
