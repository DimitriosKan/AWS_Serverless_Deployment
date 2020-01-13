import boto3

client = boto3.client('lambda')

function_name = 'FancyLambdaFunction'

def find_lamb():
    response = client.list_functions()
    for function in response['Functions']:
        if function['FunctionName'] == function_name:
            lamb_func_arn = function['FunctionArn']
            print (lamb_func_arn)
            return lamb_func_arn

if __name__ == "__main__":
    find_lamb()
