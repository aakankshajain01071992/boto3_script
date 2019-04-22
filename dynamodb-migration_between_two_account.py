import boto3
import os

wd_session = boto3.Session(profile_name='abc')
dp_session = boto3.Session(profile_name='xyz')

wddynamoclient = wd_session.client('dynamodb')
dpdynamoclient = dp_session.client('dynamodb')

dynamopaginator = wddynamoclient.get_paginator('scan')
tabname='table_name'
targettabname='target_table_name'
dynamoresponse = dynamopaginator.paginate(
    TableName=tabname,
    Select='ALL_ATTRIBUTES',
    ReturnConsumedCapacity='NONE',
    ConsistentRead=True
)
for page in dynamoresponse:
    for item in page['Items']:
        print(item)
        dpdynamoclient.put_item(TableName=targettabname, Item=item)
