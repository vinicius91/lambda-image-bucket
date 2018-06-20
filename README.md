# IMAGE BUCKET

This is an AWS Lambda implementation with Serverless framework

## Functions

### extractMetadata

This function will get the metadata from a image uploaded to the AWS S3 and will save in a DynamoDB objects the metadata extracted

Props: s3objectkey, bucket, size, width, size

### getMetadata

This function will expose an AWS API Gateway GET endpoint that will fetch the metadata when provided with th s3objectkey

Ps.: To call this method you will have to escape the '/' with the default URL escape code '%2F'

## Deploy and Setup

To deploy this project you will need to have Docker instaled in your machine and the Serverless-Cli

- Step 1 - Install the Python Requirements Plugin
  <code>sls plugin install --name serverless-python-requirements</code>

- Step 2 - Deploy the Function
  <code>sls deploy -v</code>

Ps.: You might also need to setup your Serverless Profile, in this example I used serverless-admin as a default profile, you can get more info in how to setup your serverless cli in its docs page.
https://serverless.com/framework/docs/

## Created By

Vinicius Rodrigues
https://www.viniro.me
