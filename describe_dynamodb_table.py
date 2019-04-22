import boto3
import os

session = boto3.Session(profile_name='xyz')

dynamoclient = session.client('dynamodb')

dynamopaginator = dynamoclient.get_paginator('scan')
tabname='table_name'
dynamoresponse = dynamopaginator.paginate(
    TableName=tabname,
    Select='ALL_ATTRIBUTES',
    ReturnConsumedCapacity='NONE',
    ConsistentRead=True
)
for page in dynamoresponse:
    for item in page['Items']:
        print(item)
