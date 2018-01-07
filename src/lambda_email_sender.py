from services import notification
from services.mail import MailService
from services.template import TemplateServiceS3
import time
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

mail = MailService()
mail_template_service = TemplateServiceS3('www.intervention.ninja', 'emails/')

MAIL_SUBJECT = 'Intervention Ninja - personal message'
MAIL_SENDER = 'intervention.ninja@gmail.com'


def lambda_handler(event, context):
    logger.info('event: {}'.format(event))
    records = event['Records']
    for item in records:
        message = json.loads(item['Sns']['Message'])
        logger.info('message: {}'.format(message))
        template = message['template']
        email = message['email']

        start = time.time()
        content_html = mail_template_service.render_template('{}.html'.format(template))
        end = time.time()
        logger.info('Rendering template took: {} seconds'.format(str(end-start)))

        start = time.time()
        mail.send_mail(MAIL_SUBJECT, MAIL_SENDER, email, content_html)
        end = time.time()
        logger.info('Sending email took: {} seconds'.format(str(end - start)))
