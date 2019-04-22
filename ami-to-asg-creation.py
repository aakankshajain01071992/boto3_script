#!/usr/bin/python3
import boto3
import collections
import datetime
import time
from termcolor import colored


Date = time.strftime("%d%m%y")
Time = time.strftime("%H%M%S")
Name = "XXXXX"
AsgName = "YYYYY"
instance_ip = "0.0.0.0"
ami_description = "{0} AMI created on {1}".format(Name, Date)
ami_name = "{0}-{1}-{2}".format(Name, Date, Time)
lc_name = "{0}-{1}-{2}".format(Name, Date, Time)
asg_name = "{0}".format(AsgName)


def get_image_details_on_available(image_id):
    try:
        available = 0
        while available == 0:
            print("AMI Not created yet.. Checking again in 15 seconds.")
            time.sleep(15)
            image = ec2client.describe_images(ImageIds=[image_id])
            if image['Images'][0]['State'] == 'available':
                available = 1
        if available == 1:
            print("AMI is now available for use.")
            return image
    except e:
        return e


ec2client = boto3.client('ec2')
ec2resource = boto3.resource('ec2')
asgclient = boto3.client('autoscaling')
instances = ec2resource.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']},
                 {'Name': 'ip-address', 'Values': [instance_ip]}])

for instance in instances:
    inst_id = instance.id
    inst_type = instance.instance_type
    inst_pub_ip = instance.public_ip_address
    inst = instance
    print(inst_id, inst_type, inst_pub_ip,
          instance.platform, instance.tags[0]["Value"])
    response = ec2client.create_image(
            Description=ami_description,
            DryRun = True,
            InstanceId=inst_id,
            Name=ami_name,
            NoReboot=True)
    print("New AMI ID : {0}".format(response['ImageId']))
    img = get_image_details_on_available(response['ImageId'])

    #For specific ImageID
    #imgid = "ami-XYZ"
    #img = get_image_details_on_available(imgid)
    if(isinstance(img, dict)):
        print("Snapshot ID : {0}".format(
            img['Images'][0]['BlockDeviceMappings'][0]['Ebs']['SnapshotId']))
        print("Device Name : {0}".format(
            img['Images'][0]['BlockDeviceMappings'][0]['DeviceName']))
        print("Volume Type : {0}".format(
            img['Images'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeType']))
        print("Volume Size : {0}".format(
            img['Images'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeSize']))
        print("Delete on Termination : {0}".format(
            img['Images'][0]['BlockDeviceMappings'][0]['Ebs']
            ['DeleteOnTermination']))

        lc = asgclient.create_launch_configuration(
                LaunchConfigurationName=lc_name,
                ImageId=response['ImageId'],
                InstanceId=inst_id)

        lcdesc = asgclient.describe_launch_configurations(
                LaunchConfigurationNames=[lc_name])
        lcs = lcdesc['LaunchConfigurations']
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

        updateASG = asgclient.update_auto_scaling_group(
                AutoScalingGroupName = asg_name,
                MinSize=1,
                MaxSize=1,
                DesiredCapacity=1,
                LaunchConfigurationName = lc_name)

        asg_desc = asgclient.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
        all_asg = asg_desc['AutoScalingGroups']
        for i in range(len(all_asg)):
            print("------------------------------")
            print("ASG Name: {0}".format(colored(all_asg[i]['AutoScalingGroupName'], 'cyan')))
            print("Desired Capacity: {0}".format(colored(all_asg[i]['DesiredCapacity'], 'cyan')))
            print("Minimum Size: {0}".format(colored(all_asg[i]['MinSize'], 'cyan')))
            print("Maximum Size: {0}".format(colored(all_asg[i]['MaxSize'], 'cyan')))
            print("Default Cooldown: {0}".format(colored(all_asg[i]['DefaultCooldown'], 'cyan')))
            print("Created Time: {0}".format(colored(all_asg[i]['CreatedTime'], 'cyan')))
            print("Launch Configuration Name: {0}".format(colored(all_asg[i]['LaunchConfigurationName'], 'cyan')))
            all_lbs = all_asg[i]['LoadBalancerNames']
            for l in range(len(all_lbs)):
                print("Load Balancer: {0}".format(colored(all_lbs[l], 'cyan')))
            all_ec2s = all_asg[i]['Instances']
            print("Instance Details")
            for m in range(len(all_ec2s)):
                print(all_ec2s)
                print("- Instance Id: {0}".format(colored(all_ec2s[m]['InstanceId'], 'cyan')))
                print("- Protected From Scale In: {0}".format(colored(all_ec2s[m]['ProtectedFromScaleIn'], 'cyan')))
                if 'LaunchConfigurationName' in all_ec2s[m]:
                    print("- Launch Configuration Name: {0}".format(colored(all_ec2s[m]['LaunchConfigurationName'], 'cyan')))
    else:
        print(img)

