import json
import boto3

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
  # Track original ID for old messages
  currentID = event['requestContext']['connectionId']

  domainName = event['requestContext']['domainName']
  stage = event['requestContext']['stage']
  endpoint_url = f"https://{domainName}/{stage}"
  apigateway = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)
  
  def postToClient(data):
    apigateway.post_to_connection(ConnectionId=currentID, Data=json.dumps(data))

  routeKey = event["requestContext"]["routeKey"]
  if routeKey == 'open':
    parentID = json.loads(event['body'])['parentID']
    if parentID == '':
      dynamodbTable.put_item(Item={
        'websocketURL': endpoint_url,
        'parentID': currentID,
        'currentID': currentID
      })
      postToClient({'parentID': currentID})
    else:
      dynamodbKey = {
        'websocketURL': endpoint_url,
        'parentID': parentID
      }
      dynamodb_update(dynamodbTable, dynamodbKey, {'currentID': currentID})
  elif routeKey == 'close':
    parentID = json.loads(event['body'])['parentID']
    dynamodbKey = {
      'websocketURL': endpoint_url,
      'parentID': parentID
    }
    # Reset values to default for full disconnect
    dynamodbTable.delete_item(Key=dynamodbKey)
    postToClient({'parentID': ''})

  return {'statusCode': 200}
