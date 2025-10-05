# Importações de pacotes e módulos necessários.
# Flask: Classe principal para criar a aplicação.
from flask import Flask
# Flask-Login: Gerenciamento de sessões de usuário.
from flask_login import LoginManager
# Importa as instâncias das extensões criadas em 'extensions.py'.
from extensions import db, bootstrap, moment, mail
# os: Módulo para interagir com o sistema operacional, usado aqui para construir caminhos de arquivo.
import os

from config import config

# Define o caminho absoluto para o diretório onde este arquivo está localizado.
# Garante que o caminho para o banco de dados SQLite seja sempre correto,
# independentemente de onde o script é executado.
basedir = os.path.abspath(os.path.dirname(__file__))

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  

def create_app(config_name):
    """
    Função Factory para criar e configurar a instância da aplicação Flask.
    Este padrão permite criar múltiplas instâncias da aplicação com diferentes configurações,
    o que é útil para testes e evita problemas de importação circular.
    """

    # Cria a instância principal da aplicação Flask.
    # __name__ é o nome do módulo Python atual. Flask usa isso para localizar recursos.
    app = Flask(__name__)
    
    # --- Configurações da Aplicação ---
    # Carrega as configurações do objeto apropriado conforme o ambiente (development, testing, production).
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # --- Inicialização das Extensões ---
    # Associa as instâncias das extensões (db, bootstrap, moment, mail) com a aplicação 'app'.
    # O método .init_app() permite que as extensões sejam inicializadas separadamente
    # da criação da aplicação, essencial para o padrão factory.
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)  # Inicializa o Flask-Mail para envio de e-mails
    login_manager.init_app(app)  # Inicializa o Flask-Login para gerenciamento de sessões

    # --- Criação do Banco de Dados ---
    # O 'app_context' garante que a aplicação esteja configurada corretamente
    # antes de interagir com suas extensões, como o banco de dados.
    with app.app_context():
        # db.create_all() cria todas as tabelas definidas nos modelos (em models.py)
        # que ainda não existem no banco de dados.
        # Em produção, recomenda-se usar ferramentas de migração como Flask-Migrate.
        db.create_all()

    # --- Registro dos Blueprints ---

    # Importa e registra o blueprint 'main' para a aplicação.
    # Isso organiza a aplicação em componentes modulares. 
    from .main import main as main_blueprint 
    app.register_blueprint(main_blueprint)   

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  

    # Retorna a instância da aplicação configurada.
    return app