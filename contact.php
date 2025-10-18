<?php
// Simple contact form handler
header('Content-Type: application/json; charset=UTF-8');

// Only allow POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Method Not Allowed']);
    exit;
}

// Read input
$name = isset($_POST['name']) ? trim($_POST['name']) : '';
$email = isset($_POST['email']) ? trim($_POST['email']) : '';
$message = isset($_POST['message']) ? trim($_POST['message']) : '';
$source = isset($_POST['source']) ? trim($_POST['source']) : '';

// Basic validation
$errors = [];
if ($name === '') { $errors[] = 'Вкажіть ім\'я.'; }
if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) { $errors[] = 'Невалідний email.'; }
if ($message === '') { $errors[] = 'Вкажіть повідомлення.'; }

if (!empty($errors)) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => implode(' ', $errors)]);
    exit;
}

// Compose email
$to = 'info@matviy.pp.ua';
$subject = 'Нове повідомлення з контактної форми';
$body = "Ім'я: {$name}\nEmail: {$email}\nСторінка: {$source}\n\nПовідомлення:\n{$message}\n";
$headers = [];
$headers[] = 'MIME-Version: 1.0';
$headers[] = 'Content-Type: text/plain; charset=UTF-8';
$headers[] = 'From: Website <no-reply@matviy.pp.ua>';
$headers[] = 'Reply-To: ' . $email;

$sent = @mail($to, '=?UTF-8?B?'.base64_encode($subject).'?=', $body, implode("\r\n", $headers));

if ($sent) {
    echo json_encode(['ok' => true, 'message' => 'Повідомлення надіслано. Дякую!']);
} else {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'Не вдалося надіслати повідомлення. Спробуйте пізніше.']);
}
