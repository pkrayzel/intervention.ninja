import emails
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# http://python-emails.readthedocs.io/en/latest/


class MailService:
    def __init__(self):
        self._smtp = None

    def send_mail(self, subject, sender, recipient, body_html):
        try:
            message = emails.html(html=body_html,
                                  subject=subject,
                                  mail_from=(sender, sender))

            logger.info('Sending email to recipient: {}'.format(recipient))

            result = message.send(to=(recipient, recipient), smtp=self._get_smtp())

            return result.status_code == 250
        except Exception as exception:
            logger.error('Sending email failed with exception: {}'.format(exception))
            return False

    def _get_smtp(self):
        if self._smtp is None:
            self._smtp = {
                'host': 'smtp.gmail.com',
                'port': 465,
                'ssl': True,
                'tls': False,
                'user': os.environ.get('MAIL_USERNAME'),
                'password': os.environ.get('MAIL_PASSWORD')
            }

        return self._smtp
