<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Регистрация пользователя</title>
<style>
    /* Общие стили страницы */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #74ABE2, #5563DE);
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }

    /* Карточка формы */
    .form-container {
        background: #fff;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        width: 400px;
        max-width: 90%;
    }

    h2 {
        text-align: center;
        color: #333;
        margin-bottom: 25px;
    }

    label {
        display: block;
        margin-bottom: 5px;
        font-weight: 600;
        color: #555;
    }

    input[type="text"],
    input[type="email"],
    input[type="tel"],
    input[type="password"] {
        width: 100%;
        padding: 12px 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
        font-size: 14px;
        transition: all 0.3s ease;
    }

    input[type="text"]:focus,
    input[type="email"]:focus,
    input[type="tel"]:focus,
    input[type="password"]:focus {
        border-color: #5563DE;
        box-shadow: 0 0 8px rgba(85, 99, 222, 0.3);
        outline: none;
    }

    .error {
        color: red;
        font-size: 0.85em;
        margin-bottom: 8px;
    }

    .success {
        color: green;
        font-size: 1em;
        margin-bottom: 8px;
    }

    input[type="submit"] {
        width: 100%;
        padding: 12px;
        background: #5563DE;
        color: #fff;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        font-size: 16px;
        transition: all 0.3s ease;
        margin-top: 10px;
    }

    input[type="submit"]:hover {
        background: #3f4fc8;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* Полоса силы пароля */
    #passwordStrength {
        width: 100%;
        height: 10px;
        background-color: #eee;
        border-radius: 5px;
        margin-top: 5px;
        overflow: hidden;
    }

    #passwordStrengthBar {
        height: 100%;
        width: 0%;
        background: linear-gradient(90deg, red, orange, green);
        transition: width 0.4s ease, background 0.4s ease;
    }

    #passwordRules {
        font-size: 0.85em;
        margin-top: 5px;
        list-style: none;
        padding-left: 0;
    }

    #passwordRules li {
        margin-bottom: 3px;
        color: red;
        display: flex;
        align-items: center;
        transition: color 0.3s ease;
    }

    #passwordRules li.valid {
        color: green;
    }

    /* Иконки для правил */
    #passwordRules li::before {
        content: '✖';
        display: inline-block;
        width: 18px;
        margin-right: 5px;
    }

    #passwordRules li.valid::before {
        content: '✔';
    }
</style>
</head>
<body>

