import json

class User_Check:
    def __init__(self, client):
        self._client = client

    def get_caller(self):
        sts_response = self._client.get_caller_identity().get('Account')
        #print (sts_response)
        return sts_response

class Arn_Check:
    def get_arn(self, sts_response, policy_name):
        policy_arn = f'arn:aws:iam::{sts_response}:policy/{policy_name}'
        #print (policy_arn)
        return policy_arn

class Lambda_Delete:
    def __init__(self, client):
        self._client = client

    def delete_function(self, function_name):
        print ('Deleting Lambda Function ...')
        self._client.delete_function(
            FunctionName=function_name
        )

    def detach_policy(self, role_name, policy_arn):
        print ('Detaching Policy ...')
        self._client.detach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )

    def delete_role(self, role_name):
        print ('Deleting Role ...')
        self._client.delete_role(
            RoleName=role_name
        )

    def delete_policy(self, policy_arn):
        print ('Deleting Policy ...')
        self._client.delete_policy(
            PolicyArn=policy_arn
        )

class Lambda_Create:
    def __init__(self, client):
        self._client = client

    def create_role(self, role_name):
        # role json model
        basic_role = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        print ('Creating IAM Role ...')
        # role creation for function
        self._client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(basic_role)
        )


    def create_policy(self, policy_name):
        # policy json model
        basic_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Stmt1508266078275",
                    "Action": [
                        "logs:PutLogEvents",
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream"
                    ],
                    "Effect": "Allow",
                    "Resource": "*"
                }
            ]
        }

        print ('Creating IAM Policy ...')
        # policy creation for function
        self._client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(basic_policy)
        )

    def attach_policy(self, role_name, policy_arn):
        print ('Attaching Policy to Role ...')
        # attaching policy to role
        self._client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )


    def create_lambda(self, zipped_code, function_name, sts_response):
        print ('Creating Lambda function ...')
        self._client.create_function(
            FunctionName=function_name,
            Runtime='python3.6',
            Role=f'arn:aws:iam::{sts_response}:role/LambdaRole',
            Handler='function_test_hello.lambda_handler',
            Code=dict(ZipFile=zipped_code)
        )

    def invoke_lambda(self, function_name):
        print ('Invoking Lambda ...')
        response_from_lambda = self._client.invoke(
            FunctionName=function_name,
        )

        print (response_from_lambda)
