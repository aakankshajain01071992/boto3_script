#!/usr/bin/python
import boto3, datetime
cloudwatch = boto3.client('cloudwatch')
response = cloudwatch.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name':'InstanceId', 'Value':'i-002c49224'}]
        )
print(response)
