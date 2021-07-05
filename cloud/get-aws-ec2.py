#!/usr/bin/env python3

import boto3
import boto3.session
import os
from datetime import datetime

# Setup the crendentials that api calls
my_session = boto3.session.Session(
    aws_access_key_id = 'AKIA5OTdasdaOJDYI',
    aws_secret_access_key = 'UXD3bNrNXasdas/R5L79N2sXL4'
)


# Set the file path
base_dir = "/home/ec2-user/environment/ec2/"
file_name = os.path.join(base_dir, "aws-%s.txt" % (datetime.now().strftime("%Y-%m-%d")))

def get_instances(region):
    
    
    ec2 = my_session.client('ec2', region_name=region)
    # ssm = my_session.client('ssm', region_name=region)
    # Get the all EC2 information
    instances = ec2.describe_instances()
    
    for response in instances['Reservations']:
        instance = response['Instances'][0]
        
        ins = []
        ins.append("AWS")
        ins.append(instance['InstanceId'])
        ins.insert(1,instance['PrivateIpAddress'])
        ins.append(instance['InstanceType'])
        ins.append(instance['Placement']['AvailabilityZone'])
        ins.append(instance['Platform']) if instance.get('Platform') else ins.append('Linux')
        ins.append(instance['State'].get('Name'))
        
        ins_str = ' '.join(ins)
        
        # Write the info into the file
        with open(file_name, 'a+') as f:
            f.write(ins_str + '\n')

get_instances('eu-west-1')
get_instances('ap-south-1')
    
