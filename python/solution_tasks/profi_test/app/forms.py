from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    """Form for user login"""
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Пароль', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    """Form for user registration"""
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повторите пароль', 
                             validators=[DataRequired(), EqualTo('password')])

class TestForm(FlaskForm):
    """Base form for test questions"""
    pass

class KlimovTestForm(TestForm):
    """Form for Klimov's differential diagnostic questionnaire"""
    # Questions will be dynamically added based on methodology
    pass

class HollandTestForm(TestForm):
    """Form for Holland's occupational preferences questionnaire"""
    # Questions will be dynamically added based on methodology
    pass