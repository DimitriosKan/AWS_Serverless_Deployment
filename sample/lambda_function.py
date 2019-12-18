import json

class Lambda_Delete:
    def __init__(self, client):
        self._client = client


class Lambda_Create:
    def __init__(self, client):
        self._client = client

    def create_role(self):
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
            RoleName='LambdaRole',
            AssumeRolePolicyDocument=json.dumps(basic_role)
        )


    def create_policy(self):
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
            PolicyName='LambdaPolicy',
            PolicyDocument=json.dumps(basic_policy)
        )

    def attach_policy(self):
        print ('Attaching Policy to Role ...')
        # attaching policy to role
        self._client.attach_role_policy(
            RoleName='LambdaRole',
            PolicyArn='arn:aws:iam::071712497647:policy/LambdaPolicy'
        )


    def create_lambda(self, zipped_code):
        print ('Creating Lambda function ...')
        self._client.create_function(
            FunctionName='FancyLambdaFunction',
            Runtime='python3.6',
            Role='arn:aws:iam::071712497647:role/LambdaRole',
            Handler='function_test_hello.lambda_handler',
            Code=dict(ZipFile=zipped_code)
        )

    def invoke_lambda(self):
        print ('Invoking Lambda ...')
        response_from_lambda = self._client.invoke(
            FunctionName='FancyLambdaFunction',
        )

        print (response_from_lambda)
