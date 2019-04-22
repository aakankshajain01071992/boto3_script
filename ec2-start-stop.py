#!/usr/bin/python3
import boto3
import collections
import datetime
import time
import json

ec2client = boto3.client('ec2')
ec2resource = boto3.resource('ec2')

# Manually provided instance Id
#ins_id = ["i-w65546666","i-87677888888"]

#Get list of running instance (Automatic)
filters = [
    {
       'Name': 'instance-state-name', 
       'Values': ['running'] # for check stop status 'stopped'  and for check running status 'running'
    }
 ]
    
# filter the instances based on filters() above
instances = ec2resource.instances.filter(Filters=filters)

for instance in instances:
    #print(instance)
    ins_id = instance.id
    print(ins_id)
    response = ec2client.stop_instances(
    	InstanceIds=[
    		ins_id,
       	],
    		Force=False
    	)
     #response = ec2client.start_instances(
     #    InstanceIds=[
     #        ins_id,
     #    ]
     #    )	
