# delete role
# delete policy
# delete lambda
import boto3

lamb = boto3.client('lambda')
iam = boto3.client('iam')

role_name = 'LambdaRole'
policy_arn = 'arn:aws:iam::071712497647:policy/LambdaPolicy'

try:
    lamb.delete_function(
        FunctionName='FancyLambdaFunction'
    )
    print ('Lambda function deleted')
except:
    print ('Hm ...')

iam.detach_role_policy(
    RoleName=role_name,
    PolicyArn=policy_arn
)
print ('Role dettached from policy')

iam.delete_role(
    RoleName=role_name
)
print ('Role deleted')

iam.delete_policy(
    PolicyArn=policy_arn
)
print ('Policy deleted')
