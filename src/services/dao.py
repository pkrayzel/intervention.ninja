import boto3
import logging
from datetime import datetime
import time
import uuid

client_dynamo = boto3.client('dynamodb')

FILTER_FIELD_IP_ADDRESS = 'ip_address'
FILTER_FIELD_TIMESTAMP_GREATER_THAN = 'timestamp_gt'
FILTER_FIELD_EMAIL = 'email'


def store_mail_sent(source_ip, email, template):
    date = datetime.now()

    item = {
        'guid': {
            'S': str(uuid.uuid4())
        },
        'ip_address': {
            'S': source_ip
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


def get_count_for_filter(filter_criteria):
    logging.info('Querying DynamoDB - filter_criteria: {}'.format(filter_criteria))
    try:
        pass
        # response = client_dynamo.put_item(
        #     TableName='ninja_emails',
        #     Item=item
        # )
        # logging.info('DynamoDB response: {}'.format(response))
    except Exception as exception:
        pass
        # logging.error('Error during dynamodb request: {}', exception)

    return 0