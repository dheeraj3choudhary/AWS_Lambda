### Author:-Dheeraj Choudhary
import boto3
ec2 = boto3.client('ec2')
sns_client = boto3.client('sns')
instances = ec2.describe_instances()
def lambda_handler(event, context):
    used_ami = []  # Create empty list to save used ami
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            state = instance['State']
            state = (state['Name'])
            if state == 'running':
                used_ami.append(instance['ImageId'])

    # Remove duplicate entries from list
    used_ami = list(set(used_ami))

    # Get all images from account in available state
    images = ec2.describe_images(
        Filters=[
            {
                'Name': 'state',
                'Values': ['available']
            },
        ],
        Owners=['self'],
    )

    # Traverse dictonary returned and fetch Image ID and append in list
    custom_ami = []  # Create empty list to save custom ami
    for image in images['Images']:
        custom_ami.append(image['ImageId'])

    # Check if custom ami is there in used AMI list if not deregister the AMI
    deregister_list = []
    for ami in custom_ami:
        if ami not in used_ami:
            print("AMI {} has been deregistered".format(ami))
            ec2.deregister_image(ImageId=ami)
            deg = ("-----Unused AMI ID = {} is Deregistered------".format(ami))
            deregister_list.append(deg)
            
     sns_client.publish(
        TopicArn='<SNS Topic ARN>',
        Subject='Alert - Unused AMIs Are Deregistered',
        Message=str(deregister_list)
    )
    return "success"
