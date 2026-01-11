import boto3
import json
from datetime import datetime

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):

    # Safe body parsing
    if 'body' in event and event['body'] is not None:
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    else:
        body = event

    dynamodb.transact_write_items(
        TransactItems=[
            {
                "Update": {
                    "TableName": "Books",
                    "Key": {
                        "BookID": {"S": body['BookID']}
                    },
                    "UpdateExpression": "SET AvailableCopies = AvailableCopies - :one",
                    "ConditionExpression": "AvailableCopies > :zero",
                    "ExpressionAttributeValues": {
                        ":one": {"N": "1"},
                        ":zero": {"N": "0"}
                    }
                }
            },
            {
                "Put": {
                    "TableName": "IssueRecords",
                    "Item": {
                        "IssueID": {"S": body['IssueID']},
                        "BookID": {"S": body['BookID']},
                        "MemberID": {"S": body['MemberID']},
                        "IssueDate": {"S": datetime.utcnow().isoformat()},
                        "ReturnDate": {"NULL": True}
                    }
                }
            }
        ]
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Book issued successfully")
    }
