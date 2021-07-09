from decouple import config
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import send_mail as django_send_mail
from django.template.loader import render_to_string


def send_recovery_email(first_name, last_name, reset_token, email_to):
    text_template = 'reset_password/reset_password_email.txt'
    html_template = 'reset_password/reset_password_email.html'

    reset_url = f'{config("PASSWORD_RECOVERY_LINK_TEMPLATE")}'.format(reset_token=reset_token)

    context = {
        "first_name": first_name,
        "last_name": last_name,
        "reset_url": reset_url,
    }

    send_mail(
        'Password recovery',
        email_to,
        context,
        text_template,
        html_template
    )


def send_mail(subject, email_to, context, text_template, html_template):
    text_content = render_to_string(text_template, context)
    html_content = render_to_string(html_template, context)

    django_send_mail(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [email_to],
        html_message=html_content
    )
