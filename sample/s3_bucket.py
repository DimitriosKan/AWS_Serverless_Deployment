import json

class S3_Delete:
    def __init__(self, resource):
        self._resource = resource

    def fetch_buckets(self):
        response = self._resource.meta.client.list_buckets()
        up_buckets = [bucket['Name'] for bucket in response['Buckets']]
        return up_buckets

    def delete_files(self, up_buckets):
        print ('Empyting bucket ...')
        bucket = self._resource.Bucket(up_buckets)
        bucket.object_versions.delete()

    def destroy_bucket(self, up_buckets):
        print ('Destroying bucket ...')
        bucket = self._resource.Bucket(up_buckets)
        bucket.delete()

class S3_Create:
    # think this is the init for the client(or resource)calls when dealing with boto3
    # it is referenced by the main file, when pushing the locator
    def __init__(self, client):
        self._client = client
   
    def create_bucket(self, bucket_name):
        print ('Creating S3 bucket ...')
        return self._client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-west-2'
            }
        )
    
    def create_bucket_policy(self, bucket_name):
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AddPerm",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": [
                        "s3:DeleteObject",
                        "s3:GetObject",
                        "s3:PutObject"
                    ],
                    "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                }
            ]
        }

        policy_string = json.dumps(bucket_policy)

        print ('Creating bucket policy ...')
        return self._client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=policy_string
        )

    def create_encryption(self, bucket_name):
        return self._client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [{
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }]
            }
        )

    def upload_files(self, file_path, bucket_name, file_name):
        print (f'Uploading {file_name} ...')
        return self._client.upload_file(file_path, bucket_name, file_name)

    def host_website (self, index_file, error_file, bucket_name):
        print ('Getting website set up ...')

        website_config = {
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'}
        }

        self._client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration=website_config
        )

        self._client.put_object(
            Bucket=bucket_name,
            ACL='public-read',
            Key='index.html',
            Body=open(index_file).read(),
            ContentType='text/html'
        )

        self._client.put_object(
            Bucket=bucket_name,
            ACL='public-read',
            Key='error.html',
            Body=open(error_file).read(),
            ContentType='text/html'
        )
