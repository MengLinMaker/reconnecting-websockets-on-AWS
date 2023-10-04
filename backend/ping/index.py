import time
import boto3
import json

dynamodbTable = boto3.resource('dynamodb').Table('WebSocket-Test-Table')

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

def handler(event, context):
  body = json.loads(event['body'])
  dynamodbKey = {
    'socketUrl': body['endpoint'],
    'socketId': body['socketId']
  }

  currentTime = time.time()
  while (time.time() - currentTime < 20):
    message = json.dumps({
      'Time': '{:.1f} sec'.format(time.time() - currentTime)
    })
    dynamodb_update(dynamodbTable, dynamodbKey, {'message': message})
    time.sleep(2.5)

  response = {
    'statusCode': 200,
    'headers': {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': 'true',
    }
  }
  return response