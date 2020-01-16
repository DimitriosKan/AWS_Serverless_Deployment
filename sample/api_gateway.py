class Lambda_Arn:
    def __init__(self, client):
        self._client = client

    # function_name = 'FancyLambdaFunction'

    def find_lamb(self, function_name):
        response = self._client.list_functions()
        for function in response['Functions']:
            if function['FunctionName'] == function_name:
                lamb_func_arn = function['FunctionArn']
                print (f'Lambda function ARN: {lamb_func_arn}')
                return lamb_func_arn

class API_Gateway_Delete:
    def __init__(self, client):
        self._client = client

    def find_rest_api(self):
        response = self._client.get_rest_apis()

        for item in response['items']:
            rest_api_id = item['id']
            print (rest_api_id)
            return rest_api_id

    def delete_rest_api(self, rest_api_id):
        # rest_api_id = find_rest_api()

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

        print (f"RestAPI created. ID: {restapi_id}")
        return restapi_id
    
    '''
    edit and integrate below VVV
    '''

    def get_parent_resource(self, restapi_id):
        # get the parentId of the rest api neede below
        response = self._client.get_resources(restApiId=restapi_id)
        for item in response['items']:
            if item['path'] == "/":
                parent_restapi = item['id']
                # print (parent_restapi)
                return parent_restapi

    def create_api_gateway(self, restapi_id, parent_restapi):
        # create the APIGateway
        api_gateway_response = self._client.create_resource(
                restApiId=restapi_id,
                parentId=parent_restapi,
                pathPart='FancyLambdaFunction'
            )

        print ('APIGateway created')

    def get_child_resource(self, restapi_id):
        # get the childId of the rest api neede below
        response = self._client.get_resources(restApiId=restapi_id)
        for item in response['items']:
            if item['path'] == "/FancyLambdaFunction":
                child_restapi = item['id']
                # print (child_restapi)
                return child_restapi

    def put_method(self, restapi_id, child_restapi):
        # adds the get method
        api_method_response = self._client.put_method(
                restApiId=restapi_id,
                resourceId=child_restapi,
                httpMethod='GET',
                authorizationType='NONE'
            )

        api_method_res = self._client.put_method_response(
                restApiId=restapi_id,
                resourceId=child_restapi,
                httpMethod='GET',
                statusCode='200',
                responseModels={'application/json': 'Empty'}
            )
        print (f'Get Method Created')

    def uri_construct(self, aws_region, find_lamb):
        # need to integrate, aka assign to lambda function
        uri = f'arn:aws:apigateway:{aws_region}:lambda:path/2015-03-31/functions/{find_lamb}/invocations'

        print (f'Constructed URI: {uri}')
        return uri

    def put_integration(self, restapi_id, child_restapi, uri):
        integration_response = self._client.put_integration(
                restApiId=restapi_id,
                resourceId=child_restapi,
                httpMethod='GET',
                type='AWS',
                integrationHttpMethod='POST',
                uri=uri
            )

        response_integration = self._client.put_integration_response(
                restApiId=restapi_id,
                resourceId=child_restapi,
                httpMethod='GET',
                statusCode='200',
                responseTemplates={'application/json': ''}
            )
        print (f'Get Integration Created')

    def create_deployment(self, restapi_id):
        # deploys the thing, almost like a stage, which should be performed so it is assigned to the function trigger
        api_deploy_response = self._client.create_deployment(
                restApiId=restapi_id,
                stageName='prod'
            )
        print ('Deploymnet created')

    def source_arn_construct(self, aws_region, restapi_id):
        # if you wish you can make the region and id modular *MAYBE ID NEEDS TO BE*
        source_arn = f'arn:aws:execute-api:{aws_region}:071712497647:{restapi_id}/*/*/FancyLambdaFunction'
        print (f'Constructed source ARN: {source_arn}')
        return source_arn

        # hipothetical way of attaching api to lambda function trigger
    def add_permission(self, source_arn):
        lambda_perm = self._client.add_permission(
                FunctionName='FancyLambdaFunction',
                StatementId='new-rando',
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn=source_arn
            )
        print ('Permissions added to function')


