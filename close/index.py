import json
import boto3

dynamodbTable = boto3.resource('dynamodb').Table('WebSocket-Test-Table')

# Remove persistent websocket from dynamodb
def handler(event, context):
  socketId = json.loads(event['body'])['socketId']
  domainName = event['requestContext']['domainName']
  stage = event['requestContext']['stage']
  endpoint_url = f'https://{domainName}/{stage}'

  dynamodbTable.delete_item(Key={
    'websocketUrl': endpoint_url,
    'socketId': socketId
  })

  return {'statusCode': 200}
