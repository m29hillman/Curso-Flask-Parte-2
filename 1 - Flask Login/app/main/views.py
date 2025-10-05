# Importações de bibliotecas padrão
from datetime import datetime

# Importações de pacotes de terceiros (Flask e extensões)
from flask import render_template, session, redirect, url_for, flash, current_app

# Importações locais da aplicação
from app import create_app, db
from app.models import User, Role, NameForm
from app.email import send_email  # Função para envio de e-mails (notificações)

from . import main

# Rota principal da aplicação ('/'), aceita métodos GET e POST.
@main.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota principal que renderiza a página inicial e processa o formulário de nome.

    Se o formulário for submetido, verifica se o usuário já existe.
    - Se for um novo usuário, ele é adicionado ao banco de dados e uma
      notificação por e-mail é enviada ao administrador.
    - Se o usuário já existir, uma mensagem informativa é exibida.

    Utiliza a sessão para lembrar o nome do usuário e se ele já era conhecido.
    O padrão Post/Redirect/Get é utilizado para evitar reenvio de formulários.
    """
    form = NameForm()
    
    # Valida o formulário: True se foi submetido e passou nos validadores.
    if form.validate_on_submit():
        # Consulta o banco de dados por um usuário com o nome informado.
        user = User.query.filter_by(username=form.name.data).first()
        
        # Se o usuário não existe, cadastra e envia e-mail de notificação.
        if user is None:
            flash('Novo nome cadastrado!')
            # Envia e-mail ao administrador informando novo cadastro.
            #O problema é que current_app é um proxy, não a instância real do Flask.
            #Quando você usa threads (como no envio assíncrono de e-mail), precisa passar a instância real da aplicação.
            send_email(current_app._get_current_object(), 
                       'Novo usuário ' + form.name.data, 
                       ['m29hillman@gmail.com'], 
                       "Obrigado por se cadastrar no nosso site!", 
                       None)
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False  # Marca como usuário novo
        else:
            # Usuário já existe, apenas informa.
            flash('Nome existente!')
            session['known'] = True  # Marca como usuário conhecido
            
        # Salva o nome na sessão para uso futuro.
        session['name'] = form.name.data
        form.name.data = ''  # Limpa o campo do formulário
        
        # Redireciona o usuário para a mesma rota ('index') usando uma requisição GET.
        # Este é o padrão Post/Redirect/Get, que previne o reenvio de formulários
        # caso o usuário atualize a página após uma submissão POST.
        return redirect(url_for('.index'))
        
    # Se a requisição for GET (ou se o formulário não for válido), renderiza o template.
    # Passa as variáveis para o template para que possam ser usadas no HTML.
    return render_template('index.html', 
                           form=form, 
                           name=session.get('name'), 
                           known=session.get('known', False),
                           current_time=datetime.utcnow())

@main.route('/user/<id>')
def user(id):
    user = User.query.filter_by(id=id).first_or_404()
    return render_template('user.html', user=user)