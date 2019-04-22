#!/usr/bin/python
import boto3
import datetime, json

project = "XXXX"
iid = []
Metric_name = ['CPUUtilization','MemoryUtilization','DiskSpaceUtilizationforslash','DiskSpaceUtilizationfordata'] 
Alarm_Actions = ['arn:aws:sns:ap-southeast-1:3443434433434:XYZ']

# ASG - Name
asg_name = ["A","B","C","D"]

# Boto connection

session = boto3.Session(profile_name='abc')
cloudwatch = session.client('cloudwatch')
asg_client = session.client('autoscaling')
ec2client = session.client('ec2')

# List of Instances

for asgname in asg_name:
    response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asgname])
    all_asg = response['AutoScalingGroups']

    for i in range(len(all_asg)):
        count = 0 
        all_ec2s = all_asg[i]['Instances']
        for m in range(len(all_ec2s)):
            iid.append(all_ec2s[m]['InstanceId'])
ins_id = iid

# Describe and create alarm
AlarmNames=[]

for insid in ins_id:
	ins_ip=ec2client.describe_instances(InstanceIds=[insid])['Reservations'][0]['Instances'][0]['PublicIpAddress']
	for Metricname in Metric_name:
		if Metricname == 'CPUUtilization':
			threshold = 80.0
			dimensions =[{'Name': 'InstanceId','Value': insid}]
			AlarmNames.append('{0}-{2} {1} > {3}'.format(project,Metricname,ins_ip,threshold))
			Namespace='AWS/EC2'
		elif Metricname == 'MemoryUtilization':
			threshold = 90.0
			dimensions =[{'Name': 'InstanceId','Value': insid}]
			AlarmNames.append('{0}-{2} {1} > {3}'.format(project,Metricname,ins_ip,threshold))
			Namespace='AWS/EC2'
		elif Metricname == 'DiskSpaceUtilizationforslash':
			Metricname = "DiskSpaceUtilization"
			threshold = 80.0
			dimensions =[{'Name': 'InstanceId','Value': insid},{'Name': 'MountPath','Value': '/'},{'Name': 'Filesystem','Value': '/dev/xvda1'}]
			AlarmNames.append('{0}-{2} {1} for / > {3}'.format(project,Metricname,ins_ip,threshold))
			Namespace='System/Linux'
		elif Metricname == 'DiskSpaceUtilizationfordata':
			Metricname = "DiskSpaceUtilization"
			threshold = 80.0
			dimensions =[{'Name': 'InstanceId','Value': insid},{'Name': 'MountPath','Value': '/dev'},{'Name': 'Filesystem','Value': 'devtmpfs'}]
			AlarmNames.append('{0}-{2} {1} for /dev > {3}'.format(project,Metricname,ins_ip,threshold))
			Namespace='System/Linux'
			
		alarm_names = AlarmNames
		print  alarm_names
		paginator = cloudwatch.get_paginator('describe_alarms')
		for Alarm_Names in alarm_names:
			print Alarm_Names
			for response in paginator.paginate(AlarmNames=[Alarm_Names]):
				res=response['MetricAlarms']  
				if res == []:
					print "Alarm not set, we are setting alarm for that"
					'''# Create alarm
					cloudwatch.put_metric_alarm(
						AlarmName=Alarm_Names,
						ComparisonOperator='GreaterThanThreshold',
						EvaluationPeriods=1,
						MetricName=Metricname,
						Namespace=Namespace,
						Period=300,
						Statistic='Average',
						Threshold=threshold,
						ActionsEnabled=True,
						AlarmActions=Alarm_Actions,
						AlarmDescription='Alarm when {0} exceeds on server {1}'.format(Metricname,insid),
						Dimensions=dimensions
				)'''
				else:
					print "Alarm exist"
		AlarmNames= []
	
