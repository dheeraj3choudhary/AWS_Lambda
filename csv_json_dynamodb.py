import boto3
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('user')
def lambda_handler(event, context):
    # First we will fetch bucket name from event json object
    bucket = event['Records'][0]['s3']['bucket']['name']
    # Now we will fetch file name which is uploaded in s3 bucket from event json object
    csv_file_name = event['Records'][0]['s3']['object']['key']
    #Lets call get_object() function which Retrieves objects from Amazon S3 as dictonary
    csv_object = s3_client.get_object(Bucket=bucket,Key=csv_file_name)
    file_reader = csv_object['Body'].read().decode("utf-8")
    print(file_reader)
    # Split a string into a list where each word is a list item
    users = file_reader.split("\n")
    # The filter() method filters the given sequence with the help of a function that tests each element in the sequence to be true or not.
    users = list(filter(None, users))
    #Now we will traverse throught the list pick elements one by one and push it to dynamodb table
    for user in users:
        user_data = user.split(",")
        table.put_item(Item = {
            "id" : user_data[0],
            "name" : user_data[1],
            "salary" : user_data[2]
        })
    return 'success'
