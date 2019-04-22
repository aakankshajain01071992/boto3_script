#!/usr/bin/python
import boto3
import datetime, json
metrics = []
metrics2 = []
metrics3 = []
metric = []
metric2 = []
metric3 = []

ec2client = boto3.client('ec2')
ec2resource = boto3.resource('ec2')
instances = ec2resource.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
count = 0
for i in instances:
    if (count == 0):
        metric = ["AWS/EC2","CPUUtilization","InstanceId",i.id]
        metric2 = ["System/Linux","MemoryUtilization","InstanceId",i.id]
        metric3 = ["System/Linux","DiskUtilization","InstanceId",i.id]
    
    else:
        metric = [".",".",".",i.id]
        metric2= [".",".",".",i.id]
        metric3= [".",".",".",i.id]
    
    metrics.append(metric)
    metrics2.append(metric2)
    metrics3.append(metric3)
    count +=1
#print(metrics)

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


widget2 = {
         "type":"metric",
         "x":13,
         "y":0,
         "width":12,
         "height":6,
         "properties":{
            "view": "timeSeries",
            "metrics": metrics2,
            "period": 300,
            "stat":"Average",
            "region":"ap-southeast-1",
            "title":"EC2 Instance Memory Utilization"
         }
      }

widget3 = {
         "type":"metric",
         "x":23,
         "y":0,
         "width":12,
         "height":6,
         "properties":{
            "view": "timeSeries",
            "metrics": metrics2,
            "period": 300,
            "stat":"Average",
            "region":"ap-southeast-1",
            "title":"EC2 Instance Disk Utilization"
         }
      }



#print(widget1)
dashboard_body = { "widgets": [ widget1 , widget2 , widget3 ] }
dash_body = json.dumps(dashboard_body)
print(dash_body)


cwclient = boto3.client('cloudwatch')

response = cwclient.put_dashboard(
    DashboardName='All-Instance-Util',
    DashboardBody=dash_body
)
print(response)
exit()





