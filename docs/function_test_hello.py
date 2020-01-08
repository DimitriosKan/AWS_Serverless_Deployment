import json

def lambda_handler(event, context):
    # TODO implement
    print("In lambda handler")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello world')
    }
