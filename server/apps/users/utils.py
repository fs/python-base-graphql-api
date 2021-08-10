from server.core.utils.email import send_mail
from server.settings.components import config


def send_recovery_email(first_name, last_name, reset_token, email_to):
    """Send recovery email with rendered templates."""
    text_template = 'email/reset_password/reset_password_email.txt'
    html_template = 'email/reset_password/reset_password_email.html'

    context = {
        'first_name': first_name,
        'last_name': last_name,
        'reset_url': config('PASSWORD_RECOVERY_LINK_TEMPLATE').format(reset_token=reset_token),
    }

    send_mail(
        'Password recovery',
        email_to,
        context,
        text_template,
        html_template,
    )
