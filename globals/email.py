from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


class EmailService:

    @staticmethod
    def send_email(subject, body, from_email, to_emails, fail_silently=False):
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=to_emails,
            fail_silently=fail_silently
        )

    @staticmethod
    def send_activation_email(activation_link, from_email, to_emails):
        subject = 'Activate Your Account'
        html_content = render_to_string('email/activation_email.html', {'activation_link': activation_link})
        text_content = 'Click the following link to activate your account: {}'.format(activation_link)

        email = EmailMultiAlternatives(subject, text_content, from_email=from_email, to=to_emails)
        email.attach_alternative(html_content, "text/html")
        email.send()

    @staticmethod
    def send_reset_password_email(reset_link, from_email, to_emails):
        subject = 'Reset Your Password'
        html_content = render_to_string('email/reset_email.html', {'reset_link': reset_link})
        text_content = 'Click the following link to reset your password: {}'.format(reset_link)

        email = EmailMultiAlternatives(subject, text_content, from_email=from_email, to=to_emails)
        email.attach_alternative(html_content, "text/html")
        email.send()
