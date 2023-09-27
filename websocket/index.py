import json
import time
try:
  import boto3
except:
  pass

startTime = time.time()
IDs = {}

def response(responseCode, body):
  # Websocket lambda must return status code and stringified body
  return { 
    'statusCode': responseCode,
    'body': json.dumps(body)
  }
  
def disconnectHandler(apigw_management, connectionId, event):
  disconnectName = IDs[connectionId]
  IDs.pop(connectionId, None)
  data = json.dumps({
    'Left socket': disconnectName,
    'ID': connectionId,
    'Connections': len(IDs),
    'Time': '{:.1f} sec'.format(time.time() - startTime),
  })
  apigw_management.post_to_connection(ConnectionId=connectionId, Data=data)
  return data

def setNameHandler(apigw_management, connectionId, event):
  IDs[connectionId] = json.loads(event['body'])['Name']
  data = json.dumps({
    'Joined socket': IDs[connectionId],
    'ID': connectionId,
    'Connections': len(IDs),
    'Time': '{:.1f} sec'.format(time.time() - startTime),
  })
  apigw_management.post_to_connection(ConnectionId=connectionId, Data=data)
  return {'Name': IDs[connectionId] }

def pingHandler(apigw_management, connectionId, event):
  currentTime = time.time()
  while (time.time() - currentTime < 10):
    name = IDs[connectionId]
    data = json.dumps({
      'Ping from': name,
      'ID': connectionId,
      'Connections': len(IDs),
      'Time': '{:.1f} sec'.format(time.time() - startTime),
    })
    apigw_management.post_to_connection(ConnectionId=connectionId, Data=data)
    time.sleep(1)
  return data

def handler(event, context):
  try:
    connectionId = event['requestContext']['connectionId']
  except:
    return response(400, 'Request requestContext.connectionId does not exist')

  routeKey = event["requestContext"]["routeKey"]
  domainName = event['requestContext']['domainName']
  stage = event['requestContext']['stage']
  apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=f"https://{domainName}/{stage}")
  
  if routeKey == '$connect':
    data = 'Connected'
  elif routeKey == '$disconnect':
    data = disconnectHandler(apigw_management, connectionId, event)
  elif routeKey == 'setName':
    data = setNameHandler(apigw_management, connectionId, event)
  elif routeKey == 'ping':
    data = pingHandler(apigw_management, connectionId, event)

  return response(200, data)
        