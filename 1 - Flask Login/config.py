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
    # Endereço do servidor SMTP para envio de e-mails (ex: 'smtp.googlemail.com').
    MAIL_SERVER = os.environ.get('MAIL_SERVER') 
    # Porta do servidor SMTP (ex: 587 para TLS).
    MAIL_PORT = int(os.environ.get('MAIL_PORT')) 
    # Define se a conexão deve usar TLS (Transport Layer Security).
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS').lower()
    # Nome de usuário para autenticação no servidor de e-mail.
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') 
    # Senha para autenticação no servidor de e-mail.
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') 
    # Prefixo adicionado ao assunto de todos os e-mails enviados pela aplicação (ex: '[Meu App]').
    FLASKY_MAIL_SUBJECT_PREFIX = os.environ.get('FLASKY_MAIL_SUBJECT_PREFIX') 
    # Endereço de e-mail que aparecerá como remetente.
    FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER') 
    # E-mail do administrador do site, usado para receber notificações e como papel especial no sistema.
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') 
    # Desativa o sistema de eventos do SQLAlchemy, que não é necessário e consome recursos.
    # É recomendado manter como False, a menos que você precise explicitamente dos eventos.
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
    # Ativa o modo de depuração do Flask, que fornece um debugger interativo no navegador em caso de erro.
    DEBUG = True 
    # Define a URI de conexão para o banco de dados de desenvolvimento (ex: um arquivo SQLite local).
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB') + ':///' + os.path.join(basedir, os.environ.get('DEV_DATABASE'))
    
class TestingConfig(Config): 
    """
    Configurações para ambiente de testes.
    Ativa o modo de teste e define um banco de dados separado (geralmente em memória).
    """
    # Ativa o modo de teste, que desabilita o tratamento de erros e facilita as asserções nos testes.
    TESTING = True 
    # Define a URI para um banco de dados de teste, garantindo que os testes não afetem os dados de desenvolvimento.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB') + ':///' + os.path.join(basedir, os.environ.get('TEST_DATABASE'))
    
class ProductionConfig(Config): 
    """
    Configurações para ambiente de produção.
    Desativa o modo debug e aponta para o banco de dados de produção.
    """
    # Define a URI de conexão para o banco de dados de produção (ex: PostgreSQL, MySQL em um servidor remoto).
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB') + ':///' + os.path.join(basedir, os.environ.get('DATABASE'))

# Dicionário que mapeia nomes de ambientes para suas classes de configuração.
config = { 
    'development': DevelopmentConfig, 
    'testing': TestingConfig, 
    'production': ProductionConfig, 
    'default': DevelopmentConfig 
}