# Importa a classe Blueprint do Flask, que permite organizar um grupo de rotas e outros códigos relacionados à aplicação.
from flask import Blueprint

# Cria uma instância de Blueprint chamada 'auth'.
# Blueprints são usados para modularizar uma aplicação Flask.
# O primeiro argumento, 'auth', é o nome do blueprint e será usado nos endpoints das rotas (ex: 'auth.login').
# O segundo argumento, `__name__`, ajuda o Flask a localizar o diretório raiz do blueprint (para templates, arquivos estáticos, etc.).
auth = Blueprint('auth', __name__)

# Importa o módulo de views (rotas) que pertence a este blueprint.
# A importação é feita no final para evitar dependências circulares, já que o arquivo 'views.py' precisará importar a variável 'auth' definida aqui.
from . import views