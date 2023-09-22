import json
import boto3
import time

connectionIds = []

def connectHandler(apigw_management, connectionId):
  for yourConnectionId in connectionIds:
    data = json.dumps({
      'Your ID': yourConnectionId,
      'Just connected': connectionId,
      'Number of connections': len(connectionIds),
      'Time': f'{time.time()} seconds',
      'List IDs': connectionIds,
    })
    apigw_management.post_to_connection(ConnectionId=connectionId, Data=data)
  
def disconnectHandler(apigw_management, connectionId):
  for yourConnectionId in connectionIds:
    data = json.dumps({
      'Your ID': yourConnectionId,
      'Just disconnected': connectionId,
      'Number of connections': len(connectionIds),
      'Time': f'{time.time()} seconds',
      'List IDs': connectionIds,
    })
  apigw_management.post_to_connection(ConnectionId=connectionId, Data=data)

def defaultHandler(apigw_management, connectionId):
  for yourConnectionId in connectionIds:
    data = json.dumps({
      'Your ID': yourConnectionId,
      'Default ID': connectionId,
      'Number of connections': len(connectionIds),
      'Time': f'{time.time()} seconds',
      'List IDs': connectionIds,
    })
  apigw_management.post_to_connection(ConnectionId=connectionId, Data=data)

def handler(event):
  connectionId = event.get('requestContext',{}).get('connectionId')
  if connectionId is None:
    return { 
      'statusCode': 400, 
      'body': 'bad request'
    }
  connectionIds.append(connectionId)
  
  eventType = event["requestContext"]["eventType"]
  domain_name = event.get('requestContext',{}).get('domainName')
  stage = event.get('requestContext',{}).get('stage')
  apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=F"https://{domain_name}/{stage}")
 
  if eventType == 'connect':
    connectHandler(apigw_management, connectionId)
  elif eventType == 'disconnect':
    disconnectHandler(apigw_management, connectionId)
  elif eventType == 'default':
    defaultHandler(apigw_management, connectionId)
  
  return
