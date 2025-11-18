"""
Валидаторы для проверки данных
"""
import re
from datetime import datetime, date


class ValidationError(Exception):
    """Исключение для ошибок валидации"""
    pass


class Validator:
    """Базовый класс для валидаторов"""
    
    @staticmethod
    def validate_email(email):
        """Валидация email адреса"""
        if not email:
            raise ValidationError("Email обязателен для заполнения")
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Некорректный формат email")
        
        if len(email) > 120:
            raise ValidationError("Email не может быть длиннее 120 символов")
        
        return True
    
    @staticmethod
    def validate_phone(phone):
        """Валидация номера телефона"""
        if not phone:
            return True  # Phone is optional
        
        # Remove spaces, dashes, parentheses
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        
        # Check if it's a valid phone number (10-15 digits, optionally starting with +)
        pattern = r'^\+?[0-9]{10,15}$'
        if not re.match(pattern, cleaned):
            raise ValidationError("Некорректный формат телефона")
        
        return True
    
    @staticmethod
    def validate_password(password):
        """Валидация пароля"""
        if not password:
            raise ValidationError("Пароль обязателен для заполнения")
        
        if len(password) < 8:
            raise ValidationError("Пароль должен быть не менее 8 символов")
        
        if len(password) > 128:
            raise ValidationError("Пароль не может быть длиннее 128 символов")
        
        # Check for at least one letter
        if not re.search(r"[a-zA-Z]", password):
            raise ValidationError("Пароль должен содержать хотя бы одну букву")
        
        # Check for at least one digit
        if not re.search(r"[0-9]", password):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру")
        
        # Check for at least one special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Пароль должен содержать хотя бы один специальный символ")
        
        # Check for common weak passwords
        weak_passwords = [
            'password', '12345678', 'qwerty123', 'admin123', 'user1234',
            'password123', 'test1234', 'welcome1', 'letmein1'
        ]
        if password.lower() in weak_passwords:
            raise ValidationError("Пожалуйста, выберите более сложный пароль")
        
        return True
    
    @staticmethod
    def validate_username(username):
        """Валидация имени пользователя"""
        if not username:
            raise ValidationError("Имя пользователя обязательно для заполнения")
        
        if len(username) < 3:
            raise ValidationError("Имя пользователя должно быть не менее 3 символов")
        
        if len(username) > 80:
            raise ValidationError("Имя пользователя не может быть длиннее 80 символов")
        
        # Only allow alphanumeric characters, underscores, and hyphens
        pattern = r'^[a-zA-Z0-9_-]+$'
        if not re.match(pattern, username):
            raise ValidationError("Имя пользователя может содержать только буквы, цифры, _ и -")
        
        return True
    
    @staticmethod
    def validate_date(date_value, field_name="Дата"):
        """Валидация даты"""
        if not date_value:
            raise ValidationError(f"{field_name} обязательна для заполнения")
        
        if isinstance(date_value, str):
            try:
                date_value = datetime.strptime(date_value, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError(f"{field_name} должна быть в формате YYYY-MM-DD")
        
        if not isinstance(date_value, date):
            raise ValidationError(f"{field_name} должна быть корректной датой")
        
        return True
    
    @staticmethod
    def validate_date_range(start_date, end_date):
        """Валидация диапазона дат"""
        if not start_date or not end_date:
            raise ValidationError("Дата начала и окончания обязательны")
        
        if end_date < start_date:
            raise ValidationError("Дата окончания не может быть раньше даты начала")
        
        return True
    
    @staticmethod
    def validate_string_length(value, field_name, min_length=1, max_length=255):
        """Валидация длины строки"""
        if not value:
            raise ValidationError(f"{field_name} обязательно для заполнения")
        
        if len(value) < min_length:
            raise ValidationError(f"{field_name} должно быть не менее {min_length} символов")
        
        if len(value) > max_length:
            raise ValidationError(f"{field_name} не может быть длиннее {max_length} символов")
        
        return True
    
    @staticmethod
    def validate_choice(value, choices, field_name="Значение"):
        """Валидация выбора из списка"""
        if not value:
            raise ValidationError(f"{field_name} обязательно для заполнения")
        
        if value not in choices:
            raise ValidationError(f"{field_name} должно быть одним из: {', '.join(choices)}")
        
        return True
    
    @staticmethod
    def validate_employee_id(employee_id):
        """Валидация табельного номера"""
        if not employee_id:
            raise ValidationError("Табельный номер обязателен")
        
        # Typically 3-20 alphanumeric characters
        if len(employee_id) < 3 or len(employee_id) > 20:
            raise ValidationError("Табельный номер должен быть от 3 до 20 символов")
        
        # Allow alphanumeric and some special characters
        pattern = r'^[A-Z0-9\-]+$'
        if not re.match(pattern, employee_id.upper()):
            raise ValidationError("Табельный номер может содержать только буквы, цифры и дефис")
        
        return True
    
    @staticmethod
    def validate_positive_integer(value, field_name="Значение"):
        """Валидация положительного целого числа"""
        try:
            int_value = int(value)
            if int_value <= 0:
                raise ValidationError(f"{field_name} должно быть положительным числом")
            return True
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} должно быть целым числом")
    
    @staticmethod
    def validate_salary(salary):
        """Валидация зарплаты"""
        if salary is None:
            return True  # Salary is optional
        
        try:
            salary_value = float(salary)
            if salary_value < 0:
                raise ValidationError("Зарплата не может быть отрицательной")
            if salary_value > 10000000:  # 10 млн максимум
                raise ValidationError("Зарплата превышает допустимый максимум")
            return True
        except (ValueError, TypeError):
            raise ValidationError("Зарплата должна быть числом")
    
    @staticmethod
    def validate_birth_date(birth_date):
        """Валидация даты рождения"""
        if birth_date is None:
            return True  # Birth date is optional
        
        if isinstance(birth_date, str):
            try:
                birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("Дата рождения должна быть в формате YYYY-MM-DD")
        
        # Проверка что дата рождения не в будущем
        if birth_date > datetime.now().date():
            raise ValidationError("Дата рождения не может быть в будущем")
        
        # Проверка минимального возраста (16 лет)
        today = datetime.now().date()
        min_age = 16
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        
        if age < min_age:
            raise ValidationError(f"Минимальный возраст для трудоустройства: {min_age} лет")
        
        # Проверка максимального возраста (100 лет)
        if age > 100:
            raise ValidationError("Некорректная дата рождения")
        
        return True
    
    @staticmethod
    def validate_future_date(date_value, field_name="Дата"):
        """Проверка что дата не в прошлом"""
        if isinstance(date_value, str):
            date_value = datetime.strptime(date_value, '%Y-%m-%d').date()
        
        if date_value < datetime.now().date():
            raise ValidationError(f"{field_name} не может быть в прошлом")
        
        return True
    
    @staticmethod
    def validate_past_date(date_value, field_name="Дата"):
        """Проверка что дата не в будущем"""
        if isinstance(date_value, str):
            date_value = datetime.strptime(date_value, '%Y-%m-%d').date()
        
        if date_value > datetime.now().date():
            raise ValidationError(f"{field_name} не может быть в будущем")
        
        return True


