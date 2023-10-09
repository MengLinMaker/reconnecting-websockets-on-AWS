import json
import uuid
import time
import struct
import base64
import boto3

dynamodbTable = boto3.resource('dynamodb').Table('WebSocket-Test-Table')

def ulid():
  uuidByte = uuid.uuid4().bytes
  timeByte = struct.pack('!d', time.time())
  ulidString = base64.urlsafe_b64encode(timeByte+uuidByte).decode('ascii').strip("=")
  return ulidString

def dynamodb_update(dynamodbTable, dynamodbKey, attribute):
  condition_expression = []
  update_expression = []
  attribute_values = dict()
  
  for key, val in dynamodbKey.items():
    condition_expression.append(f'attribute_exists({key})')
  condition_expression = ' AND '.join(condition_expression)

  for key, val in attribute.items():
    update_expression.append(f' {key} = :{key}')
    attribute_values[f':{key}'] = val
  update_expression = 'SET ' + ', '.join(update_expression)

  dynamodbTable.update_item(
    Key=dynamodbKey,
    UpdateExpression=update_expression,
    ExpressionAttributeValues=attribute_values,
    ConditionExpression=condition_expression
  )

# Connect to new or existing websocket in dynamodb
def handler(event, context):
  currentId = event['requestContext']['connectionId']
  socketId = json.loads(event['body'])['socketId']
  domainName = event['requestContext']['domainName']
  stage = event['requestContext']['stage']
  endpoint_url = f'https://{domainName}/{stage}'

  apigateway = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)
  if socketId == '':
    socketId = ulid()
    TTL = int(time.time() + 60*5)
    apigateway.post_to_connection(ConnectionId=currentId, Data=json.dumps({'socketId': socketId}))
    dynamodbTable.put_item(Item={
      'socketUrl': endpoint_url,
      'socketId': socketId,
      'currentId': currentId,
      'TTL': TTL
    })
  else:
    dynamodb_update(dynamodbTable, {
      'socketUrl': endpoint_url,
      'socketId': socketId
    }, {
      'currentId': currentId
    })
  
  return {'statusCode': 200}
