# import win32com.client as win32

def envio_email(nome, to, senha):
    from http import server
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from bd import login, password

    # S M T P - Simple Mail Transfere Protocol
    # para criar o servidor e enviar o email

    # starta o servidor smtp
    # Declaração de valores de entrada e acesso 
    host = "smtp.gmail.com"
    port = "587"

    # Faz a conexão com servidor
    server = smtplib.SMTP(host, port)

    # Starta os requisitos de segurança para ativação
    #  fornece endereço IP do servidor SMTP
    server.ehlo()
    # Inicializa a função de segurança "Transport Layer Security"
    server.starttls()

    # Acessa a conta com os dados de login
    server.login(login, password)

    #CORPO DE EMAIL TIPO MIME
    corpo = f'''
            Olá, {nome}!
            segue abaixo seus dados para acessar nossa plataforma
            email: {to}
            senha: {senha}

            não compartilhe sua senha com ninguêm!

            este é uma email automático, favor não responder :)
            '''

    # Codifica a mensagem do email em tipo MIME
    email_msg = MIMEMultipart()
    email_msg ['From'] = login
    email_msg ['To'] = to
    email_msg ['Subject'] = "E-mail automático - Dados para acesso da plataforma"
    email_msg.attach(MIMEText(corpo, 'Plain'))

    # Envia o email tipo MIME no SERVIDOR SMTP
    server.sendmail(email_msg["From"], email_msg["To"], email_msg.as_string())

    if str(object='@') in to:
        server.sendmail(email_msg["From"], email_msg["To"], email_msg.as_string())
        print(f'E-mail enviado para {nome}')
    else:
        print(f'Não existe e-mail cadastrado para {nome}')

    # Ecerra conexão com o servidor
    server.quit()
    
# Função envio de  e-mail Líder do Grupo e Fake Client
def enviar_email(nome, email1, senha):
    outlook = win32.Dispatch('outlook.application')  # Criar interação com outlook
    email = outlook.CreateItem(0)  # Criar um e-mail

    # Configurar as informações do e-mail
    email.To = email1
    email.Subject = 'E-mail automático - Senha cadastrada para Avaliação 360°'
    email.HTMLBody = f"""
    <p>Olá, {nome}!</p>

    <p>Aqui está sua senha gerada automaticamente, para acesso à plataforma de Avaliação 360°:</p>
    <p>E-MAIL CADASTRADO: {email1}</p>

    <p><b>Sua senha é intrasferível, não compartilhe com ninguém.</b></p>
    <p>SENHA:{senha}</p>

    <p>Não responda a este e-mail.</p>
    """

    if str(object='@') in email1:
        email.Send()
        print(f'E-mail enviado para {nome}')
    else:
        print(f'Não existe e-mail cadastrado para {nome}')
