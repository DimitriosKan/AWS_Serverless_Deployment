import boto3

client = boto3.client('apigateway')

response = client.get_resources(restApiId='js3gmpzly9')
for item in response['items']:
    if item['path'] == "/FancyLambdaFunction":
        parent_restapi = item['id']
        print (parent_restapi)
