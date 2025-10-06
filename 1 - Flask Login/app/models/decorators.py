# Importa a função 'wraps' para preservar os metadados da função original ao usar um decorador.
from functools import wraps
# Importa a função 'abort' do Flask para interromper uma requisição com um código de erro HTTP.
from flask import abort
# Importa 'current_user' do Flask-Login, que é um proxy para o objeto do usuário logado na requisição atual.
from flask_login import current_user
# Importa o modelo de Permissões para verificar os níveis de acesso.
# OBS: A importação 'from permission import Permission' pode estar incorreta dependendo da estrutura do projeto.
# Geralmente, seria uma importação relativa como 'from .permission import Permission'.
from .permission import Permission

# Define um decorador que verifica se o usuário logado possui uma permissão específica.
# Este é um "decorator factory", pois ele recebe um argumento (a permissão) e retorna o decorador real.
def permission_required(permission):
    # A função 'decorator' recebe a função que será "embrulhada" (ex: uma view do Flask).
    def decorator(f):
        # '@wraps(f)' garante que a função 'decorated_function' se pareça com a função original 'f'
        # (mantendo nome, docstring, etc.).
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verifica se o usuário atual (current_user) NÃO tem a permissão necessária.
            # O método 'can()' é definido no modelo User.
            if not current_user.can(permission):
                # Se o usuário não tiver a permissão, a requisição é abortada com um erro 403 (Forbidden).
                abort(403)
            # Se o usuário tiver a permissão, a função original é executada normalmente.
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Define um decorador específico para verificar se o usuário é um administrador.
# Este é um atalho para não ter que escrever @permission_required(Permission.ADMIN) toda vez.
def admin_required(f):
    # Retorna o resultado da aplicação do decorador 'permission_required' com a permissão de ADMIN
    # para a função 'f'.
    return permission_required(Permission.ADMIN)(f)