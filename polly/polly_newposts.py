import boto3
import os
import uuid


def lambda_handler(event, context):
    recordId = str(uuid.uuid4())
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    voice = event["voice"]
    text = event["text"]
    # print('Generating new DynamoDB record, with ID:' + recordId)
    # print('Input Text:' + text)
    # print('Selected voice:' + voice)

    # Createing new record in DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    table.put_item(
        Item={
            'id': recordId,
            'text': text,
            'voice': voice,
            'status': 'PROCESSING',
            'ctime': ctime
        }
    )

    # Sending notification about new post to SNS
    client = boto3.client('sns')
    client.publish(
        TopicArn=os.environ['SNS_TOPIC'],
        Message=recordId
    )
    return recordId