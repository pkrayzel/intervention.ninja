import boto3
import logging
import random

import os,sys,inspect
from datetime import datetime
import time

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client_dynamo = boto3.client('dynamodb', region_name='us-east-1')
resource_dynamo = boto3.resource('dynamodb', region_name='us-east-1')

TABLE_NAME_EMAILS_CACHE = 'intervention_ninja_emails_cache_2'
TABLE_NAME_IPS_CACHE = 'intervention_ninja_ips_cache_2'
TABLE_NAME_EMAILS = 'intervention_ninja_emails_3'
TABLE_NAME_IPS = 'intervention_ninja_ips_3'

logger.info('Generating items... ')

EMAILS = [
  'pkrayzel@gmail.com',
  'martina.krayzelova@gmail.com',
  'petr.palchat@gmail.com',
  'robert.spurny@email.cz',
  'dalsi@email.cz',
  'first@second.cz',
  'vlada.spurny@gomail.cz'
]

IPS = [
  '11.1.2.4',
  '189.34.32.4',
  '124.5.4.6',
  '123.4.3.2',
  '12.2.2.1',
  '178.65.54.3',
  '129.54.76.4',
  '86.5.4.2'
]

TEMPLATES = ['drink', 'smell']

def main():
  for x in range(100):
    response = client_dynamo.batch_write_item(
      RequestItems={
        TABLE_NAME_EMAILS: [
          {
            'PutRequest': {
              'Item': {
                'timestamp': {'N': str(int(time.mktime(datetime.now().timetuple())) * 1000 + random.randint(1,1000000))},
                'date': {'S': datetime.now().strftime("%Y/%m/%d")},
                'time': {'S': datetime.now().strftime("%H:%M:%S")},
                'email': {'S': random.choice(EMAILS)},
                'template': {'S': random.choice(TEMPLATES)}
              }
            }
          } for i in range(25)
        ]
      },
      ReturnConsumedCapacity='TOTAL',
      ReturnItemCollectionMetrics='SIZE'
    )
    logger.info(response)

    response = client_dynamo.batch_write_item(
      RequestItems={
        TABLE_NAME_IPS: [
          {
            'PutRequest': {
              'Item': {
                'timestamp': {'N': str(int(time.mktime(datetime.now().timetuple())) * 1000 + random.randint(1,1000000))},
                'date': {'S': datetime.now().strftime("%Y/%m/%d")},
                'time': {'S': datetime.now().strftime("%H:%M:%S")},
                'ip_address': {'S': random.choice(IPS)}
              }
            }
          } for i in range(25)
        ]
      },
      ReturnConsumedCapacity='TOTAL',
      ReturnItemCollectionMetrics='SIZE'
    )

    logger.info(response)


def main_2():
  for i in range(1000):
    ip = {
      'timestamp': {'N': str(int(time.mktime(datetime.now().timetuple())) * 1000 + random.randint(1,1000000))},
      'date': {'S': datetime.now().strftime("%Y/%m/%d")},
      'time': {'S': datetime.now().strftime("%H:%M:%S")},
      'ip_address': {'S': random.choice(IPS)}
    }

    client_dynamo.put_item(
      TableName=TABLE_NAME_IPS_CACHE,
      Item=ip)
    logger.info('ip created...')

    email = {
      'timestamp': {'N': str(int(time.mktime(datetime.now().timetuple())) * 1000 + random.randint(1,1000000))},
      'date': {'S': datetime.now().strftime("%Y/%m/%d")},
      'time': {'S': datetime.now().strftime("%H:%M:%S")},
      'email': {'S': random.choice(EMAILS)},
      'template': {'S': random.choice(TEMPLATES)}
    }

    client_dynamo.put_item(TableName=TABLE_NAME_EMAILS_CACHE, Item=email)
    logger.info('email created...')


if __name__ == '__main__':
    main_2()
