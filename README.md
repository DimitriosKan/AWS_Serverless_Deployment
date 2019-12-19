# AWS_Serverless_Deployment
Serverless web page deployment, hosted on an S3 Bucket. Built in Python, running boto3 calls to Lambda, S3 and other AWS services

## Command list
To run the deployment execute **_'python serv_apply.py'_**

To destroy the deployment, run **_'python serv_destroy.py'_**

#### What happens in the code?
_serv_apply.py_ file calls functions in the modules located in _sample_

Requred modules are split into the bucket (_s3_bucket.py_) and function (_lambda_function.py_)

Those contain the actual boto3 commands with the parameters necessary (sometimes these parameters are passed from the main module)

**_Locators_** 
* Structure here is to support and modularize the calls to boto3 services (_client_ or _resource_)
* Basically ... _ClientLocator_ sets up the structure of **_boto3.client_** (or **_boto3.resource_**). Then _...Client_ sets up the specific service you will be working with.

The Locators are called in the sample modules, with the *self._clien* __init__ call in the begining of a class.

Which when being executed in the main module is populated with the exact extension needed (_'s3', 'iam', 'lambda'_).


#### ! Disclaimer !: If using this on your own account, go through the lambda function file and edit the PolicyArn with your own.
