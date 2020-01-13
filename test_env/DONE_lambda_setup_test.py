import boto3
import json
import os
from zipfile import ZipFile
import time
import sys

iam = boto3.client('iam')
lamb = boto3.client('lambda')

'''
todo:
    - check if you can assign the iam user dynamically in the policy parts
  V  if you can zip up files from python (make it so you zip up the lambda function file so it allows modularizing it)
'''

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

# role creation for function
iam.create_role(
    RoleName='LambdaRole',
    AssumeRolePolicyDocument=json.dumps(basic_role)
)

# policy creation for function
iam.create_policy(
    PolicyName='LambdaPolicy',
    PolicyDocument=json.dumps(basic_policy)
)

# attaching policy to role
iam.attach_role_policy(
    RoleName='LambdaRole',
    PolicyArn='arn:aws:iam::071712497647:policy/LambdaPolicy'
)

print ('Waiting ...\n')
x = True
while x:
    sys.stdout.write('[')
    sys.stdout.flush()
    for i in range(30,0,-1):
        sys.stdout.write(f'$')
        sys.stdout.flush()
        time.sleep(1)
    x = False
    print (']')
print ('\n Creating Lambda Function ...')

# *** LAMBDA FUNCTION CREATION ***

# zip up that file
zipObj = ZipFile('function_test_hello.zip', 'w')
zipObj.write('function_test_hello.py')
zipObj.close()

# open file before sending it over
with open('function_test_hello.zip', 'rb') as f:
    zipped_code = f.read()

lamb.create_function(
    FunctionName='FancyLambdaFunction',
    Runtime='python3.6',
    Role='arn:aws:iam::071712497647:role/LambdaRole',
    Handler='function_test_hello.lambda_handler',
    Code=dict(ZipFile=zipped_code)
)

response_from_lambda = lamb.invoke(
    FunctionName='FancyLambdaFunction',
)

print (response_from_lambda)

# close file

# remove the zip
os.remove('function_test_hello.zip')
