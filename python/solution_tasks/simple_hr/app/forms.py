from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateField, SelectField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, ValidationError
from app.models import Employee, Department, Position, User
from app import db

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
        self.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
        self.position_id.choices = [(p.id, p.title) for p in Position.query.all()]
    
    def validate_email(self, email):
        if self.original_email and email.data == self.original_email:
            return
        employee = Employee.query.filter_by(email=email.data).first()
        if employee:
            raise ValidationError('Сотрудник с таким email уже существует.')
    
    def validate_employee_id(self, employee_id):
        if self.original_employee_id and employee_id.data == self.original_employee_id:
            return
        employee = Employee.query.filter_by(employee_id=employee_id.data).first()
        if employee:
            raise ValidationError('Сотрудник с таким табельным номером уже существует.')

class DepartmentForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Сохранить')
    
    def __init__(self, original_name=None, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
    
    def validate_name(self, name):
        if self.original_name and name.data == self.original_name:
            return
        department = Department.query.filter_by(name=name.data).first()
        if department:
            raise ValidationError('Подразделение с таким названием уже существует.')

class PositionForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Сохранить')
    
    def __init__(self, original_title=None, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
        self.original_title = original_title
    
    def validate_title(self, title):
        if self.original_title and title.data == self.original_title:
            return
        position = Position.query.filter_by(title=title.data).first()
        if position:
            raise ValidationError('Должность с таким названием уже существует.')

class VacationForm(FlaskForm):
    employee_id = SelectField('Сотрудник', coerce=int, validators=[DataRequired()])
    start_date = DateField('Дата начала', validators=[DataRequired()])
    end_date = DateField('Дата окончания', validators=[DataRequired()])
    type = SelectField('Тип отпуска', 
                      choices=[('paid', 'Оплачиваемый'), ('unpaid', 'Неоплачиваемый'), ('sick', 'Больничный')],
                      validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    
    def __init__(self, *args, **kwargs):
        super(VacationForm, self).__init__(*args, **kwargs)
        self.employee_id.choices = [(e.id, e.full_name) for e in Employee.query.all()]
    
    def validate(self, extra_validators=None):
        if not super(VacationForm, self).validate(extra_validators=extra_validators):
            return False
        
        if self.start_date.data and self.end_date.data and self.start_date.data >= self.end_date.data:
            self.end_date.errors = list(self.end_date.errors) + ['Дата окончания должна быть позже даты начала']
            return False
        
        return True

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
        self.employee_id.choices = [(e.id, e.full_name) for e in Employee.query.all()]
        self.new_department_id.choices = [('', 'Не выбрано')] + [(d.id, d.name) for d in Department.query.all()]
        self.new_position_id.choices = [('', 'Не выбрано')] + [(p.id, p.title) for p in Position.query.all()]

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
        if self.original_username and username.data == self.original_username:
            return
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Пользователь с таким именем уже существует.')
    
    def validate_email(self, email):
        if self.original_email and email.data == self.original_email:
            return
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Пользователь с таким email уже существует.')
    
    def validate(self, extra_validators=None):
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
