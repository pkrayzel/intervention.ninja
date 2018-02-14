import boto3

client = boto3.client('ses')

response = client.send_templated_email(
    Source='no-reply@intervention.ninja',
    Destination={
        'ToAddresses': [
            'pkrayzel@gmail.com',
        ]
    },
    Template='intervention-ninja-smell',
    TemplateData="{}"
)

print(response)
