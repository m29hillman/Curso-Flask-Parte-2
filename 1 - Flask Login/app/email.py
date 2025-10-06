# Importa a instância do Flask-Mail, presumivelmente definida em extensions.py.
from extensions import mail
# Importa a classe Message para criar objetos de e-mail.
from flask_mail import Message
# Importa current_app para acessar a instância da aplicação e render_template para criar o corpo do e-mail a partir de arquivos de template.
from flask import current_app, render_template
# Importa a classe Thread para executar o envio de e-mail em uma thread separada (de forma assíncrona).
from threading import Thread

# Define a função que será executada na thread de envio.
def send_async_email(app,msg):
    """
    Função auxiliar para envio assíncrono de e-mails.
    Executa o envio dentro do contexto da aplicação Flask.
    Isso permite que o envio não bloqueie o fluxo principal da aplicação.
    """
    # O 'app_context' é necessário porque o envio de e-mail e a renderização de templates
    # precisam acessar a configuração da aplicação, o que não está disponível por padrão em uma nova thread.
    with app.app_context(): 
        mail.send(msg)

# Função principal para preparar e iniciar o envio de um e-mail.
def send_email(to, subject, template, **kwargs):
    """
    Função para envio de e-mails.
    Parâmetros:
    - to: destinatário do e-mail.
    - subject: assunto do e-mail.
    - template: nome base do template (sem .txt ou .html) a ser usado para o corpo do e-mail.
    - **kwargs: argumentos de palavras-chave a serem passados para o template (ex: user=user, token=token).

    Cria a mensagem, define remetente e dispara o envio em uma thread separada.
    O uso de threads evita que o usuário espere pelo envio do e-mail.
    """
    # 'current_app' é um proxy. Para passar a instância da aplicação para outra thread,
    # precisamos obter o objeto real da aplicação com '_get_current_object()'.
    app = current_app._get_current_object()
    with app.app_context():
        # Cria o objeto Message com o assunto (prefixado), remetente (da config) e destinatário.
        msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
        # Renderiza o corpo do e-mail em texto plano a partir do template .txt.
        msg.body = render_template(template + '.txt', **kwargs)
        # Renderiza o corpo do e-mail em HTML a partir do template .html.
        msg.html = render_template(template + '.html', **kwargs)
        # Cria uma thread para envio assíncrono do e-mail.
        # O alvo é a nossa função 'send_async_email', e passamos a instância da app e a mensagem como argumentos.
        thr = Thread(target=send_async_email, args=[app, msg])
        # Inicia a execução da thread. O programa principal continua imediatamente.
        thr.start()
        # Retorna o objeto da thread, o que pode ser útil para gerenciamento avançado.
        return thr
        # Se preferir envio síncrono, descomente a linha abaixo
        # mail.send(msg)