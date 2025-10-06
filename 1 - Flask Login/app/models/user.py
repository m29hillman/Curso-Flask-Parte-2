# models/user.py
# Importa a instância do banco de dados (db) da aplicação.
from app import db
# Importa funções de segurança para gerar e verificar hashes de senha.
from werkzeug.security import generate_password_hash, check_password_hash
# Importa UserMixin, que fornece implementações padrão para os métodos exigidos pelo Flask-Login (is_authenticated, etc.).
from flask_login import UserMixin
# Importa o Serializer para criar tokens seguros e com tempo de expiração (para confirmação de e-mail, reset de senha).
from itsdangerous import URLSafeTimedSerializer as Serializer
# Importa o proxy current_app para acessar a configuração da aplicação (como a SECRET_KEY).
from flask import current_app
# Importa os modelos Role e Permission para gerenciar o controle de acesso.
from .role import Role
from .permission import Permission
# Importa datetime para trabalhar com timestamps.
from datetime import datetime

# Define o modelo de dados 'User' que mapeia para a tabela 'users' no banco de dados.
# A classe User herda de UserMixin (para integração com Flask-Login) e db.Model (para integração com SQLAlchemy).
class User(UserMixin, db.Model):
    # __tablename__ especifica o nome da tabela no banco de dados.
    __tablename__ = 'users'
    
    # Define a coluna 'id' como a chave primária da tabela.
    # db.Column é usado para definir uma coluna.
    # db.Integer especifica o tipo de dado como um inteiro.
    # primary_key=True marca esta coluna como a chave primária.
    id = db.Column(db.Integer, primary_key=True)
    
    # Define a coluna 'email' para armazenar o endereço de e-mail do usuário.
    # unique=True garante que cada e-mail seja único. index=True cria um índice para acelerar as buscas por e-mail.
    email = db.Column(db.String(120), unique=True, index=True)

    # Coluna para o nome do usuário.
    name = db.Column(db.String(120))

    # Coluna para a localização do usuário.
    location = db.Column(db.String(64))

    # Coluna para a biografia do usuário ("Sobre mim"). db.Text() é usado para textos longos.
    about_me = db.Column(db.Text())

    # Coluna para registrar a data de cadastro do usuário. default=db.func.now() define o valor padrão como a data/hora atual do servidor de banco de dados.
    member_since = db.Column(db.DateTime(), default=db.func.now())

    # Coluna para registrar a última vez que o usuário esteve ativo.
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
    
    # Gera um token de confirmação de e-mail.
    def generate_confirmation_token(self):
        # Cria um serializador usando a chave secreta da aplicação.
        s = Serializer(current_app.config['SECRET_KEY'])
        # Gera um token seguro contendo o ID do usuário.
        return s.dumps({'confirm': self.id})

    # Valida um token de confirmação e marca o usuário como confirmado.
    def confirm(self, token, expiration=3600):
        # Cria um serializador com a mesma chave secreta.
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # Tenta decodificar o token. max_age define o tempo de vida do token em segundos (1 hora por padrão).
            data = s.loads(token, max_age=expiration)
        except:
            # Se o token for inválido ou expirado, a decodificação falha.
            return False
        # Verifica se o ID no token corresponde ao ID do usuário atual.
        if data.get('confirm') != self.id:
            return False
        # Se tudo estiver correto, marca o usuário como confirmado e adiciona à sessão do DB.
        self.confirmed = True
        db.session.add(self)
        return True
    
    # Gera um token para redefinição de senha.
    def generate_reset_token(self):
        # O processo é semelhante ao token de confirmação, mas com um payload diferente.
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset': self.id})
    
    # Método estático para redefinir a senha de um usuário usando um token.
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # Decodifica o token para obter o ID do usuário.
            # Nota: Não há verificação de expiração (max_age) aqui, o que pode ser um risco de segurança.
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        # Busca o usuário no banco de dados usando o ID do token.
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        # Define a nova senha (o setter cuidará do hashing).
        user.password = new_password
        db.session.add(user)
        return True
    
    # Verifica se o usuário tem uma permissão específica.
    def can(self, perm):
        # Delega a verificação para o papel (Role) do usuário.
        # Retorna False se o usuário não tiver um papel associado.
        return self.role is not None and self.role.has_permission(perm)
    
    # Verifica se o usuário é um administrador.
    def is_administrator(self):
        # É um atalho para verificar a permissão de ADMIN.
        return self.can(Permission.ADMIN)
    
    # Atualiza o timestamp 'last_seen' do usuário para a hora atual.
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        # Nota: Chamar commit() aqui em cada requisição pode adicionar sobrecarga.
        # Em aplicações de alto tráfego, pode ser melhor otimizar isso.
        db.session.commit()
    

    # Construtor da classe User. É chamado quando um novo objeto User é criado.
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # Se nenhum papel (role) for atribuído ao criar o usuário...
        if self.role is None:
            # ...verifica se o e-mail do usuário corresponde ao e-mail do administrador definido na configuração.
            if self.email == current_app.config['FLASKY_ADMIN']:
                # Se for o admin, atribui o papel de 'Administrator'.
                self.role = Role.query.filter_by(name='Administrator').first()
            # Se ainda não tiver um papel (ou seja, não é o admin)...
            if self.role is None:
                # ...atribui o papel que está marcado como padrão no banco de dados (geralmente 'User').
                self.role = Role.query.filter_by(default=True).first()

    # O método __repr__ (representação) fornece uma representação em string "oficial" do objeto.
    # É útil para depuração, pois permite ver uma representação legível do objeto
    # ao imprimi-lo ou exibi-lo no console.
    def __repr__(self):
        return f'<User {self.email}>'