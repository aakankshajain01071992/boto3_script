#!/usr/bin/python
import boto3
import datetime, json

project = "VOOT"

iid = []
asgrep = []
Metric_name = ['CPUUtilization','MemoryUtilization','DiskSpaceUtilizationforslash','DiskSpaceUtilizationfordata'] 
Alarm_Actions = ['arn:aws:sns:ap-southeast-1:65657634:sdfd']

#content of file.txt
#name1:asg_name1
#name2:asg_name2
#name3:asg_name3

def asgname():
	asgName =[]
	asgRep = []
	f = open('/home/file.txt','r')
	for line in f:
		a = line.split(":")
		b = a[0]
		c = a[1].rstrip("\n")
		asgName.append(c)
		asgRep.append(b)
	return (asgName,asgRep)

# Boto connection

session = boto3.Session(profile_name='abc')
cloudwatch = session.client('cloudwatch')
asg_client = session.client('autoscaling')
ec2client = session.client('ec2')

# List of Instances
asg_name,asg_rep = asgname()
print asg_name
print asg_rep
for j,k in zip (asg_name,xrange(len(asg_rep))):
    response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[j])
    all_asg = response['AutoScalingGroups']
    condition = bool(True)
    for i in range(len(all_asg)):
        all_ec2s = all_asg[i]['Instances']
        for m in range(len(all_ec2s)):
			scalein=all_ec2s[m]['ProtectedFromScaleIn']
			if scalein == condition:
				iid.append(all_ec2s[m]['InstanceId'])

ins_id = iid
print ins_id

# Describe and create alarm
AlarmNames=[]

for insid in ins_id:
	ins_ip = ec2client.describe_instances(InstanceIds=[insid])['Reservations'][0]['Instances'][0]['PublicIpAddress']
	asgrep = "Test"
	for Metricname in Metric_name:
		if Metricname == 'CPUUtilization':
			threshold = 80.0
			dimensions =[{'Name': 'InstanceId','Value': insid}]
			AlarmNames.append('{0}-{1}-{2} {3} > {4}'.format(project,asgrep,ins_ip,Metricname,threshold))
			Namespace='AWS/EC2'
		elif Metricname == 'MemoryUtilization':
			threshold = 90.0
			dimensions =[{'Name': 'InstanceId','Value': insid}]
			AlarmNames.append('{0}-{1}-{2} {3} > {4}'.format(project,asgrep,ins_ip,Metricname,threshold))
			Namespace='AWS/EC2'
		elif Metricname == 'DiskSpaceUtilizationforslash':
			Metricname = "DiskSpaceUtilization"
			threshold = 80.0
			dimensions =[{'Name': 'InstanceId','Value': insid},{'Name': 'MountPath','Value': '/'},{'Name': 'Filesystem','Value': '/dev/xvda1'}]
			AlarmNames.append('{0}-{1}-{2} {3} for / > {4}'.format(project,asgrep,ins_ip,Metricname,threshold))
			Namespace='System/Linux'
		elif Metricname == 'DiskSpaceUtilizationfordata':
			Metricname = "DiskSpaceUtilization"
			threshold = 80.0
			dimensions =[{'Name': 'InstanceId','Value': insid},{'Name': 'MountPath','Value': '/dev'},{'Name': 'Filesystem','Value': 'devtmpfs'}]
			AlarmNames.append('{0}-{1}-{2} {3} for /dev > {4}'.format(project,asgrep,ins_ip,Metricname,threshold))
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
						AlarmDescription='Alarm when {0} exceeds on server {1}'.format(Metricname,j),
						Dimensions=dimensions
				)'''
				else:
					print "Alarm exist"
		AlarmNames= []
		
