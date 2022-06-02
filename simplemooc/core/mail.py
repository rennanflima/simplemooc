from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string


def send_mail_template(subject, template_name, context, recipient_list,
                       from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
    """
    Envia um e-mail usando um template Django.
    """
    # Usa o template do Django para o corpo do e-mail
    message_html = render_to_string(template_name, context)

    message_text = striptags(message_html)

    email = EmailMultiAlternatives(
        subject=subject, body=message_text, from_email=from_email, to=recipient_list
    )
    email.attach_alternative(message_html, 'text/html')
    email.send(fail_silently=fail_silently)
