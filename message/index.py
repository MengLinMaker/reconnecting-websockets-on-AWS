import boto3

dynamodbTable = boto3.resource('dynamodb').Table('WebSocket-Test-Table')

def handler(event, context):
  dynamodbNewImage = event['Records'][0]['dynamodb']['NewImage']
  endpoint_url = dynamodbNewImage['websocketURL']['S']
  currentID = dynamodbNewImage['currentID']['S']
  apigateway = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)
  try:
    message = dynamodbNewImage['message']['S']
    apigateway.post_to_connection(ConnectionId=currentID, Data=message)
  except: pass
