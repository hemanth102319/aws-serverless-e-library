import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Books')

def lambda_handler(event, context):

    # 🔐 SAFE parsing
    if 'body' in event and event['body'] is not None:
        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']
    else:
        body = event

    table.put_item(
        Item={
            'BookID': body['BookID'],
            'Title': body['Title'],
            'Author': body['Author'],
            'TotalCopies': int(body['TotalCopies']),
            'AvailableCopies': int(body['TotalCopies'])
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Book added successfully')
    }
