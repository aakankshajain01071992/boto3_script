import boto3
import datetime
from termcolor import colored

client = boto3.client('autoscaling')

response = client.describe_launch_configurations()
lcs = response['LaunchConfigurations']
for i in range(len(lcs)):
    print("------------------------------")
    print("Launch Configuration Name: {0}".format(colored(lcs[i]['LaunchConfigurationName'], 'cyan')))
    print("Image Id: {0}".format(colored(lcs[i]['ImageId'], 'cyan')))
    print("Key Name: {0}".format(colored(lcs[i]['KeyName'], 'cyan')))
    print("Instance Type: {0}".format(colored(lcs[i]['InstanceType'], 'cyan')))
    print("Create Time: {0}".format(colored(lcs[i]['CreatedTime'], 'cyan')))
    print("EBS Obtimized: {0}".format(colored(lcs[i]['EbsOptimized'], 'cyan')))
    sgs = lcs[i]['SecurityGroups']
    for l in range(len(sgs)):
        print("Security Group: {0}".format(colored(sgs[l], 'cyan')))
    bdm = lcs[i]['BlockDeviceMappings']
    for m in range(len(bdm)):
        print("Device Name: {0}".format(colored(bdm[m]['DeviceName'], 'cyan')))
        print("Snapshot ID: {0}".format(colored(bdm[m]['Ebs']['SnapshotId'], 'cyan')))
        print("Volume Size: {0}".format(colored(bdm[m]['Ebs']['VolumeSize'], 'cyan')))
        print("Volume Type: {0}".format(colored(bdm[m]['Ebs']['VolumeType'], 'cyan')))
        print("Delete on Termination: {0}".format(colored(bdm[m]['Ebs']['DeleteOnTermination'], 'cyan')))
