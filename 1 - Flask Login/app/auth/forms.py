# Importa as classes e funções necessárias
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

# Define o formulário de login do usuário
class LoginForm(FlaskForm):
    # Campo para o e-mail do usuário.
    # Validadores:
    # - DataRequired: Garante que o campo não seja enviado vazio.
    # - Email: Valida se o formato do texto é um e-mail válido.
    # - Length: Limita o comprimento máximo do e-mail para 120 caracteres.
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    # Campo para a senha do usuário.
    # Validadores:
    # - DataRequired: Garante que o campo não seja enviado vazio.
    password = PasswordField('Senha', validators=[DataRequired()])
    # Campo de caixa de seleção para a funcionalidade "Lembrar-me".
    remember_me = BooleanField('Lembrar-me')
    # Botão para submeter o formulário de login.
    submit = SubmitField('Entrar')

# Define o formulário para solicitar a redefinição de senha.
class PasswordResetRequestForm(FlaskForm):
    # Campo para o e-mail do usuário que solicita a redefinição.
    # Os validadores garantem que um e-mail válido e existente seja fornecido.
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    # Botão para submeter o pedido de redefinição.
    submit = SubmitField('Redefinir Senha')

# Define o formulário para efetivamente redefinir a senha com uma nova.
class PasswordResetForm(FlaskForm):
    # Campo para a nova senha.
    # Validadores:
    # - DataRequired: O campo não pode ser vazio.
    # - EqualTo: Compara o valor deste campo com 'password2' para garantir que as senhas coincidam.
    password = PasswordField('Nova Senha', validators=[DataRequired(), EqualTo('password2', message='As senhas devem corresponder.')])
    # Campo para confirmação da nova senha.
    password2 = PasswordField('Confirme a Nova Senha', validators=[DataRequired()])
    # Botão para submeter a nova senha.
    submit = SubmitField('Redefinir Senha')

# Define o formulário de registro para novos usuários.
class RegistrationForm(FlaskForm):
    # Campo para o e-mail do novo usuário.
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    # Campo para o nome completo do novo usuário.
    # O validador Length garante que o nome tenha entre 2 e 80 caracteres.
    name = StringField('Nome Completo', validators=[DataRequired(), Length(2, 80)])
    # Campo para a senha do novo usuário.
    # O validador EqualTo garante que a senha e sua confirmação sejam idênticas.
    password = PasswordField('Senha', validators=[DataRequired(), EqualTo('password2', message='As senhas devem corresponder.')])
    # Campo para confirmar a senha.
    password2 = PasswordField('Confirme a Senha', validators=[DataRequired()])
    # Botão para submeter o formulário de registro.
    submit = SubmitField('Registrar')

    # Validador customizado para o campo 'email'.
    # Este método é invocado automaticamente pelo WTForms durante a validação do formulário.
    def validate_email(self, field):
        # Verifica no banco de dados se já existe um usuário com o e-mail fornecido.
        if User.query.filter_by(email=field.data).first():
            # Se o e-mail já estiver em uso, lança um erro de validação com uma mensagem.
            raise ValidationError('O e-mail já está em uso.')