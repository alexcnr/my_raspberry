import smtplib, ssl

def mail_sender(message):
    port = 587  # For starttls
    smtp_server = "smtp.mail.ru"
    sender_email = "raspberry.py4@mail.ru"
    receiver_email = "raspberry.py4@mail.ru"
    password = "password"

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.set_debuglevel(1)
        server.ehlo()  
        server.starttls(context=context)
        server.ehlo()  
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    

