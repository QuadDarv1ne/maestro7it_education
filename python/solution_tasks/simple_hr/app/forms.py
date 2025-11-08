from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateField, SelectField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, ValidationError
from app.models import Employee, Department, Position, User, Vacation
from app import db
from sqlalchemy import or_
import logging
import re

# Set up logging
logger = logging.getLogger(__name__)

class EmployeeForm(FlaskForm):
    full_name = StringField('ФИО', validators=[DataRequired(), Length(max=150)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    employee_id = StringField('Табельный номер', validators=[DataRequired(), Length(max=50)])
    hire_date = DateField('Дата приема', validators=[DataRequired()])
    department_id = SelectField('Подразделение', coerce=int, validators=[DataRequired()])
    position_id = SelectField('Должность', coerce=int, validators=[DataRequired()])
    status = SelectField('Статус', choices=[('active', 'Активен'), ('dismissed', 'Уволен')], 
                        validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    
    def __init__(self, original_email=None, original_employee_id=None, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
        self.original_employee_id = original_employee_id
        try:
            self.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
            self.position_id.choices = [(p.id, p.title) for p in Position.query.all()]
        except Exception as e:
            logger.error(f"Error loading form choices: {str(e)}")
            self.department_id.choices = []
            self.position_id.choices = []
    
    def validate_full_name(self, full_name):
        """Validate full name format"""
        try:
            if not full_name.data:
                raise ValidationError('ФИО обязательно для заполнения.')
            
            # Check for at least two words (first name and last name)
            if len(full_name.data.strip().split()) < 2:
                raise ValidationError('Пожалуйста, введите полное ФИО (минимум имя и фамилия).')
            
            # Check for valid characters (letters, spaces, hyphens, apostrophes)
            if not re.match(r"^[а-яА-ЯёЁa-zA-Z\s\-']+$", full_name.data.strip()):
                raise ValidationError('ФИО может содержать только буквы, пробелы, дефисы и апострофы.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating full_name: {str(e)}")
            raise ValidationError('Ошибка при проверке ФИО.')
    
    def validate_email(self, email):
        try:
            if self.original_email and email.data == self.original_email:
                return
            
            if not email.data:
                raise ValidationError('Email обязателен для заполнения.')
            
            # Basic email format validation
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
                raise ValidationError('Неверный формат email.')
            
            employee = Employee.query.filter_by(email=email.data).first()
            if employee:
                raise ValidationError('Сотрудник с таким email уже существует.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating email: {str(e)}")
            raise ValidationError('Ошибка при проверке email.')
    
    def validate_employee_id(self, employee_id):
        try:
            if self.original_employee_id and employee_id.data == self.original_employee_id:
                return
            
            if not employee_id.data:
                raise ValidationError('Табельный номер обязателен для заполнения.')
            
            # Check for valid format (alphanumeric, hyphens, underscores)
            if not re.match(r"^[a-zA-Z0-9\-_]+$", employee_id.data):
                raise ValidationError('Табельный номер может содержать только буквы, цифры, дефисы и подчеркивания.')
            
            employee = Employee.query.filter_by(employee_id=employee_id.data).first()
            if employee:
                raise ValidationError('Сотрудник с таким табельным номером уже существует.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating employee_id: {str(e)}")
            raise ValidationError('Ошибка при проверке табельного номера.')
    
    def validate_hire_date(self, hire_date):
        """Validate hire date"""
        try:
            if not hire_date.data:
                raise ValidationError('Дата приема обязательна для заполнения.')
            
            from datetime import date
            if hire_date.data > date.today():
                raise ValidationError('Дата приема не может быть в будущем.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating hire_date: {str(e)}")
            raise ValidationError('Ошибка при проверке даты приема.')

class DepartmentForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Сохранить')
    
    def __init__(self, original_name=None, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
    
    def validate_name(self, name):
        try:
            if self.original_name and name.data == self.original_name:
                return
            
            if not name.data:
                raise ValidationError('Название подразделения обязательно для заполнения.')
            
            # Check for valid characters
            if not re.match(r"^[а-яА-ЯёЁa-zA-Z0-9\s\-'\"]+$", name.data.strip()):
                raise ValidationError('Название может содержать только буквы, цифры, пробелы, дефисы и кавычки.')
            
            department = Department.query.filter_by(name=name.data).first()
            if department:
                raise ValidationError('Подразделение с таким названием уже существует.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating department name: {str(e)}")
            raise ValidationError('Ошибка при проверке названия подразделения.')

class PositionForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Сохранить')
    
    def __init__(self, original_title=None, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
        self.original_title = original_title
    
    def validate_title(self, title):
        try:
            if self.original_title and title.data == self.original_title:
                return
            
            if not title.data:
                raise ValidationError('Название должности обязательно для заполнения.')
            
            # Check for valid characters
            if not re.match(r"^[а-яА-ЯёЁa-zA-Z0-9\s\-'\"]+$", title.data.strip()):
                raise ValidationError('Название должности может содержать только буквы, цифры, пробелы, дефисы и кавычки.')
            
            position = Position.query.filter_by(title=title.data).first()
            if position:
                raise ValidationError('Должность с таким названием уже существует.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating position title: {str(e)}")
            raise ValidationError('Ошибка при проверке названия должности.')

class VacationForm(FlaskForm):
    employee_id = SelectField('Сотрудник', coerce=int, validators=[DataRequired()])
    start_date = DateField('Дата начала', validators=[DataRequired()])
    end_date = DateField('Дата окончания', validators=[DataRequired()])
    type = SelectField('Тип отпуска', 
                      choices=[('paid', 'Оплачиваемый'), ('unpaid', 'Неоплачиваемый'), ('sick', 'Больничный')],
                      validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    
    def __init__(self, vacation_id=None, *args, **kwargs):
        super(VacationForm, self).__init__(*args, **kwargs)
        self.vacation_id = vacation_id
        try:
            # Load active employees only and sort by full name
            employees = Employee.query.filter_by(status='active').order_by(Employee.full_name).all()
            self.employee_id.choices = [(e.id, e.full_name) for e in employees]
            
            # If no employees found, provide a default option
            if not self.employee_id.choices:
                self.employee_id.choices = [("", "Нет доступных сотрудников")]
        except Exception as e:
            logger.error(f"Error loading employee choices: {str(e)}")
            self.employee_id.choices = [("", "Ошибка загрузки сотрудников")]
    
    def validate_start_date(self, start_date):
        """Validate start date"""
        try:
            if not start_date.data:
                raise ValidationError('Дата начала обязательна для заполнения.')
            
            from datetime import date
            if start_date.data > date(2100, 1, 1):
                raise ValidationError('Дата начала не может быть такой далекой в будущем.')
                
            # Check that start date is not in the past (optional validation)
            # Uncomment the following lines if you want to prevent past dates
            # if start_date.data < date.today():
            #     raise ValidationError('Дата начала не может быть в прошлом.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating start_date: {str(e)}")
            raise ValidationError('Ошибка при проверке даты начала.')
    
    def validate_end_date(self, end_date):
        """Validate end date"""
        try:
            if not end_date.data:
                raise ValidationError('Дата окончания обязательна для заполнения.')
            
            from datetime import date
            if end_date.data > date(2100, 1, 1):
                raise ValidationError('Дата окончания не может быть такой далекой в будущем.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating end_date: {str(e)}")
            raise ValidationError('Ошибка при проверке даты окончания.')
    
    def validate(self, extra_validators=None):
        try:
            if not super(VacationForm, self).validate(extra_validators=extra_validators):
                return False
            
            if self.start_date.data and self.end_date.data:
                if self.start_date.data > self.end_date.data:
                    self.end_date.errors = list(self.end_date.errors) + ['Дата окончания должна быть позже даты начала']
                    return False
                
                # Check if vacation is too long (more than 60 days)
                if (self.end_date.data - self.start_date.data).days > 60:
                    self.end_date.errors = list(self.end_date.errors) + ['Отпуск не может быть длиннее 60 дней']
                    return False
            
            # Check for overlapping vacations for the same employee
            if self.employee_id.data and self.start_date.data and self.end_date.data:
                # Query for overlapping vacations
                overlapping_query = Vacation.query.filter(
                    Vacation.employee_id == self.employee_id.data,
                    Vacation.start_date <= self.end_date.data,
                    Vacation.end_date >= self.start_date.data
                )
                
                # Exclude the current vacation being edited
                if self.vacation_id:
                    overlapping_query = overlapping_query.filter(Vacation.id != self.vacation_id)
                
                overlapping_vacations = overlapping_query.all()
                
                if overlapping_vacations:
                    self.employee_id.errors = list(self.employee_id.errors) + ['У сотрудника уже есть отпуск в выбранный период']
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error validating vacation form: {str(e)}")
            self.employee_id.errors = list(self.employee_id.errors) + ['Ошибка при проверке формы']
            return False

class OrderForm(FlaskForm):
    employee_id = SelectField('Сотрудник', coerce=int, validators=[DataRequired()])
    type = SelectField('Тип приказа',
                      choices=[('hire', 'Прием'), ('transfer', 'Перевод'), ('dismissal', 'Увольнение')],
                      validators=[DataRequired()])
    date_issued = DateField('Дата приказа', validators=[DataRequired()])
    new_department_id = SelectField('Новое подразделение', coerce=int, validators=[Optional()])
    new_position_id = SelectField('Новая должность', coerce=int, validators=[Optional()])
    submit = SubmitField('Сохранить')
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        try:
            self.employee_id.choices = [(e.id, e.full_name) for e in Employee.query.all()]
            self.new_department_id.choices = [("", "Не выбрано")]
            for d in Department.query.all():
                self.new_department_id.choices.append((str(d.id), d.name))
            self.new_position_id.choices = [("", "Не выбрано")]
            for p in Position.query.all():
                self.new_position_id.choices.append((str(p.id), p.title))
        except Exception as e:
            logger.error(f"Error loading order form choices: {str(e)}")
            self.employee_id.choices = []
            self.new_department_id.choices = [("", "Не выбрано")]
            self.new_position_id.choices = [("", "Не выбрано")]
    
    def validate_date_issued(self, date_issued):
        """Validate order date"""
        try:
            if not date_issued.data:
                raise ValidationError('Дата приказа обязательна для заполнения.')
            
            from datetime import date
            if date_issued.data > date.today():
                raise ValidationError('Дата приказа не может быть в будущем.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating date_issued: {str(e)}")
            raise ValidationError('Ошибка при проверке даты приказа.')
    
    def validate(self, extra_validators=None):
        try:
            if not super(OrderForm, self).validate(extra_validators=extra_validators):
                return False
            
            # For transfer orders, both new department and position are required
            if self.type.data == 'transfer':
                if not self.new_department_id.data or not self.new_position_id.data:
                    self.type.errors = list(self.type.errors) + ['Для перевода необходимо указать новое подразделение и должность']
                    return False
            
            # For dismissal orders, new department and position should not be set
            if self.type.data == 'dismissal':
                if self.new_department_id.data or self.new_position_id.data:
                    self.type.errors = list(self.type.errors) + ['При увольнении не нужно указывать новое подразделение или должность']
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error validating order form: {str(e)}")
            self.employee_id.errors = list(self.employee_id.errors) + ['Ошибка при проверке формы']
            return False

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
    
    def validate_username(self, username):
        """Validate username format"""
        try:
            if not username.data:
                raise ValidationError('Имя пользователя обязательно для заполнения.')
            
            # Check for valid characters
            if not re.match(r"^[a-zA-Z0-9_]+$", username.data):
                raise ValidationError('Имя пользователя может содержать только буквы, цифры и подчеркивания.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating username: {str(e)}")
            raise ValidationError('Ошибка при проверке имени пользователя.')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Подтверждение пароля', 
                             validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    role = SelectField('Роль', choices=[('hr', 'HR'), ('admin', 'Администратор')], validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
    
    def validate_username(self, username):
        """Validate username"""
        try:
            if not username.data:
                raise ValidationError('Имя пользователя обязательно для заполнения.')
            
            # Check length
            if len(username.data) < 3 or len(username.data) > 80:
                raise ValidationError('Имя пользователя должно быть от 3 до 80 символов.')
            
            # Check for valid characters
            if not re.match(r"^[a-zA-Z0-9_]+$", username.data):
                raise ValidationError('Имя пользователя может содержать только буквы, цифры и подчеркивания.')
            
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Пользователь с таким именем уже существует.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating username: {str(e)}")
            raise ValidationError('Ошибка при проверке имени пользователя.')
    
    def validate_email(self, email):
        """Validate email"""
        try:
            if not email.data:
                raise ValidationError('Email обязателен для заполнения.')
            
            # Basic email format validation
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
                raise ValidationError('Неверный формат email.')
            
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Пользователь с таким email уже существует.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating email: {str(e)}")
            raise ValidationError('Ошибка при проверке email.')
    
    def validate_password(self, password):
        """Validate password strength"""
        try:
            if not password.data:
                raise ValidationError('Пароль обязателен для заполнения.')
            
            # Check length
            if len(password.data) < 6:
                raise ValidationError('Пароль должен быть не менее 6 символов.')
            
            # Check for password strength (at least one letter and one digit)
            if not re.search(r"[a-zA-Z]", password.data) or not re.search(r"[0-9]", password.data):
                raise ValidationError('Пароль должен содержать хотя бы одну букву и одну цифру.')
                
            # Check for common weak passwords
            weak_passwords = ['password', '123456', 'qwerty', 'admin', 'user']
            if password.data.lower() in weak_passwords:
                raise ValidationError('Пожалуйста, выберите более сложный пароль.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating password: {str(e)}")
            raise ValidationError('Ошибка при проверке пароля.')

class ResetPasswordRequestForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Отправить')
    
    def validate_email(self, email):
        """Validate email for password reset"""
        try:
            if not email.data:
                raise ValidationError('Email обязателен для заполнения.')
            
            # Basic email format validation
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
                raise ValidationError('Неверный формат email.')
            
            user = User.query.filter_by(email=email.data).first()
            if not user:
                raise ValidationError('Пользователь с таким email не найден.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating email: {str(e)}")
            raise ValidationError('Ошибка при проверке email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Подтверждение пароля', 
                             validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Установить пароль')
    
    def validate_password(self, password):
        """Validate new password strength"""
        try:
            if not password.data:
                raise ValidationError('Пароль обязателен для заполнения.')
            
            # Check length
            if len(password.data) < 6:
                raise ValidationError('Пароль должен быть не менее 6 символов.')
            
            # Check for password strength (at least one letter and one digit)
            if not re.search(r"[a-zA-Z]", password.data) or not re.search(r"[0-9]", password.data):
                raise ValidationError('Пароль должен содержать хотя бы одну букву и одну цифру.')
                
            # Check for common weak passwords
            weak_passwords = ['password', '123456', 'qwerty', 'admin', 'user']
            if password.data.lower() in weak_passwords:
                raise ValidationError('Пожалуйста, выберите более сложный пароль.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating password: {str(e)}")
            raise ValidationError('Ошибка при проверке пароля.')

class UserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Пароль', validators=[Optional(), Length(min=6)])
    password2 = PasswordField('Подтверждение пароля', 
                             validators=[Optional(), EqualTo('password', message='Пароли должны совпадать')])
    role = SelectField('Роль', choices=[('hr', 'HR'), ('admin', 'Администратор')], validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    
    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        try:
            if self.original_username and username.data == self.original_username:
                return
            
            if not username.data:
                raise ValidationError('Имя пользователя обязательно для заполнения.')
            
            # Check length
            if len(username.data) < 3 or len(username.data) > 80:
                raise ValidationError('Имя пользователя должно быть от 3 до 80 символов.')
            
            # Check for valid characters
            if not re.match(r"^[a-zA-Z0-9_]+$", username.data):
                raise ValidationError('Имя пользователя может содержать только буквы, цифры и подчеркивания.')
            
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Пользователь с таким именем уже существует.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating username: {str(e)}")
            raise ValidationError('Ошибка при проверке имени пользователя.')
    
    def validate_email(self, email):
        try:
            if self.original_email and email.data == self.original_email:
                return
            
            if not email.data:
                raise ValidationError('Email обязателен для заполнения.')
            
            # Basic email format validation
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
                raise ValidationError('Неверный формат email.')
            
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Пользователь с таким email уже существует.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating email: {str(e)}")
            raise ValidationError('Ошибка при проверке email.')
    
    def validate_password(self, password):
        """Validate password strength when provided"""
        try:
            # If password is provided, validate it
            if password.data:
                # Check length
                if len(password.data) < 6:
                    raise ValidationError('Пароль должен быть не менее 6 символов.')
                
                # Check for password strength (at least one letter and one digit)
                if not re.search(r"[a-zA-Z]", password.data) or not re.search(r"[0-9]", password.data):
                    raise ValidationError('Пароль должен содержать хотя бы одну букву и одну цифру.')
                    
                # Check for common weak passwords
                weak_passwords = ['password', '123456', 'qwerty', 'admin', 'user']
                if password.data.lower() in weak_passwords:
                    raise ValidationError('Пожалуйста, выберите более сложный пароль.')
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validating password: {str(e)}")
            raise ValidationError('Ошибка при проверке пароля.')
    
    def validate(self, extra_validators=None):
        try:
            if not super(UserForm, self).validate(extra_validators=extra_validators):
                return False
            
            # Если это создание нового пользователя, пароль обязателен
            if not self.original_username and not self.password.data:
                self.password.errors = list(self.password.errors) + ['Пароль обязателен при создании пользователя']
                return False
            
            # Если указан пароль, проверяем его подтверждение
            if self.password.data and not self.password2.data:
                self.password2.errors = list(self.password2.errors) + ['Подтверждение пароля обязательно']
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error validating user form: {str(e)}")
            self.username.errors = list(self.username.errors) + ['Ошибка при проверке формы']
            return False

# New form for searching employees
class EmployeeSearchForm(FlaskForm):
    search = StringField('Поиск', validators=[Optional()])
    department_id = SelectField('Подразделение', coerce=int, validators=[Optional()])
    position_id = SelectField('Должность', coerce=int, validators=[Optional()])
    status = SelectField('Статус', choices=[('', 'Все'), ('active', 'Активен'), ('dismissed', 'Уволен')], 
                        validators=[Optional()])
    submit = SubmitField('Найти')
    
    def __init__(self, *args, **kwargs):
        super(EmployeeSearchForm, self).__init__(*args, **kwargs)
        try:
            # Add empty option for department and position
            self.department_id.choices = [("", "Все подразделения")]
            for d in Department.query.all():
                self.department_id.choices.append((d.id, d.name))
                
            self.position_id.choices = [("", "Все должности")]
            for p in Position.query.all():
                self.position_id.choices.append((p.id, p.title))
        except Exception as e:
            logger.error(f"Error loading search form choices: {str(e)}")
            self.department_id.choices = [("", "Все подразделения")]
            self.position_id.choices = [("", "Все должности")]

# New form for filtering reports
class ReportFilterForm(FlaskForm):
    start_date = DateField('Начальная дата', validators=[Optional()])
    end_date = DateField('Конечная дата', validators=[Optional()])
    department_id = SelectField('Подразделение', coerce=int, validators=[Optional()])
    employee_id = SelectField('Сотрудник', coerce=int, validators=[Optional()])
    submit = SubmitField('Фильтровать')
    
    def __init__(self, *args, **kwargs):
        super(ReportFilterForm, self).__init__(*args, **kwargs)
        try:
            # Add empty option for department
            self.department_id.choices = [("", "Все подразделения")]
            for d in Department.query.all():
                self.department_id.choices.append((d.id, d.name))
                
            # Add empty option for employee
            self.employee_id.choices = [("", "Все сотрудники")]
            for e in Employee.query.all():
                self.employee_id.choices.append((e.id, e.full_name))
        except Exception as e:
            logger.error(f"Error loading report filter form choices: {str(e)}")
            self.department_id.choices = [("", "Все подразделения")]
            self.employee_id.choices = [("", "Все сотрудники")]
    
    def validate(self, extra_validators=None):
        try:
            if not super(ReportFilterForm, self).validate(extra_validators=extra_validators):
                return False
            
            # Validate date range
            if self.start_date.data and self.end_date.data:
                if self.start_date.data > self.end_date.data:
                    self.end_date.errors = list(self.end_date.errors) + ['Конечная дата должна быть позже начальной']
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error validating report filter form: {str(e)}")
            return False