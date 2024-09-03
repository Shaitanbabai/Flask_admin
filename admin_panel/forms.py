import logging
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from admin_panel.models import User

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            logger.error('Validation error: Username already exists.')
            raise ValidationError('Такое имя уже существует.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            logger.error('Validation error: Email already in use.')
            raise ValidationError('Такая почта уже используется.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    remember = BooleanField('Запомни меня')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                logger.error('Validation error: Username already exists.')
                raise ValidationError('Такое имя уже существует.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                logger.error('Validation error: Email already in use.')
                raise ValidationError('Такая почта уже используется.')


class UpdateUserForm(FlaskForm):
    role = SelectField('Role', choices=[('User', 'User'), ('Admin', 'Admin')], validators=[DataRequired()])
    status = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_role(self, role):
        if role.data not in ['User', 'Admin']:
            logger.error('Validation error: Invalid role selected.')
            raise ValidationError('Invalid role selected.')

    def validate_status(self, status):
        if status.data not in ['Active', 'Inactive']:
            logger.error('Validation error: Invalid status selected.')
            raise ValidationError('Invalid status selected.')

    def validate_user(self, user_id):
        user = User.query.get(user_id)
        if not user:
            logger.error('Validation error: User not found.')
            raise ValidationError('User not found.')
