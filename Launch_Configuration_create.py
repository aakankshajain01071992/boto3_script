import boto3

client = boto3.client('autoscaling')

response = client.create_launch_configuration(
    LaunchConfigurationName='launchconfig_name',
    ImageId='ami-4343232',
    KeyName='Name-of-Key',
    SecurityGroups=[
        'sg-23453',
    ],
    InstanceType='t2.small',
    BlockDeviceMappings=[
        {
            'VirtualName': '/dev/xvda',
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'SnapshotId': 'snap-435434345',
                'VolumeSize': 8,
                'VolumeType': 'gp2',
                'DeleteOnTermination': True,
                'Iops': 123,
                'Encrypted': False
            },
            'NoDevice': True|False
        },
    ],
    InstanceMonitoring={
        'Enabled': False
    },
    EbsOptimized=False,
    AssociatePublicIpAddress=True
)
