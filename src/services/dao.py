import boto3
import logging
from datetime import datetime
import time
import uuid

client_dynamo = boto3.client('dynamodb')


def store_mail_sent(email, template):
    date = datetime.now()

    item = {
        'guid': {
            'S': str(uuid.uuid4())
        },
        'email': {
            'S': email
        },
        'template': {
            'S': template
        },
        'date': {
            'S': date.strftime("%Y/%m/%d")
        },
        'time': {
            'S': date.strftime("%H:%M:%S")
        },
        'timestamp': {
            'S': str(int(time.mktime(date.timetuple())))
        }
    }
    logging.info('Sending data to DynamoDB - item: {}'.format(item))
    try:
        response = client_dynamo.put_item(
            TableName='ninja_emails',
            Item=item
        )
        logging.info('DynamoDB response: {}'.format(response))
    except Exception as exception:
        logging.error('Error during dynamodb request: {}', exception)