<div class="form-container">
    <h2>Регистрация</h2>
    <form id="registrationForm" method="post" action="">
        <label for="fullname">ФИО</label>
        <input type="text" id="fullname" name="fullname" required>
        <div class="error" id="fullnameError"></div>

        <label for="phone">Телефон</label>
        <input type="tel" id="phone" name="phone" placeholder="+7 999 123-45-67" required>
        <div class="error" id="phoneError"></div>

        <label for="email">Email</label>
        <input type="email" id="email" name="email" required>
        <div class="error" id="emailError"></div>

        <label for="password">Пароль</label>
        <input type="password" id="password" name="password" required>
        <div id="passwordStrength"><div id="passwordStrengthBar"></div></div>
        <ul id="passwordRules">
            <li id="ruleLength">Минимум 8 символов</li>
            <li id="ruleUpper">Заглавная буква</li>
            <li id="ruleLower">Строчная буква</li>
            <li id="ruleNumber">Цифра</li>
            <li id="ruleSpecial">Спецсимвол (!@#$%^&* etc.)</li>
        </ul>
        <div class="error" id="passwordError"></div>

        <label for="confirm_password">Подтверждение пароля</label>
        <input type="password" id="confirm_password" name="confirm_password" required>
        <div class="error" id="confirmPasswordError"></div>

        <input type="submit" value="Зарегистрироваться">
    </form>
</div>

<script>
const form = document.getElementById('registrationForm');
const passwordInput = document.getElementById('password');
const strengthBar = document.getElementById('passwordStrengthBar');
const rules = {
    length: document.getElementById('ruleLength'),
    upper: document.getElementById('ruleUpper'),
    lower: document.getElementById('ruleLower'),
    number: document.getElementById('ruleNumber'),
    special: document.getElementById('ruleSpecial')
};

function updatePasswordStrength(password) {
    let score = 0;

    if (password.length >= 8) { score++; rules.length.classList.add('valid'); } else { rules.length.classList.remove('valid'); }
    if (/[A-Z]/.test(password)) { score++; rules.upper.classList.add('valid'); } else { rules.upper.classList.remove('valid'); }
    if (/[a-z]/.test(password)) { score++; rules.lower.classList.add('valid'); } else { rules.lower.classList.remove('valid'); }
    if (/[0-9]/.test(password)) { score++; rules.number.classList.add('valid'); } else { rules.number.classList.remove('valid'); }
    if (/[\W]/.test(password)) { score++; rules.special.classList.add('valid'); } else { rules.special.classList.remove('valid'); }

    let width = (score / 5) * 100 + '%';
    let color = 'red';
    if (score === 5) color = 'green';
    else if (score >= 3) color = 'orange';

    strengthBar.style.width = width;
    strengthBar.style.backgroundColor = color;
}

passwordInput.addEventListener('input', () => {
    updatePasswordStrength(passwordInput.value);
});

form.addEventListener('submit', function(event) {
    let isValid = true;
    document.querySelectorAll('.error').forEach(el => el.textContent = '');

    const fullname = document.getElementById('fullname').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = passwordInput.value;
    const confirmPassword = document.getElementById('confirm_password').value;

    if (!/^[а-яА-ЯёЁa-zA-Z\s]+$/.test(fullname)) {
        document.getElementById('fullnameError').textContent = "ФИО может содержать только буквы и пробелы.";
        isValid = false;
    }
    if (!/^[0-9\+\-\s]+$/.test(phone)) {
        document.getElementById('phoneError').textContent = "Телефон может содержать только цифры, '+', '-', пробелы.";
        isValid = false;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        document.getElementById('emailError').textContent = "Некорректный email.";
        isValid = false;
    }
    if (password.length < 8 || !/[A-Z]/.test(password) || !/[a-z]/.test(password) || !/[0-9]/.test(password) || !/[\W]/.test(password)) {
        document.getElementById('passwordError').textContent = "Пароль не соответствует требованиям.";
        isValid = false;
    }
    if (password !== confirmPassword) {
        document.getElementById('confirmPasswordError').textContent = "Пароли не совпадают.";
        isValid = false;
    }

    if (!isValid) event.preventDefault();
});
</script>

<?php
/**
 * Обработка регистрации пользователя
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 */
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $fullname = htmlspecialchars(trim($_POST['fullname']));
    $phone = htmlspecialchars(trim($_POST['phone']));
    $email = htmlspecialchars(trim($_POST['email']));
    $password = htmlspecialchars(trim($_POST['password']));
    $confirm_password = htmlspecialchars(trim($_POST['confirm_password']));

    $errors = [];

    if (!preg_match("/^[а-яА-ЯёЁa-zA-Z\s]+$/u", $fullname)) $errors[] = "ФИО может содержать только буквы и пробелы.";
    if (!preg_match("/^[0-9\+\-\s]+$/", $phone)) $errors[] = "Телефон может содержать только цифры, '+', '-', пробелы.";
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = "Некорректный email.";
    if (strlen($password) < 8 || !preg_match("/[A-Z]/", $password) || !preg_match("/[a-z]/", $password) || !preg_match("/[0-9]/", $password) || !preg_match("/[\W]/", $password)) {
        $errors[] = "Пароль должен содержать минимум 8 символов, заглавную и строчную буквы, цифру и спецсимвол.";
    }
    if ($password !== $confirm_password) $errors[] = "Пароли не совпадают.";

    if (empty($errors)) {
        $hashedPassword = password_hash($password, PASSWORD_BCRYPT);

        $user = [
            "ФИО" => $fullname,
            "Телефон" => $phone,
            "Email" => $email,
            "Пароль (хеш)" => $hashedPassword
        ];

        echo "<h3 style='color:green; text-align:center;'>Регистрация прошла успешно!</h3>";
        echo "<pre style='background:#f4f4f4;padding:10px;border-radius:8px;'>";
        print_r($user);
        echo "</pre>";
    } else {
        echo "<h3 style='color:red; text-align:center;'>Ошибки при заполнении формы:</h3><ul>";
        foreach ($errors as $error) echo "<li>$error</li>";
        echo "</ul>";
    }
}
?>
</body>
</html>
