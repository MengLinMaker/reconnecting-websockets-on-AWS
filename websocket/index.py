import json
import time
try:
  import boto3
except:
  pass

startTime = time.time()
connectionIds = set()

def response(responseCode, body):
  # Websocket lambda must return status code and stringified body
  return { 
    'statusCode': responseCode,
    'body': json.dumps(body)
  }

def connectHandler(apigw_management, connectionId):
  pass
  
def disconnectHandler(apigw_management, connectionId):
  connectionIds.remove(connectionId)
  for loopConnectionId in list(connectionIds):
    data = json.dumps({
      'Your ID': loopConnectionId,
      'Just disconnected': connectionId,
      'Number of connections': len(connectionIds),
      'Time': f'{time.time() - startTime} seconds',
      'List IDs': list(connectionIds)
    })
    apigw_management.post_to_connection(ConnectionId=loopConnectionId, Data=data)

def defaultHandler(apigw_management, connectionId):
  for loopConnectionId in list(connectionIds):
    data = json.dumps({
      "Time": time.time() - startTime
    })
    apigw_management.post_to_connection(ConnectionId=loopConnectionId, Data=data)

def handler(event, context):
  connectionId = event.get('requestContext', {}).get('connectionId')
  if connectionId is None:
    return response(400, 'Request requestContext.connectionId does not exist')
  print('Adding connection')
  connectionIds.add(connectionId)

  try:
    eventType = event["requestContext"]["eventType"]
    domainName = event.get('requestContext',{}).get('domainName')
    stage = event.get('requestContext', {}).get('stage')
    apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=f"https://{domainName}/{stage}")
    if eventType == 'CONNECT':
      connectHandler(apigw_management, connectionId)
    elif eventType == 'DISCONNECT':
      disconnectHandler(apigw_management, connectionId)
    elif eventType == 'DEFAULT':
      defaultHandler(apigw_management, connectionId)
    
    return response(200, 'Connected')
  except:
    return response(400, 'Handler failed to execute')
