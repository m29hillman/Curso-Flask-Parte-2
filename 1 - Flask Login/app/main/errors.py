from flask import render_template 
from . import main

# O decorator @app.errorhandler registra uma função para ser chamada quando um erro HTTP específico ocorre.
# Neste caso, o erro 403 (Acesso Negado).
@main.app_errorhandler(403)
def forbidden(e):
    """Renderiza a página de erro 403 personalizada."""
    # Retorna o template '403.html' e o código de status 403.
    return render_template('403.html'), 403


# O decorator @app.errorhandler registra uma função para ser chamada quando um erro HTTP específico ocorre.
# Neste caso, o erro 404 (Página Não Encontrada).
@main.app_errorhandler(404)
def page_not_found(e):
    """Renderiza a página de erro 404 personalizada."""
    # Retorna o template '404.html' e o código de status 404.
    return render_template('404.html'), 404

# Registra um manipulador para o erro 500 (Erro Interno do Servidor).
# Isso captura exceções não tratadas na aplicação.
@main.app_errorhandler(500)
def internal_server_error(e):
    """Renderiza a página de erro 500 personalizada."""
    # Retorna o template '500.html' e o código de status 500.
    return render_template('500.html'), 500