#!/usr/bin/python
import boto3
client = boto3.client('dynamodb')

response = client.get_item(
   TableName = "sample_test",
   Key = {
       "title":"munich"
   })
print(response)

response = client.update_item(
   TableName = "sample_test",
   Key = {
       "title":"munich"
   },
   UpdateExpression = "SET director = :label",
   ExpressionAttributeValues = { 
       ":label": "Aakanksha"
   })
print(response)
