# Importa a classe datetime para trabalhar com datas e horas.
from datetime import datetime

# Importa funções e objetos do Flask para renderizar templates, gerenciar sessões, redirecionar, etc.
from flask import render_template, session, redirect, url_for, flash, current_app

# Importa a instância do banco de dados (db) da aplicação.
from app import db
# Importa os modelos de dados User e Role, e o formulário NameForm.
from app.models import User, Role, NameForm
# Importa a função de envio de e-mail.
from app.email import send_email

# Importa o blueprint 'main' para registrar as rotas.
from . import main

# Rota principal da aplicação ('/'), aceita métodos GET e POST.
@main.route('/', methods=['GET', 'POST'])
def index():
    # Instancia o formulário de nome.
    form = NameForm()
    
    # Verifica se o formulário foi submetido (POST) e se os dados são válidos.
    if form.validate_on_submit():
        # Consulta o banco de dados por um usuário com o nome informado.
        user = User.query.filter_by(name=form.name.data).first()
        
        # Se o usuário não existe, cadastra e envia e-mail de notificação.
        if user is None:
            flash('Novo nome cadastrado!')
            # Cria uma nova instância de User com o nome do formulário.
            user = User(name=form.name.data)
            # Adiciona o novo usuário à sessão do banco de dados e commita.
            db.session.add(user)
            db.session.commit()
            # Armazena na sessão que este é um usuário novo.
            session['known'] = False
        else:
            # Se o usuário já existe, exibe uma mensagem e marca na sessão.
            flash('Nome existente!')
            session['known'] = True
            
        # Salva o nome na sessão para ser exibido na página.
        session['name'] = form.name.data
        
        # Redireciona para a mesma rota (padrão Post/Redirect/Get).
        # Isso evita que o formulário seja reenviado se o usuário atualizar a página.
        return redirect(url_for('.index'))
        
    # Para requisições GET (ou se o formulário for inválido), renderiza a página inicial.
    # Passa as variáveis necessárias para o template Jinja2.
    return render_template('index.html', 
                           form=form, 
                           name=session.get('name'), 
                           known=session.get('known', False),
                           current_time=datetime.utcnow())

# Define uma rota para exibir o perfil de um usuário específico.
# '<id>' é uma parte dinâmica da URL que corresponde ao ID do usuário.
@main.route('/user/<id>')
def user(id):
    # Busca o usuário no banco de dados pelo ID fornecido.
    # 'first_or_404()' retorna o primeiro resultado ou, se não encontrar, aborta com um erro 404 (Not Found).
    user = User.query.filter_by(id=id).first_or_404()
    # Renderiza o template 'user.html', passando o objeto 'user' encontrado.
    return render_template('user.html', user=user)