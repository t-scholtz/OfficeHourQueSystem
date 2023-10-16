from flask_mail import Mail, Message

mail = None  # Initialize the mail instance as None

def set_mail(mail_in):
    global mail
    mail = mail_in  # Store the mail instance

def send_email(recipient, subject, message_body):
    if mail is None:
        raise ValueError("Mail instance is not set. Call set_mail() before sending emails.")
    
    msg = Message(subject=subject, recipients=[recipient])
    msg.body = message_body
    mail.send(msg)
