#!/usr/bin/python3
import boto3
import collections
import datetime
import time
from sys import argv
import smtplib


htmldoc = '<html><body><table border="1" style="width:100%; border-collapse: collapse; border: 1px solid black; padding: 2px;">'
htmldoc += "<tr style='background:grey;'><td colspan='2'>Provided Input Details</td></tr>"
htmldoc += "<tr><td>Instance IP</td><td>{0}</td></tr>".format(argv[1])
htmldoc += "<tr><td>AMI Name</td><td>{0}</td></tr>".format(argv[2])
htmldoc += "<tr><td>AMI Description</td><td>{0}</td></tr>".format(argv[3])
htmldoc += "<tr><td>Launch Configuration Name</td><td>{0}</td></tr>".format(argv[4])
htmldoc += "<tr><td>ASG Name</td><td>{0}</td></tr>".format(argv[5])

Date = time.strftime("%B-%d-%Y")
Time = time.strftime("%H:%M:%S")
instance_ip = "{0}".format(argv[1])
ami_name = "{0}".format(argv[2])
ami_description = "{0} created on {1}".format(argv[3], Date)
lc_name = "{0}".format(argv[4])
asg_name = "{0}".format(argv[5])



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
    htmldoc += "<tr style='background:grey;'><td colspan='2'>Instance Details</td></tr>"
    htmldoc += "<tr><td>Instance ID</td><td>{0}</td></tr>".format(inst_id)
    htmldoc += "<tr><td>Instance Type</td><td>{0}</td></tr>".format(inst_type)
    htmldoc += "<tr><td>Instance IP</td><td>{0}</td></tr>".format(inst_pub_ip)
    response = ec2client.describe_image(
            Name=ami_name,
    )
    print("AMI ID : {0}".format(response['ImageId']))
    img = get_image_details_on_available(response['ImageId'])

    #For specific ImageID
    #imgid = "ami-XYZ"
    #img = get_image_details_on_available(imgid)
        
    if(isinstance(img, dict)):
        htmldoc += "<tr style='background:grey;'><td colspan='2'>AMI Details</td></tr>"
        htmldoc += "<tr><td>AMI ID</td><td>{0}</td></tr>".format(imgid)
        htmldoc += "<tr><td>Snapshot ID</td><td>{0}</td></tr>".format(
            img['Images'][0]['BlockDeviceMappings'][0]['Ebs']['SnapshotId'])
        htmldoc += "<tr><td>Device Name</td><td>{0}</td></tr>".format(
            img['Images'][0]['BlockDeviceMappings'][0]['DeviceName'])
        htmldoc += "<tr><td>Volume Type</td><td>{0}</td></tr>".format(
            img['Images'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeType'])
        htmldoc += "<tr><td>Volume Size</td><td>{0}</td></tr>".format(
            img['Images'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeSize'])
        htmldoc += "<tr><td>Delete on Termination</td><td>{0}</td></tr>".format(
            img['Images'][0]['BlockDeviceMappings'][0]['Ebs']
            ['DeleteOnTermination'])

        #lc = asgclient.create_launch_configuration(
        #        LaunchConfigurationName=lc_name,
        #        ImageId=response['ImageId'],
        #        InstanceId=inst_id)

        lcdesc = asgclient.describe_launch_configurations(
                LaunchConfigurationNames=[lc_name])
        lcs = lcdesc['LaunchConfigurations']
        for i in range(len(lcs)):
            htmldoc += "<tr style='background:grey;'><td colspan='2'>Launch Configuration Details</td></tr>"
            htmldoc += "<tr><td>Launch Configuration Name</td><td>{0}</td></tr>".format(lcs[i]['LaunchConfigurationName'])
            htmldoc += "<tr><td>Image Id</td><td>{0}</td></tr>".format(lcs[i]['ImageId'])
            htmldoc += "<tr><td>Key Name</td><td>{0}</td></tr>".format(lcs[i]['KeyName'])
            htmldoc += "<tr><td>Instance Type</td><td>{0}</td></tr>".format(lcs[i]['InstanceType'])
            htmldoc += "<tr><td>Create Time</td><td>{0}</td></tr>".format(lcs[i]['CreatedTime'])
            htmldoc += "<tr><td>EBS Obtimized</td><td>{0}</td></tr>".format(lcs[i]['EbsOptimized'])
            sgs = lcs[i]['SecurityGroups']
            for l in range(len(sgs)):
                htmldoc += "<tr><td>Security Group</td><td>{0}</td></tr>".format(sgs[l])
            bdm = lcs[i]['BlockDeviceMappings']
            for m in range(len(bdm)):
                htmldoc += "<tr><td>Device Name</td><td>{0}</td></tr>".format(bdm[m]['DeviceName'])
                htmldoc += "<tr><td>Snapshot ID</td><td>{0}</td></tr>".format(bdm[m]['Ebs']['SnapshotId'])
                htmldoc += "<tr><td>Volume Size</td><td>{0}</td></tr>".format(bdm[m]['Ebs']['VolumeSize'])
                htmldoc += "<tr><td>Volume Type</td><td>{0}</td></tr>".format(bdm[m]['Ebs']['VolumeType'])
                htmldoc += "<tr><td>Delete on Termination</td><td>{0}</td></tr>".format(bdm[m]['Ebs']['DeleteOnTermination'])

        #updateASG = asgclient.update_auto_scaling_group(
        #        AutoScalingGroupName = asg_name,
        #        MinSize=1,
        #        MaxSize=1,
        #        DesiredCapacity=1,
        #        LaunchConfigurationName = lc_name)

        asg_desc = asgclient.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
        all_asg = asg_desc['AutoScalingGroups']
        for i in range(len(all_asg)):
            htmldoc += "<tr style='background:grey;'><td colspan='2'>Auto Scaling Group Details</td></tr>"
            htmldoc += "<tr><td>ASG Name</td><td>{0}</td></tr>".format(all_asg[i]['AutoScalingGroupName'])
            htmldoc += "<tr><td>Desired Capacity</td><td>{0}</td></tr>".format(all_asg[i]['DesiredCapacity'])
            htmldoc += "<tr><td>Minimum Size</td><td>{0}</td></tr>".format(all_asg[i]['MinSize'])
            htmldoc += "<tr><td>Maximum Size</td><td>{0}</td></tr>".format(all_asg[i]['MaxSize'])
            htmldoc += "<tr><td>Default Cooldown</td><td>{0}</td></tr>".format(all_asg[i]['DefaultCooldown'])
            htmldoc += "<tr><td>Created Time</td><td>{0}</td></tr>".format(all_asg[i]['CreatedTime'])
            htmldoc += "<tr><td>Launch Configuration Name</td><td>{0}</td></tr>".format(all_asg[i]['LaunchConfigurationName'])
            all_lbs = all_asg[i]['LoadBalancerNames']
            for l in range(len(all_lbs)):
                htmldoc += "<tr><td>Load Balancer</td><td>{0}</td></tr>".format(all_lbs[l])
            all_ec2s = all_asg[i]['Instances']
            htmldoc += "<tr style='background:grey;'><td colspan='2'>EC2 Instances present in ASG</td></tr>"
            for m in range(len(all_ec2s)):
                htmldoc += "<tr><td>Instance Id</td><td>{0}</td></tr>".format(all_ec2s[m]['InstanceId'])
                htmldoc += "<tr><td>Protected From Scale In</td><td>{0}</td></tr>".format(all_ec2s[m]['ProtectedFromScaleIn'])
                if 'LaunchConfigurationName' in all_ec2s[m]:
                    htmldoc += "<tr><td>Launch Configuration Name</td><td>{0}</td></tr>".format(all_ec2s[m]['LaunchConfigurationName'])
    else:
        htmldoc += "<tr><td colspan='2'>Error in AMI Creation. Exiting.</td></tr>"
        htmldoc += "<tr><td colspan='2'>{0}</td></tr>".format(img)

htmldoc += "</table></body></html>"
# Send Mail
mailto = 'XXXX@YYYY.net'
mailcc = ['XXXX@YYYY.com']
#mailcc = ['']
maillist = [mailto] + mailcc
mailfrom = 'XXXX@YYYY.net'
user = 'user_name'
pwd = 'password'
smtpserver = smtplib.SMTP("smtp_hostname",port_number)
smtpserver.ehlo()
smtpserver.ehlo() # extra characters to permit edit
smtpserver.login(user, pwd)
header = 'MIME-Version: 1.0' + "\r\n";
header = header + 'Content-type: text/html; charset=iso-8859-1' + "\r\n";
header = header + 'To:' + mailto + '\n' + 'From:' + mailfrom + '\n' + 'Subject: AMI Creation Report\n'
msg = header + '\n' + htmldoc + '\r\n'
smtpserver.sendmail(mailfrom, maillist, msg)
smtpserver.quit()
