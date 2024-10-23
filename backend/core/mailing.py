import logging
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_mail_to_user(
    user, subject_template: str, text_template: str, context: dict = {}
):
    context["protocol"] = "https" if settings.SECURE_SSL_REDIRECT else "http"
    context["domain"] = settings.DOMAIN
    context["user"] = user

    subject = render_to_string(
        template_name=subject_template,
        context=context,
    )
    # remove newlines
    subject = "".join(subject.splitlines())

    message_plain = render_to_string(
        template_name=text_template,
        context=context,
    )
    # remove spaces from the beginning and end of each line
    message_plain = "\n".join([line.strip() for line in message_plain.splitlines()])

    res = send_mail(
        subject=subject,
        message=message_plain,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    if not res:
        logger.error(f"Send_mail error for user {user.email} of {subject_template}")

    return res
