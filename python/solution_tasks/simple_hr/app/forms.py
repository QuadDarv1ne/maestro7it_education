from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateField, SelectField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, ValidationError
from app.models import Employee, Department, Position, User, Vacation
from app import db
from sqlalchemy import or_
import logging

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
    
    def validate_email(self, email):
        try:
            if self.original_email and email.data == self.original_email:
                return
            employee = Employee.query.filter_by(email=email.data).first()
            if employee:
                raise ValidationError('Сотрудник с таким email уже существует.')
        except Exception as e:
            logger.error(f"Error validating email: {str(e)}")
            raise ValidationError('Ошибка при проверке email.')
    
    def validate_employee_id(self, employee_id):
        try:
            if self.original_employee_id and employee_id.data == self.original_employee_id:
                return
            employee = Employee.query.filter_by(employee_id=employee_id.data).first()
            if employee:
                raise ValidationError('Сотрудник с таким табельным номером уже существует.')
        except Exception as e:
            logger.error(f"Error validating employee_id: {str(e)}")
            raise ValidationError('Ошибка при проверке табельного номера.')

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
            department = Department.query.filter_by(name=name.data).first()
            if department:
                raise ValidationError('Подразделение с таким названием уже существует.')
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
            position = Position.query.filter_by(title=title.data).first()
            if position:
                raise ValidationError('Должность с таким названием уже существует.')
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
            self.employee_id.choices = [(e.id, e.full_name) for e in Employee.query.all()]
        except Exception as e:
            logger.error(f"Error loading employee choices: {str(e)}")
            self.employee_id.choices = []
    
    def validate(self, extra_validators=None):
        try:
            if not super(VacationForm, self).validate(extra_validators=extra_validators):
                return False
            
            if self.start_date.data and self.end_date.data and self.start_date.data >= self.end_date.data:
                self.end_date.errors = list(self.end_date.errors) + ['Дата окончания должна быть позже даты начала']
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

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Подтверждение пароля', 
                             validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    role = SelectField('Роль', choices=[('hr', 'HR'), ('admin', 'Администратор')], validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

class ResetPasswordRequestForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Отправить')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Подтверждение пароля', 
                             validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Установить пароль')

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
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Пользователь с таким именем уже существует.')
        except Exception as e:
            logger.error(f"Error validating username: {str(e)}")
            raise ValidationError('Ошибка при проверке имени пользователя.')
    
    def validate_email(self, email):
        try:
            if self.original_email and email.data == self.original_email:
                return
            user = User.query.filter(
                or_(
                    User.email == email.data,
                    User.username == email.data  # This is a common mistake, checking for username instead
                )
            ).first()
            if user and user.email == email.data:
                raise ValidationError('Пользователь с таким email уже существует.')
        except Exception as e:
            logger.error(f"Error validating email: {str(e)}")
            raise ValidationError('Ошибка при проверке email.')
    
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