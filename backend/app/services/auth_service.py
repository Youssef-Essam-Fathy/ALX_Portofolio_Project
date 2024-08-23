from flask import current_app
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, message):
    """
    Send an email asynchronously within the application's context.

    This function runs the email-sending process in a separate thread,
    allowing the application to continue processing without delay.

    Parameters:
    -----------
    app : Flask
        The Flask application instance to provide the context for email sending.
    message : Message
        The email message to be sent.

    Returns:
    --------
    None
    """
    with app.app_context():
        mail.send(message)


def send_account_created_email(user):
    """
    Send a confirmation email to the user after account creation.

    This function creates an email with a subject and body specific to
    account creation and sends it to the user's registered email address
    asynchronously.

    Parameters:
    -----------
    user : User
        The user object containing the username and email address to
        which the account creation email will be sent.

    Returns:
    --------
    None
    """
    subject = "Account Created"
    body = f"Dear {user.username}, your account has been successfully created."
    recipients = [user.email]
    sender = current_app.config['MAIL_SENDER']
    message = Message(subject=subject, body=body, recipients=recipients, sender=sender)
    thread = Thread(target=send_async_email, args=(current_app._get_current_object(), message))
    thread.start()
