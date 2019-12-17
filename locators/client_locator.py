import boto3

# internal class setting up the base of the client allocation
class ClientLocator:
    def __init__(self, client):
        self._client = boto3.client(client, region_name='eu-west-2')
    def get_client(self):
        return self._client

# allows you to specify which client setup to use (the 's3' at the end)
class S3Client(ClientLocator):
    def __init__(self):
        super().__init__('s3')
