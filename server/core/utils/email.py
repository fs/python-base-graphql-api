from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.template.loader import render_to_string


def send_mail(subject, email_to, context, text_template, html_template):
    """Send email with templates."""
    text_content = render_to_string(text_template, context)
    html_content = render_to_string(html_template, context)

    django_send_mail(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [email_to],
        html_message=html_content,
    )
