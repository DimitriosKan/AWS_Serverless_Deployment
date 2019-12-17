import boto3
import json

iam = boto3.client('iam')
lamb = boto3.client('lambda')

'''
todo:
    - check if you can assign the iam user dynamically in the policy parts
    - if you can zip up files from python (make it so you zip up the lambda function file so it allows modularizing it)
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

# *** LAMBDA FUNCTION CREATION ***

lamb.create_function(
    FunctionName='FancyLambdaFunction',
    Runtime='python3.6',
    Role='arn:aws:iam::071712497647:role/LambdaRole',
    Handler='*name-of-method-in-code*',
    Code={
        'ZipFile': b'*zip_file_name*'
    }
)
