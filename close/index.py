import json
import boto3

dynamodbTable = boto3.resource('dynamodb').Table('WebSocket-Test-Table')

# Remove persistent websocket from dynamodb
def handler(event, context):
  parentID = json.loads(event['body'])['parentID']
  domainName = event['requestContext']['domainName']
  stage = event['requestContext']['stage']
  endpoint_url = f'https://{domainName}/{stage}'

  dynamodbTable.delete_item(Key={
    'websocketURL': endpoint_url,
    'parentID': parentID
  })

  return {'statusCode': 200}
