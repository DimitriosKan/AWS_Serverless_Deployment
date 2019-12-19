from sample.s3_bucket import S3_Delete
from sample.lambda_function import Lambda_Delete, User_Check, Arn_Check
from locators.client_locator import S3Client, IAMClient, LambdaClient, STSClient
from locators.resource_locator import S3Resource

s3_resource = S3Resource().get_resource()
iam_client = IAMClient().get_client()
lambda_client = LambdaClient().get_client()
sts_client = STSClient().get_client()

s3_res = S3_Delete(s3_resource)
iam_cli = Lambda_Delete(iam_client)
lamb_cli = Lambda_Delete(lambda_client)
sts_cli = User_Check(sts_client)

function_name = 'FancyLambdaFunction'
policy_name = 'LambdaPolicy'
role_name = 'LambdaRole'

# fetch the list of buckets still up
def fetch_buckets():
    return s3_res.fetch_buckets()

def empty_and_destroy_buckets():
    # if length of list is above 0 run the 'for' loop
    # iterate through list and run commands on individual instances

    proj_bucket = 'fresh-bucket-but-boto3-2020'

    print ('The buckets I could find are:')
    for bckt in fetch_buckets():
        print (bckt)
    print ('')

    if proj_bucket in fetch_buckets():
        print (f'Destroying "{proj_bucket}" bucket ...')
        s3_res.delete_files(proj_bucket)
        print (f'Bucket "{proj_bucket}" has been emptied')
        s3_res.destroy_bucket(proj_bucket)
        print (f'{proj_bucket} was destroyed.')
    # if it is not, run confirmation of no instances in list
    else:
        print ("We are on the 'else' statement ... Probably there's nothing to clean up")
        print ("Yay!")

def destroy_lambda():
    try:
        lamb_cli.delete_function(function_name)
    except:
        print ('Hm ...')

sts_response = sts_cli.get_caller()

def destroy_iams():
    zeclass = Arn_Check()
    policy_arn = zeclass.get_arn(sts_response, policy_name)

    print ('Destroying IAM Policy and Role ...')
    iam_cli.detach_policy(role_name, policy_arn)
    iam_cli.delete_role(role_name)
    iam_cli.delete_policy(policy_arn)


if __name__ == "__main__":
    fetch_buckets()
    empty_and_destroy_buckets()

    destroy_lambda()
    destroy_iams()
