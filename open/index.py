import json
import boto3

dynamodbTable = boto3.resource('dynamodb').Table('WebSocket-Test-Table')

# Connect to new or existing websocket in dynamodb
def handler(event, context):
  currentId = event['requestContext']['connectionId']
  socketId = json.loads(event['body'])['socketId']
  domainName = event['requestContext']['domainName']
  stage = event['requestContext']['stage']
  endpoint_url = f'https://{domainName}/{stage}'

  if socketId == '':
    socketId = currentId
    apigateway = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)
    apigateway.post_to_connection(ConnectionId=currentId, Data=json.dumps({'socketId': currentId}))
  
  dynamodbTable.put_item(Item={
    'websocketUrl': endpoint_url,
    'socketId': socketId,
    'currentId': currentId
  })
  
  return {'statusCode': 200}
