import time
import boto3
import json

dynamodbTable = boto3.resource('dynamodb').Table('WebSocket-Test-Table')

def dynamodb_update(dynamodbTable, dynamodbKey, attribute):
  update_expression = []
  attribute_values = dict()

  for key, val in attribute.items():
    update_expression.append(f" {key} = :{key}")
    attribute_values[f":{key}"] = val
  update_expression = "SET " + ", ".join(update_expression)

  dynamodbTable.update_item(
    Key=dynamodbKey,
    UpdateExpression=update_expression,
    ExpressionAttributeValues=attribute_values
  )

def handler(event, context):
  endpoint_url = event['body']['endpoint']
  parentID = event['body']['parentID']
  currentTime = time.time()
  while (time.time() - currentTime < 20):
    message = json.dumps{
      'Time': '{:.1f} sec'.format(time.time() - currentTime)
    }
    dynamodbKey = {
        'websocketURL': endpoint_url,
        'parentID': parentID
      }
    dynamodb_update(dynamodbTable, dynamodbKey, {
      'message': message
    })
    time.sleep(1)