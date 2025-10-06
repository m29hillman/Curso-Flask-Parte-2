# models/role.py
# Importa a instância do banco de dados (db) da aplicação.
from app import db
# Importa a classe Permission para definir os níveis de acesso.
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

    # Define uma coluna booleana para marcar qual papel (role) é o padrão para novos usuários.
    # default=False significa que, por padrão, um novo papel não é o padrão.
    # index=True cria um índice nesta coluna para otimizar as buscas por papéis padrão.
    default = db.Column(db.Boolean, default=False, index=True)

    # Define uma coluna de inteiro para armazenar as permissões do papel.
    # Este número é uma máscara de bits (bitmask) que representa a combinação de todas as permissões concedidas.
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

    # Construtor da classe. É chamado quando um novo objeto Role é criado.
    def __init__(self, **kwargs):
        # Chama o construtor da classe pai (db.Model) para inicialização padrão.
        super().__init__(**kwargs)
        # Garante que, se nenhuma permissão for fornecida na criação, o papel comece com 0 (sem permissões).
        if self.permissions is None:
            self.permissions = 0

    # Adiciona uma permissão ao papel.
    def add_permission(self, perm):
        # Verifica se o papel ainda não possui a permissão.
        if not self.has_permission(perm):
            # Adiciona a permissão usando o operador de OU bit a bit (bitwise OR).
            # Isso "liga" o bit correspondente à nova permissão sem afetar as outras.
            self.permissions += perm

    # Remove uma permissão do papel.
    def remove_permission(self, perm):
        # Verifica se o papel atualmente possui a permissão.
        if self.has_permission(perm):
            # Remove a permissão usando subtração.
            # Isso funciona porque os valores de permissão são potências de 2.
            self.permissions -= perm

    # Reseta todas as permissões do papel, definindo o valor como 0.
    def reset_permissions(self):
        self.permissions = 0

    # Verifica se o papel possui uma permissão específica.
    def has_permission(self, perm):
        # Usa o operador E bit a bit (bitwise AND) para verificar se o bit da permissão está "ligado".
        # Ex: Se permissions=3 (011) e perm=2 (010), (011 & 010) resulta em 2 (010), que é igual a perm.
        # Ex: Se permissions=1 (001) e perm=2 (010), (001 & 010) resulta em 0 (000), que não é igual a perm.
        return self.permissions & perm == perm

    # Método estático para popular o banco de dados com papéis e permissões predefinidos.
    # Pode ser chamado para configurar a aplicação na primeira vez que ela é executada.
    @staticmethod
    def insert_roles():
        # Dicionário que mapeia nomes de papéis a uma lista de suas permissões.
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT,
                     Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN]
        }
        # Define qual papel será o padrão para novos usuários.
        default_role = 'User'
        # Itera sobre os papéis definidos no dicionário.
        for r in roles:
            # Verifica se o papel já existe no banco de dados.
            role = Role.query.filter_by(name=r).first()
            # Se não existir, cria uma nova instância.
            if role is None:
                role = Role(name=r)
            # Reseta as permissões existentes para garantir um estado limpo.
            role.reset_permissions()
            # Adiciona cada permissão da lista ao papel.
            for perm in roles[r]:
                role.add_permission(perm)
            # Define a propriedade 'default' como True se o nome do papel for o padrão.
            role.default = (role.name == default_role)
            # Adiciona o objeto do papel à sessão do banco de dados para ser salvo.
            db.session.add(role)
        # Commita (salva) todas as mudanças na sessão para o banco de dados.
        db.session.commit()

    # O método __repr__ (representação) fornece uma representação em string "oficial" do objeto.
    # É útil para depuração, pois permite ver uma representação legível do objeto
    # ao imprimi-lo ou exibi-lo no console.
    def __repr__(self):
        return f'<Role {self.name} {self.permissions}>'