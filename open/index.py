import json
import boto3

dynamodbTable = boto3.resource('dynamodb').Table('WebSocket-Test-Table')

# Connect to new or existing websocket in dynamodb
def handler(event, context):
  currentID = event['requestContext']['connectionId']
  parentID = json.loads(event['body'])['parentID']
  domainName = event['requestContext']['domainName']
  stage = event['requestContext']['stage']
  endpoint_url = f'https://{domainName}/{stage}'

  if parentID == '':
    parentID = currentID
    apigateway = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)
    apigateway.post_to_connection(ConnectionId=currentID, Data=json.dumps({'parentID': currentID}))
  
  dynamodbTable.put_item(Item={
    'websocketURL': endpoint_url,
    'parentID': parentID,
    'currentID': currentID
  })
  
  return {'statusCode': 200}
