#!/usr/bin/python
import boto3
import datetime, json

project = "VOOT"
iid = []
asg_name = []
asgn = []
asg_Rep = []
Metric_name = ['CPUUtilization','MemoryUtilization','DiskSpaceUtilizationforslash','DiskSpaceUtilizationfordata'] 
Alarm_Actions = ['arn:aws:sns:ap-southeast-1:5455534334:asdf']

#content of file.txt
#name1:asg_name1
#name2:asg_name2
#name3:asg_name3


def asgname():
	asgName =[]
	f = open('/home/a/b/file.txt','r')
	for line in f:
		a = line.split(":")
		b = a[1].rstrip("\n")
		asgName.append(b)
	return (asgName)
        
        
def asg_repname(asgname):
    asgrep_list = ""
    found = False
    f = open('/home/a/b/file.txt','r')
    i=0
    lineList = []
    for line in f:
		lineList.append(line.rstrip("\n"))
		if asgname in lineList[i]:
			#a = lineList.split(":")
			#c = a[0]
			#b = a[1].rstrip("\n")
			#asgrep_list = c
			print lineList[i]
		return (asgrep_list)

# Boto connection

session = boto3.Session(profile_name='abc')
cloudwatch = session.client('cloudwatch')
asg_client = session.client('autoscaling')
ec2client = session.client('ec2')


# List of Instances
asg_name = asgname()
for asgname in asg_name:
    response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asgname])
    all_asg = response['AutoScalingGroups']
    condition = bool(True)
    for i in range(len(all_asg)):
		count = 0
		asgn = all_asg[i]['AutoScalingGroupName']
		all_ec2s = all_asg[i]['Instances']
		for m in range(len(all_ec2s)):
			scalein=all_ec2s[m]['ProtectedFromScaleIn']
			if scalein == condition:
				iid.append(all_ec2s[m]['InstanceId'])
				asgrep = asg_repname(asgn)
				#print asgn
				asg_Rep.append(asgrep)
ins_id = iid
#print ins_id
asg_rep = asg_Rep
#print asg_rep


# Describe and create alarm
AlarmNames=[]

for (insid,asgrep) in zip(ins_id,asg_rep):
	ins_ip = ec2client.describe_instances(InstanceIds=[insid])['Reservations'][0]['Instances'][0]['PublicIpAddress']
	rep = asgrep
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
						AlarmDescription='Alarm when {0} exceeds on server {1}'.format(Metricname,insid),
						Dimensions=dimensions
				)'''
				else:
					print "Alarm exist"
		AlarmNames= []
	

