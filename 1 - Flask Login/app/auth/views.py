from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from app.models import User
from app import login_manager
from app.auth.forms import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm
from app import db
from app.email import send_email

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))
    
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirme sua conta', 'auth/email/confirm', user=user, token=token)
        flash('Um e-mail de confirmação foi enviado para você por e-mail.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Você confirmou sua conta. Obrigado!')
    else:
        flash('O link de confirmação é inválido ou expirou.')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirme sua conta', 'auth/email/confirm', user=current_user, token=token)
    flash('Um novo e-mail de confirmação foi enviado para você por e-mail.')
    return redirect(url_for('main.index'))

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Sua senha foi atualizada.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Redefina sua senha', 'auth/email/reset_password', user=user, token=token)
            flash('Um e-mail com instruções para redefinir sua senha foi enviado para você.')
            return redirect(url_for('auth.login'))
        else:
            flash('E-mail não cadastrado no sistema.')
            return redirect(url_for('auth.password_reset_request'))
    return render_template('auth/login.html', form=form)

    
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next') 
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('E-mail ou senha inválidos.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.')
    return redirect(url_for('main.index'))

@login_manager.user_loader    
def load_user(user_id):
    return User.query.get(int(user_id))