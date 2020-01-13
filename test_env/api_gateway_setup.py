import boto3
import func_arn_fetching

# client migrated to the locator and called in the apply script
client = boto3.client('apigateway')
lamb_cli = boto3.client('lambda')

aws_region = 'eu-west-2'
# get the lambda thing from somewhere (lambda module)
find_lamb = func_arn_fetching.find_lamb()

'''
All below goes to a new module that would be specifically for creating the certain trigger
Possible to apply the RestAPI creation to a different sub-module so it can be edited (if many setings are to be done) else it's unecessary)
'''
# restapi_response['id'] will give you the id to be used later
restapi_response = client.create_rest_api(
    name='test_rest_api',
    description='Good ol test rest api',
    endpointConfiguration={
        'types': ['REGIONAL']
        }
    )

restapi_id = restapi_response['id']

print (f"RestAPI ID: {restapi_id}")

# get the parentId of the rest api neede below
response = client.get_resources(restApiId=restapi_id)
for item in response['items']:
    if item['path'] == "/":
        parent_restapi = item['id']
        # print (parent_restapi)

# create the APIGateway
api_gateway_response = client.create_resource(
        restApiId=restapi_id,
        parentId=parent_restapi,
        pathPart='FancyLambdaFunction'
    )

print ('APIGateway created')

# get the childId of the rest api neede below
response = client.get_resources(restApiId=restapi_id)
for item in response['items']:
    if item['path'] == "/FancyLambdaFunction":
        child_restapi = item['id']
        # print (child_restapi)

# adds the get method (might wanna edit the location it's spaced aka. not '/' but '/*function*')
api_method_response = client.put_method(
        restApiId=restapi_id,
        resourceId=child_restapi,
        httpMethod='GET',
        authorizationType='NONE'
    )
print (f'Method Created: {api_method_response}')


# need to integrate, aka assign to lambda function (not sure if it needs to be after or before the create_deploy below)
# here I need to edit the uri, which is the arn to the lambda function ?
uri = f'arn:aws:apigateway:{aws_region}:lambda:path/2015-03-31/functions/{find_lamb}/invocations'

print (f'Constructed URI: {uri}')

integration_response = client.put_integration(
        restApiId=restapi_id,
        resourceId=child_restapi,
        httpMethod='GET',
        type='AWS',
        integrationHttpMethod='POST',
        uri=uri
    )
print (f'Integration sucessful: {integration_response}')

api_method_res = client.put_method_response(
        restApiId=restapi_id,
        resourceId=child_restapi,
        httpMethod='GET',
        statusCode='200',
        responseModels={'application/json': 'Empty'}
    )
print (f'Method response: {api_method_res}')

response_integration = client.put_integration_response(
        restApiId=restapi_id,
        resourceId=child_restapi,
        httpMethod='GET',
        statusCode='200',
        responseTemplates={'application/json': ''}
    )
print (f'Intergration response: {response_integration}')

# deploys the thing, almost like a stage, which should be performed so it is assigned to the function trigger
api_deploy_response = client.create_deployment(
        restApiId=restapi_id,
        stageName='prod'
    )
print (api_deploy_response)

# if you wish you can make the region and id modular *MAYBE ID NEEDS TO BE*
source_arn = f'arn:aws:execute-api:eu-west-2:071712497647:{restapi_id}/*/*/FancyLambdaFunction'

# hipothetical way of attaching api to lambda function trigger
lambda_perm = lamb_cli.add_permission(
        FunctionName='FancyLambdaFunction',
        StatementId='new-rando',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=source_arn
    )
print (lambda_perm)


api_id = input ("What's your ID: ")

delete_restapi = client.delete_rest_api(
        restApiId=f'{api_id}'
    )

