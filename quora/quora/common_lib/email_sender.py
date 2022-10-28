from django.conf import settings
from django.core.mail import EmailMessage


def send_post(subject, body):
    """
    subject = f"The letter from admin of angara77.ru server, pay attention"
    body = f"This email has been sent from maintanance angara77.ru server"
    """

    if not body:
        body = f"This email has been sent from maintanance angara77.ru server"

    if not subject:
        subject = f"The letter from admin of angara77.ru server, pay attention"

    from_email = f"PartsHub Admin <mikohan1@gmail.com>"
    headers = {
        "Content-Type": "text/plain",
        "X-Priority": "1 (Highest)",
        "X-MSMail-Priority": "High",
    }
    email = EmailMessage(
        subject,
        body,
        from_email,
        settings.EMAIL_ADMINS,
        headers=headers,
    )
    email.send(fail_silently=False)
