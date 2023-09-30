import json
import time
import boto3

dynamodbTable = boto3.resource('dynamodb').Table('WebSocket-Test-Table')

def dynamodb_update(dynamodbTable, key, attribute):
  update_expression = []
  attribute_values = dict()
  attribute_names = dict()

  for key, val in attribute.items():
    update_expression.append(f" #{key} = :{key}")
    attribute_values[f":{key}"] = val
    attribute_names[f"#{key}"] = key
  update_expression = "SET " + ", ".join(update_expression)

  print(update_expression)
  print(attribute_names)
  print(attribute_values)

  dynamodbTable.update_item(
    Key=key,
    UpdateExpression=update_expression,
    ExpressionAttributeNames=attribute_names,
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
      dynamodbKey = {
        'websocketURL': endpoint_url,
        'parentID': currentID
      }
      postToClient({'parentID': currentID})
      dynamodbTable.put_item(Item={
        'websocketURL': endpoint_url,
        'parentID': currentID,
        'currentID': currentID
      })
      print('Dynamo Create')
    else:
      result = dynamodbTable.get_item(Key=dynamodbKey)
      print(result['Item'])
      postToClient({
        'currentID': currentID
      })
      dynamodb_update(dynamodbTable, {
        'websocketURL': endpoint_url,
        'parentID': parentID
      }, {
        'currentID': currentID
      })
      print('Dynamo Update')
  elif routeKey == 'close':
    parentID = json.loads(event['body'])['parentID']
    dynamodbKey = {
      'websocketURL': endpoint_url,
      'parentID': parentID
    }
    # Reset values to default for full disconnect
    dynamodbTable.delete_item(Key=dynamodbKey)
    postToClient({
      'parentID': ''
    })
    print('Dynamo Close')

  return {'statusCode': 200}






def pingHandler(apigateway, currentID, event):
  currentTime = time.time()
  while (time.time() - currentTime < 10):
    data = json.dumps({
      'ID': currentID,
      'Time': '{:.1f} sec'.format(time.time() - currentTime),
    })
    apigateway.post_to_connection(ConnectionId=currentID, Data=data)
    time.sleep(1)