import boto3

ec2client = boto3.client('ec2')

resp = ec2client.describe_images(ImageIds=['ami-7d89b501'])
print(resp['Images'][0]['State'])
print(resp['Images'][0]['BlockDeviceMappings'][0])
print(resp['Images'][0]['BlockDeviceMappings'][0]['DeviceName'])
print(resp['Images'][0]['BlockDeviceMappings'][0]['Ebs']['SnapshotId'])
print(resp['Images'][0]['BlockDeviceMappings'][0]['Ebs']['DeleteOnTermination'])
print(resp['Images'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeType'])
print(resp['Images'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeSize'])
