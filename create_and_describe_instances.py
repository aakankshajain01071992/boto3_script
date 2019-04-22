#!/usr/bin/python3
import boto3

#for describing instances
ec2 = boto3.client('ec2') # creating the connection
response = ec2.describe_instances()
print(response)


# for launching new instances
ec2.create_instances(ImageId='<ami-image-id>', MinCount=1, MaxCount=5)


