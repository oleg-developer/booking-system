from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from apps.auth_core.celery import app


@app.task
def send_email(subject, template_name, context, emails):
    """
    Sending an email message
    :param subject: messaje subject
    :param template_name: template name
    :param context: context dict
    :param emails: recipients list
    :return: 
    """
    plaintext = get_template('{}.txt'.format(template_name))
    html = get_template('{}.html'.format(template_name))

    text_content = plaintext.render(context)
    html_content = html.render(context)

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

