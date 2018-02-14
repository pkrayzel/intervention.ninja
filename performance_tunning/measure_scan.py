import boto3
import time
from boto3.dynamodb.conditions import Key
import logging
import generate_data_batch
import random


logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client_dynamo = boto3.client('dynamodb', region_name='us-east-1')
resource_dynamo = boto3.resource('dynamodb', region_name='us-east-1')

TABLE_NAME_EMAILS_CACHE = 'intervention_ninja_emails_cache_2'
TABLE_NAME_IPS_CACHE = 'intervention_ninja_ips_cache_2'
TABLE_NAME_EMAILS = 'intervention_ninja_emails_3'
TABLE_NAME_IPS = 'intervention_ninja_ips_3'

table = resource_dynamo.Table(TABLE_NAME_EMAILS)
table_ip = resource_dynamo.Table(TABLE_NAME_IPS)

start = time.time()

email = random.choice(generate_data_batch.EMAILS)

logger.info(f'measuring search for email: {email}')
logger.info('scan: ')

response = table.scan(
  FilterExpression=Key('email').eq(email)
)

end = time.time()

logger.info(f'{str(end-start)} seconds')

logger.info('get_item: ')

start = time.time()

response = client_dynamo.get_item(
  TableName=TABLE_NAME_EMAILS_CACHE,
  Key={
    'email': {
      'S': email
    }
  }
)

end = time.time()
logger.info(f'{str(end-start)} seconds')

ip = random.choice(generate_data_batch.IPS)

logger.info(f'measuring search for ip: {ip}')
logger.info('scan: ')
response = table_ip.scan(
  FilterExpression=Key('ip_address').eq(ip)
)

end = time.time()

logger.info(f'{str(end-start)} seconds')

logger.info(f'measuring batch get item for both')
response = client_dynamo.batch_get_item(
  RequestItems={
    TABLE_NAME_EMAILS_CACHE: {
      'Keys': [
        {
          'email':
            {
              'S': email
            }
        }
      ]
    },
    TABLE_NAME_IPS_CACHE: {
      'Keys': [
        {
          'ip_address':
            {
              'S': ip
            }
        }
      ]
    }

  },
  ReturnConsumedCapacity='NONE'
)

end = time.time()

logger.info(f'{str(end-start)} seconds')
logger.info(response)
