# models/user.py
# Importa a instância do SQLAlchemy (db) do módulo 'extensions'.
# Isso evita importações circulares e segue o padrão de inicialização de extensões.
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from .role import Role
from .permission import Permission
from datetime import datetime

# Define o modelo de dados 'User' que mapeia para a tabela 'users' no banco de dados.
# A classe User herda de db.Model, a classe base para todos os modelos do Flask-SQLAlchemy.
class User(UserMixin, db.Model):
    # __tablename__ especifica o nome da tabela no banco de dados.
    __tablename__ = 'users'
    
    # Define a coluna 'id' como a chave primária da tabela.
    # db.Column é usado para definir uma coluna.
    # db.Integer especifica o tipo de dado como um inteiro.
    # primary_key=True marca esta coluna como a chave primária.
    id = db.Column(db.Integer, primary_key=True)
    
    # Define a coluna 'email' para armazenar o endereço de e-mail do usuário.
    email = db.Column(db.String(120), unique=True, index=True)

    name = db.Column(db.String(120))

    location = db.Column(db.String(64))

    about_me = db.Column(db.Text())

    member_since = db.Column(db.DateTime(), default=db.func.now())

    last_seen = db.Column(db.DateTime(), default=db.func.now())
    
    # Define a coluna 'role_id' como uma chave estrangeira.
    # db.ForeignKey('roles.id') cria uma restrição de chave estrangeira,
    # ligando esta coluna à coluna 'id' da tabela 'roles'.
    # Isso estabelece a relação "um-para-muitos" entre Role e User (uma Role pode ter muitos Users).
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    # Define a coluna 'password_hash' para armazenar o hash da senha do usuário.
    # A senha em texto plano nunca é armazenada diretamente por razões de segurança.
    # O comprimento de 128 é suficiente para armazenar os hashes gerados.
    password_hash = db.Column(db.String(128))

    # Define a coluna 'confirmed' para indicar se o usuário confirmou seu e-mail.
    # O valor padrão é False, significando que o usuário não está confirmado inicialmente.
    confirmed = db.Column(db.Boolean, default=False)
    
    # A anotação @property cria uma propriedade 'password' que não pode ser lida.
    # Tentar acessar user.password diretamente levantará um AttributeError.
    # Isso é uma medida de segurança para evitar que o hash da senha seja exposto acidentalmente.
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    # Define o setter para a propriedade 'password'.
    # Este método é chamado sempre que um valor é atribuído ao atributo 'password' de um objeto User.
    # Ex: my_user.password = 'uma_senha_super_secreta'
    # Ele recebe a senha em texto plano, gera um hash seguro usando generate_password_hash
    # e armazena esse hash na coluna 'password_hash' do banco de dados.
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Método para verificar se uma senha fornecida corresponde ao hash armazenado.
    # A função check_password_hash compara de forma segura a senha em texto plano com o hash.
    # Retorna True se a senha corresponder, e False caso contrário.
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})

    def confirm(self, token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expiration)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    def generate_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset': self.id})
    
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True
    
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
    

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    # O método __repr__ (representação) fornece uma representação em string "oficial" do objeto.
    # É útil para depuração, pois permite ver uma representação legível do objeto
    # ao imprimi-lo ou exibi-lo no console.
    def __repr__(self):
        return f'<User {self.email}>'