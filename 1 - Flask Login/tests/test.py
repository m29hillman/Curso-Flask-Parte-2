# Importa o módulo unittest para criar e rodar testes.
import unittest
# Importa o proxy 'current_app' do Flask, que aponta para a aplicação que está tratando a requisição.
from flask import current_app
# Importa a função factory 'create_app' e a instância do banco de dados 'db' da aplicação.
from app import create_app, db

# Define uma classe de teste que herda de unittest.TestCase.
class BasicTests(unittest.TestCase):
    # O método setUp é executado antes de cada método de teste.
    # É usado para configurar o ambiente de teste.
    def setUp(self):
        # Cria uma instância da aplicação Flask usando a configuração 'testing'.
        # Isso garante que estamos usando um ambiente isolado, como um banco de dados em memória ou de teste.
        self.app = create_app('testing')
        # Cria um contexto de aplicação. O contexto é necessário para que o Flask
        # saiba qual instância da aplicação está ativa, permitindo o uso de 'current_app'.
        self.app_context = self.app.app_context()
        # "Empurra" (ativa) o contexto da aplicação, tornando 'current_app' disponível para o teste.
        self.app_context.push()
        # Cria todas as tabelas do banco de dados definidas nos modelos.
        # Isso garante um banco de dados limpo para cada teste.
        db.create_all()

    # O método tearDown é executado após cada método de teste.
    # É usado para limpar o ambiente após a execução do teste.
    def tearDown(self):
        # Remove a sessão do banco de dados. Isso libera a conexão e garante que
        # não haja sessões pendentes entre os testes.
        db.session.remove()
        # Apaga todas as tabelas do banco de dados.
        # Isso limpa completamente o banco de dados, garantindo que os testes sejam independentes.
        db.drop_all()
        # "Remove" (desativa) o contexto da aplicação que foi ativado no setUp.
        self.app_context.pop()

    # Um método de teste. O nome deve começar com 'test_'.
    # Este teste verifica se a instância da aplicação foi criada com sucesso.
    def test_app_exists(self):
        # A asserção verifica se 'current_app' não é None.
        # Se 'current_app' existir, significa que a aplicação foi carregada corretamente no contexto.
        self.assertFalse(current_app is None)

    # Outro método de teste.
    # Este teste verifica se a aplicação está configurada para o modo de teste.
    def test_app_is_testing(self):
        # A asserção verifica se a chave de configuração 'TESTING' é True.
        # Isso confirma que a configuração 'testing' foi carregada corretamente pela factory create_app.
        self.assertTrue(current_app.config['TESTING'])