import boto3
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
books_table = dynamodb.Table('Books')
issue_table = dynamodb.Table('IssueRecords')

def lambda_handler(event, context):
    # 1️⃣ Safe body parsing
    if 'body' in event and event['body'] is not None:
        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']
    else:
        body = event

    # 2️⃣ Input validation
    required_fields = ['IssueID', 'ReturnDate']
    for field in required_fields:
        if field not in body:
            return {
                'statusCode': 400,
                'body': json.dumps(f"Missing field: {field}")
            }

    issue_id = body['IssueID']
    return_date = body['ReturnDate']

    try:
        # 3️⃣ Check if issue record exists
        issue_record = issue_table.get_item(Key={'IssueID': issue_id})
        if 'Item' not in issue_record:
            return {
                'statusCode': 404,
                'body': json.dumps(f"IssueID {issue_id} not found")
            }

        book_id = issue_record['Item']['BookID']

        # 4️⃣ Update ReturnDate in IssueRecords
        issue_table.update_item(
            Key={'IssueID': issue_id},
            UpdateExpression="SET ReturnDate = :rd",
            ExpressionAttributeValues={':rd': return_date}
        )

        # 5️⃣ Update Book status to Available
        books_table.update_item(
            Key={'BookID': book_id},
            UpdateExpression="SET #s = :status",
            ExpressionAttributeNames={'#s': 'Status'},
            ExpressionAttributeValues={':status': 'Available'}
        )

        # 6️⃣ Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f"Book {book_id} successfully returned",
                'IssueID': issue_id
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal server error: {str(e)}")
        }
