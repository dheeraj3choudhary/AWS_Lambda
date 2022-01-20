### Author:- Dheeraj Choudhary

import boto3
ec2 = boto3.client('ec2')
sns_client = boto3.client('sns')
volumes = ec2.describe_volumes()

def lambda_handler(event, context):
    unused_volumes = []
    for vol in volumes['Volumes']:
        if len(vol['Attachments']) == 0:
            vol1 = ("-----Unused Volume ID = {}------".format(vol['VolumeId']))
            unused_volumes.append(vol1)
    
    #email
    sns_client.publish(
        TopicArn='<SNS Topic ARN>',
        Subject='Warning - Unused Volume List',
        Message=str(unused_volumes)
    )
    return "success"
