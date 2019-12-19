import boto3

id_name = boto3.client('sts').get_caller_identity().get('Account')

print (id_name)
