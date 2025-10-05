# Importa a extensão Flask-Bootstrap para integrar o framework Bootstrap.
from flask_bootstrap import Bootstrap
# Importa a classe principal da extensão Flask-Moment, que integra a biblioteca moment.js.
from flask_moment import Moment
# Importa a extensão Flask-SQLAlchemy para integrar o banco de dados.
from flask_sqlalchemy import SQLAlchemy
# Importa a extensão Flask-Mail para enviar e-mails a partir da aplicação Flask.
from flask_mail import Mail

# Inicializa o Flask-Bootstrap na nossa aplicação.
bootstrap = Bootstrap()
# Inicializa o Flask-Moment na nossa aplicação.
moment = Moment()
# Inicializa o Flask-SQLAlchemy na nossa aplicação.
db = SQLAlchemy()
# Inicializa o Flask-Mail na nossa aplicação.
mail = Mail()
