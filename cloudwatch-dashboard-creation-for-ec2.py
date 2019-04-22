#!/usr/bin/python
import boto3
import datetime, json
metrics = []
metric = []
ec2client = boto3.client('ec2')
ec2resource = boto3.resource('ec2')
instances = ec2resource.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
count = 0
for i in instances:
    if (count == 0):
        metric = ["AWS/EC2","CPUUtilization","InstanceId",i.id]
    else:
        metric = [".",".",".",i.id]
    metrics.append(metric)
    count +=1
print(metrics)

widget1 = {
         "type":"metric",
         "x":0,
         "y":0,
         "width":12,
         "height":6,
         "properties":{
            "view": "timeSeries",
            "metrics": metrics,
            "period": 300,
            "stat":"Average",
            "region":"ap-southeast-1",
            "title":"EC2 Instance CPU Utilization"
         }
      }
#print(widget1)
dashboard_body = { "widgets": [ widget1 ] }
dash_body = json.dumps(dashboard_body)
print(dash_body)

cwclient = boto3.client('cloudwatch')

response = cwclient.put_dashboard(
    DashboardName='All-Instance-CPU-Util',
    DashboardBody=dash_body
)
print(response)
exit()
