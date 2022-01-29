import boto3
import json
import ast
s3_client = boto3.client('s3')
dynamodb_client = boto3.resource('dynamodb')
def lambda_handler(event, context):
    # First we will fetch bucket name from event json object
    bucket = event['Records'][0]['s3']['bucket']['name']
    # Now we will fetch file name which is uploaded in s3 bucket from event json object
    json_file_name = event['Records'][0]['s3']['object']['key']
    #Lets call get_object() function which Retrieves objects from Amazon S3 as dictonary
    json_object = s3_client.get_object(Bucket=bucket,Key=json_file_name)
    # Lets decode the json object returned by function which will retun string
    file_reader = json_object['Body'].read().decode("utf-8")
    # We will now change this json string to dictonary
    file_reader = ast.literal_eval(file_reader)
    # As we have retrieved the dictionary we will put it in dynamodb table
    table = dynamodb_client.Table('user')
    table.put_item(Item=file_reader)
    return 'success'
