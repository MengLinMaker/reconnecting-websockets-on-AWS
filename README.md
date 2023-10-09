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
