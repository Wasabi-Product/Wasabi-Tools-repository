import boto3

# Use the following code to connect using Wasabi profile from .aws/credentials file
session = boto3.Session(profile_name="wasabi")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key

s3 = boto3.client('s3',
                  endpoint_url='https://s3.wasabisys.com',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)

# Use the following code to connect directly via raw credentials.
# s3 = boto3.client('s3',
#                   endpoint_url='https://s3.wasabisys.com',
#                   aws_access_key_id="<insert-access-key>",
#                   aws_secret_access_key="<insert-secret-key>")

bucket_name = "<bucket-name>"
key_name = "<key-name>"

s3.delete_object(Bucket=bucket_name, Key=key_name)
