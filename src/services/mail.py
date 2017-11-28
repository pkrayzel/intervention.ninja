from flask_mail import Mail, Message
from flask import current_app, render_template
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class MailService:
    def __init__(self):
        self._mail_service = None

    def send_mail(self, subject, sender, recipient, body, body_html):
        try:
            msg = Message(subject, sender, recipients=[recipient])
            msg.body = body
            msg.html = body_html

            logger.info('Sending email to recipient: {}'.format(recipient))
            self._get_mail().send(msg)
            return True
        except Exception as exception:
            logger.error('Sending email failed with exception: {}'.format(exception))
            return False

    def _get_mail(self):
        if self._mail_service is None:
            self._mail_service = Mail(current_app)

        return self._mail_service
