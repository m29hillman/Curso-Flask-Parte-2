from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Redefinir Senha')

class PasswordResetForm(FlaskForm):
    password = PasswordField('Nova Senha', validators=[DataRequired(), EqualTo('password2', message='As senhas devem corresponder.')])
    password2 = PasswordField('Confirme a Nova Senha', validators=[DataRequired()])
    submit = SubmitField('Redefinir Senha')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    name = StringField('Nome Completo', validators=[DataRequired(), Length(2, 80)])
    password = PasswordField('Senha', validators=[DataRequired(), EqualTo('password2', message='As senhas devem corresponder.')])
    password2 = PasswordField('Confirme a Senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('O e-mail já está em uso.')