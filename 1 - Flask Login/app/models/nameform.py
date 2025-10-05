# --- Importações ---
# Flask-WTF é uma extensão que integra o WTForms com o Flask, facilitando a criação e validação de formulários web.
# FlaskForm é a classe base para todos os formulários criados com Flask-WTF.
from flask_wtf import FlaskForm

# WTForms é uma biblioteca de renderização e validação de formulários para Python.
# StringField: Representa um campo de entrada de texto (<input type="text">).
# SubmitField: Representa um botão de envio (<input type="submit">).
from wtforms import StringField, SubmitField

# O módulo de validadores do WTForms fornece funções para validar os dados de entrada do formulário.
# DataRequired: É um validador que verifica se o campo foi preenchido e não está vazio.
from wtforms.validators import DataRequired

# --- Definição do Formulário ---

# Define a classe 'NameForm' que herda de 'FlaskForm'.
# Esta classe irá representar a estrutura do nosso formulário HTML.
# Cada atributo da classe que é uma instância de um tipo de campo (como StringField)
# será renderizado como um campo de formulário no template.
class NameForm(FlaskForm):
    # Define o campo 'name'.
    # O primeiro argumento ('Qual é o seu nome?') é o rótulo (label) que será exibido ao lado do campo no HTML.
    # O argumento 'validators' é uma lista de validadores a serem aplicados a este campo.
    # [DataRequired()] garante que o usuário deve digitar algo neste campo para que o formulário seja válido.
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    # Define o campo 'submit'.
    # O argumento ('Enviar') é o texto que aparecerá no botão de envio.
    submit = SubmitField('Enviar')