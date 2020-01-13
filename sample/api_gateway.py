class Lambda_Arn:
    def __init__(self, client):
        self._client = client

    function_name = 'FancyLambdaFunction'

    def find_lamb():
        response = self._client.list_functions()
        for function in response['Functions']:
            if function['FunctionName'] == function_name:
                lamb_func_arn = function['FunctionArn']
                print (lamb_func_arn)
                return lamb_func_arn

class API_Gateway_Delete:
    def __init__(self, client):
        self._client = client

    def find_rest_api():
        response = self._client.get_rest_apis()

        for item in response['items']:
            rest_api_id = item['id']
            return rest_api_id

    def delete_rest_api():
        rest_api_id = find_rest_api()

        self._client.delete_rest_api(
            restApiId=rest_api_id
        )

        print (f'API {rest_api_id} deleted !')

class API_Gateway_Create:
    def __init__(self, client):
        self._client = client

    # Create the rest api itself and assign id to variable
    def create_rest_api(self):
        restapi_response = self._client.create_rest_api(
            name='test_rest_api',
            description='Good ol test rest api',
            endpointConfiguration={
                'types': ['REGIONAL']
                }
            )
        restapi_id = restapi_response['id']

        print (f"RestAPI ID: {restapi_id}")

        '''
        edit and integrate below VVV
        '''
        # get the parentId of the rest api neede below
        response = self._client.get_resources(restApiId=restapi_id)
        for item in response['items']:
            if item['path'] == "/":
                parent_restapi = item['id']
                # print (parent_restapi)

        # create the APIGateway
        api_gateway_response = self._client.create_resource(
                restApiId=restapi_id,
                parentId=parent_restapi,
                pathPart='FancyLambdaFunction'
            )

        print ('APIGateway created')

        # get the childId of the rest api neede below
        response = self._client.get_resources(restApiId=restapi_id)
        for item in response['items']:
            if item['path'] == "/FancyLambdaFunction":
                child_restapi = item['id']
                # print (child_restapi)

        # adds the get method
        api_method_response = self._client.put_method(
                restApiId=restapi_id,
                resourceId=child_restapi,
                httpMethod='GET',
                authorizationType='NONE'
            )
        print (f'Method Created: {api_method_response}')

        api_method_res = self._client.put_method_response(
                restApiId=restapi_id,
                resourceId=child_restapi,
                httpMethod='GET',
                statusCode='200',
                responseModels={'application/json': 'Empty'}
            )
        print (f'Method response: {api_method_res}')

        # need to integrate, aka assign to lambda function
        uri = f'arn:aws:apigateway:{aws_region}:lambda:path/2015-03-31/functions/{find_lamb}/invocations'

        print (f'Constructed URI: {uri}')

        integration_response = self._client.put_integration(
                restApiId=restapi_id,
                resourceId=child_restapi,
                httpMethod='GET',
                type='AWS',
                integrationHttpMethod='POST',
                uri=uri
            )
        print (f'Integration sucessful: {integration_response}')

        response_integration = self._client.put_integration_response(
                restApiId=restapi_id,
                resourceId=child_restapi,
                httpMethod='GET',
                statusCode='200',
                responseTemplates={'application/json': ''}
            )
        print (f'Intergration response: {response_integration}')

        # deploys the thing, almost like a stage, which should be performed so it is assigned to the function trigger
        api_deploy_response = self._client.create_deployment(
                restApiId=restapi_id,
                stageName='prod'
            )
        print (api_deploy_response)

        # if you wish you can make the region and id modular *MAYBE ID NEEDS TO BE*
        source_arn = f'arn:aws:execute-api:eu-west-2:071712497647:{restapi_id}/*/*/FancyLambdaFunction'

        # hipothetical way of attaching api to lambda function trigger
    def lambda_perm():
        lambda_perm = self._client.add_permission(
                FunctionName='FancyLambdaFunction',
                StatementId='new-rando',
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn=source_arn
            )
        print (lambda_perm)
   


'''

import boto3
import func_arn_fetching

# client migrated to the locator and called in the apply script
client = boto3.client('apigateway')
lamb_cli = boto3.client('lambda')

aws_region = 'eu-west-2'
# get the lambda thing from somewhere (lambda module)
find_lamb = func_arn_fetching.find_lamb()


All below goes to a new module that would be specifically for creating the certain trigger
Possible to apply the RestAPI creation to a different sub-module so it can be edited (if many setings are to be done) else it's unecessary)

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



api_id = input ("What's your ID: ")

delete_restapi = client.delete_rest_api(
        restApiId=f'{api_id}'
    )
'''