class EmployeeValidator(Validator):
    """Валидатор для сотрудников"""
    
    @staticmethod
    def validate_create(data):
        """Валидация данных для создания сотрудника"""
        errors = []
        
        try:
            Validator.validate_string_length(data.get('full_name', ''), 'ФИО', 3, 150)
        except ValidationError as e:
            errors.append(str(e))
        
        try:
            Validator.validate_email(data.get('email', ''))
        except ValidationError as e:
            errors.append(str(e))
        
        try:
            Validator.validate_employee_id(data.get('employee_id', ''))
        except ValidationError as e:
            errors.append(str(e))
        
        try:
            Validator.validate_date(data.get('hire_date', ''), 'Дата найма')
            Validator.validate_past_date(data.get('hire_date', ''), 'Дата найма')
        except ValidationError as e:
            errors.append(str(e))
        
        # Валидация опциональных полей
        if 'birth_date' in data and data.get('birth_date'):
            try:
                Validator.validate_birth_date(data.get('birth_date'))
            except ValidationError as e:
                errors.append(str(e))
        
        if 'phone' in data and data.get('phone'):
            try:
                Validator.validate_phone(data.get('phone'))
            except ValidationError as e:
                errors.append(str(e))
        
        if 'salary' in data and data.get('salary'):
            try:
                Validator.validate_salary(data.get('salary'))
            except ValidationError as e:
                errors.append(str(e))
        
        if errors:
            raise ValidationError('; '.join(errors))
        
        return True


class VacationValidator(Validator):
    """Валидатор для отпусков"""
    
    @staticmethod
    def validate_create(data):
        """Валидация данных для создания отпуска"""
        errors = []
        
        try:
            Validator.validate_date(data.get('start_date', ''), 'Дата начала')
        except ValidationError as e:
            errors.append(str(e))
        
        try:
            Validator.validate_date(data.get('end_date', ''), 'Дата окончания')
        except ValidationError as e:
            errors.append(str(e))
        
        try:
            Validator.validate_date_range(
                data.get('start_date', ''),
                data.get('end_date', '')
            )
        except ValidationError as e:
            errors.append(str(e))
        
        try:
            Validator.validate_choice(
                data.get('type', ''),
                ['paid', 'unpaid', 'sick'],
                'Тип отпуска'
            )
        except ValidationError as e:
            errors.append(str(e))
        
        if errors:
            raise ValidationError('; '.join(errors))
        
        return True
