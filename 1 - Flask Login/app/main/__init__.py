# Importa a classe Blueprint do Flask para modularizar a aplicação.
from flask import Blueprint

# Cria uma instância de Blueprint chamada 'main'.
# Este blueprint agrupará as rotas principais e funcionalidades centrais da aplicação,
# como a página inicial e perfis de usuário.
main = Blueprint('main', __name__)

# Importa os módulos de views (rotas) e errors (manipuladores de erro) que pertencem a este blueprint.
# A importação é feita no final para evitar dependências circulares, pois os arquivos 'views.py' e 'errors.py'
# precisarão importar a variável 'main' que foi definida acima.
from . import views, errors

# Importa o modelo de Permissões para poder injetá-lo no contexto dos templates.
from ..models.permission import Permission

# Registra uma função que será executada antes de renderizar qualquer template associado a este blueprint.
# O decorador 'app_context_processor' faz com que o dicionário retornado pela função
# seja adicionado ao contexto do template, tornando suas chaves/valores acessíveis no Jinja2.
@main.app_context_processor
def inject_permissions():
    # Esta função injeta a classe 'Permission' no contexto de todos os templates.
    # Isso permite que o código do template verifique permissões de forma conveniente,
    # por exemplo: {% if current_user.can(Permission.WRITE) %} ... {% endif %}
    return dict(Permission=Permission)