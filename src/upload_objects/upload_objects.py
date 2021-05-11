import boto3
import os

if __name__ == '__main__':
    bucket = 'bucket-name'
    profile_name = 'profile-name'
    endpoint = 'https://s3.wasabisys.com'  # please refer to for other endpoints.
    local_file_path = 'data-file-path'

    # Comment this section out if you want to specify keys directly
    # --------
    session = boto3.Session(profile_name=profile_name)
    aws_access_key_id = session.get_credentials().access_key
    aws_secret_access_key = session.get_credentials().secret_key
    # --------

    # connect to boto3 as a resource
    s3 = boto3.resource(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)

    # upload objects in the file directory.
    for file_name in os.listdir(local_file_path):
        body = open(local_file_path + file_name, 'rb')
        s3.Bucket(bucket).put_object(Key=file_name, Body=body)
