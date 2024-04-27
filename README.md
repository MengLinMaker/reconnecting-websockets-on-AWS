# Reconnecting websockets on AWS
In this example, we set up reconnecting websocket solution with API Gateway, DynamoDB and Lambda using Serverless Framework written in Python.

Read [this blogpost](https://medium.com/@menglinmaker/reconnecting-websockets-on-aws-106a9e8da4b8) for a more in depth explaination of how this works.

## Pre-requisites
In order to deploy the application, you will need the following:

API credentials for AWS, with Administrator permissions (for simplicity, not recommended in production).
Node.js and `npm` / `pnpm` / `yarn` installed locally.

## Deploying the project
1. Clone the repository
2. Install node dependencies: `npm i`
3. Deploy backend: `sls deploy --verbose`
4. Deploy frontend: `npm run dev`

## So how does this work?
Persistent WebSockets generally require:
* A shared ID between both server and client - Eg: Session Key or other Auth info - **"socketID" in our case.**
* A Key Value with Pub Sub capability - Eg: Redis - **DynamoDB in our case**

Connecition workflow:
1. First send an empty **"socketID"** via the WebSocket to indicate that no persistent connections exist - via **"open"** route.
2. In new persistent connections **"socketID"** is defined by the server.
3. On every connection, a new **"connectionId"** is created by API Gateway and saved to DynamoDB with associated **"socketID"**.
4. The DynamoDB stream allows **"socketID"** to proxy "connectionId". Any updates will trigger a lambda to send updated messages to the client via **"connectionId"**.

Note: Route is an API Gateway specific concept that needs to be configured.
