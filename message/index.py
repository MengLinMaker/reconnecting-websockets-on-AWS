import json
import boto3

dynamodbTable = boto3.resource('dynamodb').Table('WebSocket-Test-Table')

# Websocket message client from dynamodb stream
def handler(event, context):
  try:
    dynamodbNewImage = event['Records'][0]['dynamodb']['NewImage']
    endpoint_url = dynamodbNewImage['socketUrl']['S']
    currentId = dynamodbNewImage['currentId']['S']
    message = dynamodbNewImage['message']['S']

    apigateway = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)
    apigateway.post_to_connection(ConnectionId=currentId, Data=json.dumps({'message': message}))
  except: pass
