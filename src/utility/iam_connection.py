import boto3

# Use the following code to connect using Wasabi profile from .aws/credentials file
# for IAM us-east-1 is default endpoint.
session = boto3.Session(profile_name="wasabi")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key

iam = boto3.client('iam',
                   endpoint_url='https://iam.wasabisys.com',
                   aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key,
                   region_name='us-east-1')

# Use the following code to connect directly via raw credentials.
# for IAM us-east-1 is default endpoint.
# iam = boto3.client('iam',
#                    endpoint_url='https://iam.wasabisys.com',
#                    aws_access_key_id="<insert-access-key>",
#                    aws_secret_access_key="<insert-secret-key>",
#                    region_name='us-east-1')
