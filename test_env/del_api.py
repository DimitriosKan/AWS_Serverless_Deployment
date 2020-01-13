import boto3

client = boto3.client('apigateway')

def find_rest_api():
    response = client.get_rest_apis()

    for item in response['items']:
        rest_api_id = item['id']
        return rest_api_id

def delete_rest_api():
    rest_api_id = find_rest_api()

    client.delete_rest_api(
        restApiId=rest_api_id
    )
    print (f'API {rest_api_id} deleted !')

if __name__ == "__main__":
    delete_rest_api()
