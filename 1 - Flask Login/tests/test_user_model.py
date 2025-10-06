# Importa os módulos necessários para os testes.
import unittest
import time
from app.models import User, Anonymous, Role, Permission
from app import db, create_app

# Define uma suíte de testes para o modelo User.
class UserModelTestCase(unittest.TestCase):
    # O método setUp é executado antes de cada teste.
    def setUp(self):
        # Cria uma instância da aplicação com a configuração de 'testing'.
        self.app = create_app('testing')
        # Cria e empurra um contexto de aplicação para que 'current_app' funcione.
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Cria todas as tabelas do banco de dados em memória.
        db.create_all()
        # Insere os papéis (roles) padrão no banco de dados.
        Role.insert_roles()
    
    # O método tearDown é executado após cada teste.
    def tearDown(self):
        # Remove a sessão do banco de dados.
        db.session.remove()
        # Apaga todas as tabelas do banco de dados.
        db.drop_all()
        # Remove o contexto da aplicação.
        self.app_context.pop()

    # Testa se a atribuição de uma senha resulta em um hash de senha.
    def test_password_setter(self):
        u = User(password='testpassword')
        self.assertTrue(u.password_hash is not None)
        
    # Testa se a tentativa de ler a propriedade 'password' levanta um AttributeError.
    def test_no_password_getter(self):
        u = User(password='testpassword')
        with self.assertRaises(AttributeError):
            u.password

    # Testa se a verificação de senha funciona corretamente para senhas certas e erradas.
    def test_password_verification(self):
        u = User(password='testpassword')
        self.assertTrue(u.verify_password('testpassword'))
        self.assertFalse(u.verify_password('wrongpassword'))

    # Testa se dois usuários com a mesma senha têm hashes diferentes, provando o uso de 'salt'.
    def test_password_salts_are_random(self):
        u1 = User(password='testpassword')
        u2 = User(password='testpassword')
        self.assertNotEqual(u1.password_hash, u2.password_hash)

    # Testa se um token de confirmação válido funciona como esperado.
    def test_valid_confirmation_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    # Testa se um token de um usuário é inválido para outro usuário.
    def test_invalid_confirmation_token(self):
        u1 = User(password='testpassword1')
        u2 = User(password='testpassword2')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    # Testa se um token expira após o tempo definido.
    def test_expired_confirmation_token(self):
        u = User(password='testpassword')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        # Espera 2 segundos.
        time.sleep(2)
        # Tenta confirmar com uma expiração de 1 segundo, o que deve falhar.
        self.assertFalse(u.confirm(token, expiration=1))

    # Testa as permissões do papel padrão 'User'.
    def test_user_role(self):
        u = User(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    # Testa as permissões do papel 'Moderator'.
    def test_moderator_role(self):
        r = Role.query.filter_by(name='Moderator').first()
        u = User(email='john@example.com', password='cat', role=r)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    # Testa as permissões do papel 'Administrator'.
    def test_administrator_role(self):
        r = Role.query.filter_by(name='Administrator').first()
        u = User(email='john@example.com', password='cat', role=r)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertTrue(u.can(Permission.ADMIN))

    # Testa que um usuário anônimo não tem nenhuma permissão.
    def test_anonymous_user(self):
        u = Anonymous()
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))