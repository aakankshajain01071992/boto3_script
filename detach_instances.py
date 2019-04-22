#!/usr/bin/python
import boto3
from urllib2 import urlopen

instanceid = "0.0.0.0"
print instanceid

client = boto3.client('autoscaling')

response = client.detach_instances(
   InstanceIds=[
       instanceid,
   ],
   AutoScalingGroupName='Auth-Testing-Environment-ASG',
   ShouldDecrementDesiredCapacity=False
)
