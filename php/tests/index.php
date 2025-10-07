<?php
require 'db.php';
$pdo = getPDO();
$users = $pdo->query("SELECT * FROM users")->fetchAll();
?>
