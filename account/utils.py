from django.core.mail import EmailMessage
import os
class Util:
    @staticmethod
    def send_email(data):
        email =EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email=os.environ.get('EMAIL_HOST_USER'),  # Use the environment variable for the
            to=[data['to_email']]
        )
        email.sens()