### Author:-Dheeraj Choudhary
import boto3
import json
s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')
def lambda_handler(event, context):
    # First we will fetch bucket name from event json object
    bucket = event['Records'][0]['s3']['bucket']['name']
    # Now we will fetch file name which is uploaded in s3 bucket from event json object
    file_key = ['Records'][0]['s3']['object']['key']
    #Lets call get_object() function which Retrieves objects from Amazon S3 as dictonary
    response = s3_client.get_object(Bucket='bucket', Key='file_key')
    file_reader = response['Body'].read()
    file_dic = json.loads(file_reader)
    # As we have retrieved the dictionary from json object we will put it in dynamodb table
    table = dynamodb_client.Table('user')
    table.put_item(Item=file_dic)
    return 'success'
