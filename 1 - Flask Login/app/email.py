from extensions import mail
from flask_mail import Message
from flask import current_app, render_template
from threading import Thread

def send_async_email(app,msg):
    """
    Função auxiliar para envio assíncrono de e-mails.
    Executa o envio dentro do contexto da aplicação Flask.
    Isso permite que o envio não bloqueie o fluxo principal da aplicação.
    """
    with app.app_context(): 
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    """
    Função para envio de e-mails.
    Parâmetros:
    - app: instância da aplicação Flask
    - subject: assunto do email
    - recipients: lista de destinatários
    - body: corpo do email em texto
    - html: corpo do email em HTML (opcional)

    Cria a mensagem, define remetente e dispara o envio em uma thread separada.
    O uso de threads evita que o usuário espere pelo envio do e-mail.
    """
    app = current_app._get_current_object()
    with app.app_context():
        msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        # Cria uma thread para envio assíncrono do e-mail.
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return thr
        # Se preferir envio síncrono, descomente a linha abaixo
        # mail.send(msg)