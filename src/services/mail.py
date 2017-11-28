from flask_mail import Mail, Message
from flask import current_app, render_template
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class MailService:
    def __init__(self):
        self._mail_service = None

    def send_mail(self, email, template):
        msg = Message('Intervention Ninja - personal message',
                      sender='intervention.ninja@gmail.com',
                      recipients=[email])
        msg.body = render_template('emails/{}.txt'.format(template))
        msg.html = render_template('emails/{}.html'.format(template))

        logger.info('Sending email to recipient: {} with template: {}'.format(email, template))
        self._get_mail().send(msg)

    def _get_mail(self):
        if self._mail_service is None:
            self._mail_service = Mail(current_app)

        return self._mail_service
