import os 
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env para o ambiente.
# Isso permite manter dados sensíveis (senhas, chaves) fora do código-fonte.
load_dotenv()

# Define o diretório base do projeto, útil para construir caminhos de arquivos.
basedir = os.path.abspath(os.path.dirname(__file__))  

class Config:
    """
    Classe base de configuração da aplicação Flask.
    Utiliza variáveis de ambiente para definir parâmetros sensíveis e flexíveis.
    Pode ser estendida para diferentes ambientes (desenvolvimento, teste, produção).
    """

    # Chave secreta usada para sessões e proteção contra CSRF.
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Configurações do servidor de e-mail.
    MAIL_SERVER = os.environ.get('MAIL_SERVER') 
    MAIL_PORT = int(os.environ.get('MAIL_PORT')) 
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS').lower()
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') 
    # Prefixo do assunto dos e-mails enviados pela aplicação.
    FLASKY_MAIL_SUBJECT_PREFIX = os.environ.get('FLASKY_MAIL_SUBJECT_PREFIX') 
    # Remetente padrão dos e-mails.
    FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER') 
    # E-mail do administrador para notificações.
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') 
    # Desativa rastreamento de modificações do SQLAlchemy para economizar recursos.
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    @staticmethod
    def init_app(app):
        """
        Método para inicialização customizada da aplicação.
        Pode ser sobrescrito nas subclasses para adicionar configurações específicas.
        """
        pass

class DevelopmentConfig(Config): 
    """
    Configurações específicas para ambiente de desenvolvimento.
    Ativa o modo debug e define o banco de dados de desenvolvimento.
    """
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB') + ':///' + os.path.join(basedir, os.environ.get('DEV_DATABASE'))
    
class TestingConfig(Config): 
    """
    Configurações para ambiente de testes.
    Ativa o modo de teste e define o banco de dados de testes.
    """
    TESTING = True 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB') + ':///' + os.path.join(basedir, os.environ.get('TEST_DATABASE'))
    
class ProductionConfig(Config): 
    """
    Configurações para ambiente de produção.
    Utiliza o banco de dados de produção.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB') + ':///' + os.path.join(basedir, os.environ.get('DATABASE'))

# Dicionário que mapeia nomes de ambientes para suas classes de configuração.
config = { 
    'development': DevelopmentConfig, 
    'testing': TestingConfig, 
    'production': ProductionConfig, 
    'default': DevelopmentConfig 
}