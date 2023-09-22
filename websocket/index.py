import json
import time
try:
  import boto3
except:
  pass

connectionIds = []

def response(responseCode, body):
  return json.dumps({ 
    'statusCode': responseCode,
    'body': body
  })

def connectHandler(apigw_management, connectionId):
  for yourConnectionId in connectionIds:
    data = response(200, {
      'Your ID': yourConnectionId,
      'Just connected': connectionId,
      'Number of connections': len(connectionIds),
      'Time': f'{time.time()} seconds',
      'List IDs': connectionIds
    })
    apigw_management.post_to_connection(ConnectionId=connectionId, Data=data)
  
def disconnectHandler(apigw_management, connectionId):
  for yourConnectionId in connectionIds:
    data = response(200, {
      'Your ID': yourConnectionId,
      'Just disconnected': connectionId,
      'Number of connections': len(connectionIds),
      'Time': f'{time.time()} seconds',
      'List IDs': connectionIds
    })
  apigw_management.post_to_connection(ConnectionId=connectionId, Data=data)

def defaultHandler(apigw_management, connectionId):
  for yourConnectionId in connectionIds:
    data = response(200, {
      'Your ID': yourConnectionId,
      'Default ID': connectionId,
      'Number of connections': len(connectionIds),
      'Time': f'{time.time()} seconds',
      'List IDs': connectionIds
    })
  apigw_management.post_to_connection(ConnectionId=connectionId, Data=data)

def handler(event, context):
  connectionId = event.get('requestContext',{}).get('connectionId')
  if connectionId is None:
    return response(400, 'Request requestContext.connectionId does not exist')
  connectionIds.append(connectionId)
  
  try:
    eventType = event["requestContext"]["eventType"]
    domainName = event.get('requestContext',{}).get('domainName')
    stage = event.get('requestContext',{}).get('stage')
    apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=F"https://{domainName}/{stage}")
    if eventType == 'connect':
      return connectHandler(apigw_management, connectionId)
    elif eventType == 'disconnect':
      return disconnectHandler(apigw_management, connectionId)
    elif eventType == 'default':
      return defaultHandler(apigw_management, connectionId)
  except:
    return response(400, 'Handler failed to execute')

  return
