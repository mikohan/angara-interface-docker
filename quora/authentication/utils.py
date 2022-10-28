from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        subject = data["email_subject"]
        body = data["email_body"]
        to = data["email_recepient"]
        email = EmailMessage(
            subject=subject,
            body=body,
            to=[
                to,
            ],
        )
        email.send()
