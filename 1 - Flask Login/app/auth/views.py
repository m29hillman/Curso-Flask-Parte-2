# Importa as funções e classes necessárias do Flask, Flask-Login e de outros módulos da aplicação.
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
# Importa o blueprint 'auth' para registrar as rotas de autenticação.
from . import auth
# Importa o modelo de usuário.
from app.models import User
# Importa a instância do LoginManager para o user_loader.
from app import login_manager
# Importa os formulários de autenticação.
from app.auth.forms import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm
# Importa a instância do banco de dados.
from app import db
# Importa a função de envio de e-mail.
from app.email import send_email

# Define uma função a ser executada antes de cada requisição na aplicação.
@auth.before_app_request
def before_request():
    # Verifica se o usuário está autenticado.
    if current_user.is_authenticated:
        # Atualiza o timestamp de 'última vez visto' do usuário.
        current_user.ping()
        # Se o usuário estiver autenticado, mas não tiver confirmado sua conta,
        # e a requisição não for para uma rota de autenticação ('auth') ou um arquivo estático,
        # ele é redirecionado para a página de 'não confirmado'.
        if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

# Define a rota para registro de novos usuários, aceitando métodos GET e POST.
@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Instancia o formulário de registro.
    form = RegistrationForm()
    # Se o formulário for submetido e passar na validação.
    if form.validate_on_submit():
        # Cria uma nova instância de User com os dados do formulário.
        user = User(email=form.email.data,
                    name=form.name.data,
                    password=form.password.data)
        # Adiciona o novo usuário à sessão do banco de dados e commita.
        db.session.add(user)
        db.session.commit()
        # Gera um token de confirmação para o novo usuário.
        token = user.generate_confirmation_token()
        # Envia um e-mail de confirmação para o usuário.
        send_email(user.email, 'Confirme sua conta', 'auth/email/confirm', user=user, token=token)
        # Exibe uma mensagem flash para o usuário.
        flash('Um e-mail de confirmação foi enviado para você por e-mail.')
        # Redireciona para a página inicial.
        return redirect(url_for('main.index'))
    # Se for uma requisição GET ou o formulário for inválido, renderiza o template de registro.
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    # Se o usuário já tiver confirmado sua conta, redireciona para a página inicial.
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    # Tenta confirmar o usuário com o token fornecido.
    if current_user.confirm(token):
        # Se a confirmação for bem-sucedida, commita a mudança no banco.
        db.session.commit()
        flash('Você confirmou sua conta. Obrigado!')
    else:
        # Se o token for inválido ou expirado, informa o usuário.
        flash('O link de confirmação é inválido ou expirou.')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    # Gera um novo token de confirmação para o usuário logado.
    token = current_user.generate_confirmation_token()
    # Envia o novo e-mail de confirmação.
    send_email(current_user.email, 'Confirme sua conta', 'auth/email/confirm', user=current_user, token=token)
    flash('Um novo e-mail de confirmação foi enviado para você por e-mail.')
    return redirect(url_for('main.index'))

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    # Se o usuário já estiver logado, não pode resetar a senha, então redireciona.
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    # Instancia o formulário de redefinição de senha.
    form = PasswordResetForm()
    if form.validate_on_submit():
        # Tenta redefinir a senha usando o token e a nova senha do formulário.
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Sua senha foi atualizada.')
            return redirect(url_for('auth.login'))
        else:
            # Se o token for inválido, redireciona para a página inicial.
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    # Se o usuário já estiver logado, não pode solicitar reset, então redireciona.
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    # Instancia o formulário de solicitação de redefinição de senha.
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        # Procura o usuário pelo e-mail fornecido no formulário.
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Se o usuário existir, gera um token de reset e envia o e-mail.
            token = user.generate_reset_token()
            send_email(user.email, 'Redefina sua senha', 'auth/email/reset_password', user=user, token=token)
            flash('Um e-mail com instruções para redefinir sua senha foi enviado para você.')
            return redirect(url_for('auth.login'))
        else:
            # Se o e-mail não for encontrado, informa o usuário.
            flash('E-mail não cadastrado no sistema.')
            return redirect(url_for('auth.password_reset_request'))
    return render_template('auth/login.html', form=form)

# Rota para a página que informa o usuário que sua conta não foi confirmada.
@auth.route('/unconfirmed')
def unconfirmed():
    # Se o usuário for anônimo ou já tiver confirmado a conta, redireciona para a página inicial.
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

# Define a rota de login, aceitando métodos GET e POST.
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Instancia o formulário de login.
    form = LoginForm()
    if form.validate_on_submit():
        # Procura o usuário pelo e-mail fornecido.
        user = User.query.filter_by(email=form.email.data).first()
        # Verifica se o usuário existe e se a senha está correta.
        if user is not None and user.verify_password(form.password.data):
            # Realiza o login do usuário com a ajuda do Flask-Login.
            login_user(user, form.remember_me.data)
            # Obtém a URL da página que o usuário tentava acessar antes do login (se houver).
            next = request.args.get('next') 
            # Se não houver 'next' ou se for um link inseguro, redireciona para a página inicial.
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        # Se o e-mail ou senha estiverem incorretos, exibe uma mensagem de erro.
        flash('E-mail ou senha inválidos.')
    # Renderiza o template de login com o formulário.
    return render_template('auth/login.html', form=form)

# Define a rota de logout.
@auth.route('/logout')
@login_required
def logout():
    # Desloga o usuário com a função do Flask-Login.
    logout_user()
    flash('Você saiu do sistema.')
    return redirect(url_for('main.index'))

# Callback do Flask-Login para recarregar o objeto do usuário a partir do ID armazenado na sessão.
@login_manager.user_loader    
def load_user(user_id):
    # Retorna o usuário correspondente ao ID, ou None se não for encontrado.
    return User.query.get(int(user_id))