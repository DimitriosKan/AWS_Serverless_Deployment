from sample.s3_bucket import S3_Create
from locators.client_locator import S3Client
import os

s3_client = S3Client().get_client()

s3_cli = S3_Create(s3_client)

bucket_name = 'fresh-bucket-but-boto3-2020'

def create_bucket():
    s3_cli.create_bucket(bucket_name)
    print (f'Bucket {bucket_name} was created')
    # print (bucket_creation_response['ResponseMetadata']['Location'])

def create_bucket_policy():
    bucket_policy_response = s3_cli.create_bucket_policy(bucket_name)
    print (f'Policy for {bucket_name} has been created')
    print (bucket_policy_response)
'''
def encypr ...
'''


def upload_files():
    upload_dir = os.path.dirname(os.path.abspath(__file__)) + '/docs/'
    print (upload_dir)

    docfiles = [f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f))]
    print (docfiles)

    for file_name in docfiles:
        file_path = f'{upload_dir}{file_name}'
        s3_cli.upload_files(file_path, bucket_name, file_name)
        print (f'File "{file_name}" from "{file_path}" was uploaded to {bucket_name}')

def deploy_webpage():
    index_file = os.path.dirname(os.path.abspath(__file__)) + '/docs/index.html'
    print (index_file)
    error_file = os.path.dirname(__file__) + 'docs/error.html'
    print (error_file)

    s3_cli.host_website(index_file, error_file, bucket_name)

    print (f'Go to "{bucket_name}.s3-website.eu-west-2.amazonaws.com" to check out your website')


if __name__ == "__main__":
    create_bucket()
    create_bucket_policy()
    
    #upload_files()
    deploy_webpage()
