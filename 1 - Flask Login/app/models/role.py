# models/role.py
# Importa a instância do SQLAlchemy (db) do módulo 'extensions'.
# Isso evita importações circulares e segue o padrão de inicialização de extensões.
from extensions import db
from .permission import Permission


# Define o modelo de dados 'Role' que mapeia para a tabela 'roles' no banco de dados.
# A classe Role herda de db.Model, a classe base para todos os modelos do Flask-SQLAlchemy.
class Role(db.Model):
    # __tablename__ especifica o nome da tabela no banco de dados.
    __tablename__ = 'roles'
    
    # Define a coluna 'id' como a chave primária da tabela.
    # db.Column é usado para definir uma coluna.
    # db.Integer especifica o tipo de dado como um inteiro.
    # primary_key=True marca esta coluna como a chave primária.
    id = db.Column(db.Integer, primary_key=True)
    
    # Define a coluna 'name' para armazenar o nome da função/papel (ex: 'Admin', 'User').
    # db.String(64) define o tipo como uma string com um comprimento máximo de 64 caracteres.
    # unique=True garante que cada nome de função na tabela seja único.
    name = db.Column(db.String(64), unique=True)
    
    default = db.Column(db.Boolean, default=False, index=True)
    
    permissions = db.Column(db.Integer)

    # Define a relação entre Role e User. Isso não cria uma coluna no banco de dados.
    # 'User' é o nome da classe do modelo do outro lado da relação.
    # backref='role' cria um atributo 'role' nos objetos User, permitindo o acesso
    # reverso (de um usuário para sua função, ex: user.role).
    # lazy='dynamic' faz com que a consulta para os usuários não seja executada
    # imediatamente. Em vez disso, retorna um objeto de consulta que pode ser
    # refinado antes da execução (ex: role.users.order_by(...).all()).
    # Isso é útil para coleções que podem ser muito grandes.
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm
        
    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, 
                     Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT, 
                              Permission.WRITE, Permission.MODERATE, 
                              Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    # O método __repr__ (representação) fornece uma representação em string "oficial" do objeto.
    # É útil para depuração, pois permite ver uma representação legível do objeto
    # ao imprimi-lo ou exibi-lo no console.
    def __repr__(self):
        return f'<Role {self.name} {self.permissions}>'