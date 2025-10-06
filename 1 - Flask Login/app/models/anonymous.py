# Importa a classe base para usuários anônimos do Flask-Login.
from flask_login import AnonymousUserMixin
# Importa a instância do LoginManager da aplicação.
from app import login_manager
# Importa o modelo User para ser usado no user_loader.
from .user import User

# Define uma classe customizada para usuários anônimos (não logados).
# Herda de AnonymousUserMixin, que fornece implementações padrão para
# propriedades como is_authenticated (que será False).
class Anonymous(AnonymousUserMixin):
    # Implementa o método de verificação de permissão para usuários anônimos.
    # Um usuário não logado não tem nenhuma permissão, então sempre retorna False.
    # Isso garante que chamadas como `current_user.can(Permission.WRITE)` não quebrem
    # quando o usuário não está logado.
    def can(self, perm):
        return False
    
    # Implementa o método de verificação se o usuário é administrador.
    # Um usuário anônimo nunca é um administrador.
    def is_administrator(self):
        return False

# O decorador @login_manager.user_loader registra esta função com o Flask-Login.
# O Flask-Login usará esta função para recarregar um objeto de usuário a partir do
# ID de usuário armazenado na sessão em cada requisição.
# NOTA: Esta função também está definida em 'app/auth/views.py'. Ter múltiplos
# user_loaders pode ser confuso. Geralmente, apenas um é necessário para toda a aplicação.
@login_manager.user_loader
def load_user(user_id):
    # Busca e retorna o usuário do banco de dados com base no ID fornecido.
    return User.query.get(int(user_id))