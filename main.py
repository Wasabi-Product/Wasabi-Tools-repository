import sys
from boto3 import client, Session
from botocore.exceptions import ProfileNotFound, ClientError


def get_credentials():
    credentials_verified = False
    aws_access_key_id = None
    aws_secret_access_key = None
    while not credentials_verified:
        choice = input("$ Press 1 and enter to select existing profile\n"
                       "$ Press 2 and enter to enter Access Key and Secret Key\n"
                       "$ Press 3 to exit: ")
        if choice.strip() == "1":
            aws_access_key_id, aws_secret_access_key = select_profile()
            if aws_access_key_id is not None and aws_secret_access_key is not None:
                credentials_verified = True
        elif choice.strip() == "2":
            aws_access_key_id = input("$ AWS access key").strip()
            aws_secret_access_key = input("$ AWS secret access key").strip()
            credentials_verified = True
        elif choice.strip() == "3":
            sys.exit(0)
        else:
            print("Invalid choice please try again")
    return aws_access_key_id, aws_secret_access_key


def select_profile():
    profile_selected = False
    while not profile_selected:
        try:
            profiles = Session().available_profiles
            if len(profiles) == 0:
                return None, None
            print("$ Available Profiles: ", profiles)
        except Exception as e:
            print(e)
            return None, None
        profile_name = input("$ Profile name: ").strip().lower()
        try:
            session = Session(profile_name=profile_name)
            credentials = session.get_credentials()
            aws_access_key_id = credentials.access_key
            aws_secret_access_key = credentials.secret_key
            profile_selected = True
            return aws_access_key_id, aws_secret_access_key
        except ProfileNotFound:
            print("$ Invalid profile. Please Try again.")
        except Exception as e:
            raise e


def region_selection():
    dic = {"1": "us-east-1",
           "2": "us-east-2",
           "3": "us-central-1",
           "4": "eu-central-1",
           "5": "us-west-1"
           }
    region_selected = False
    _region = ""
    while not region_selected:
        choice = input("$ Select region of the bucket:\n"
                       "$ 1: us-east-1\n"
                       "$ 2: us-east-2\n"
                       "$ 3: us-central-1\n"
                       "$ 4: eu-central-1\n"
                       "$ 5: us-west-1\n")
        if str(choice) in dic:
            _region = dic[str(choice)]
            region_selected = True
        else:
            print("$ Invalid selection please try again")
    return _region


def create_connection_and_test(aws_access_key_id: str, aws_secret_access_key: str, _region, _bucket):
    try:
        _s3_client = client('s3',
                            endpoint_url='https://s3.wasabibeta.com',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)

        # Test credentials are working
        _s3_client.list_buckets()

        try:
            _s3_client.head_bucket(Bucket=bucket)
        except ClientError:
            # The bucket does not exist or you have no access.
            raise Exception("$ bucket does not exist in the account please re-check the name and try again: ")

        return _s3_client

    except ClientError:
        print("Invalid Access and Secret keys")
    except Exception as e:
        raise e
    # cannot reach here
    return None


if __name__ == '__main__':
    access_key_id, secret_access_key = get_credentials()
    bucket = input("$ Please enter the name of the bucket: ").strip()
    # region = region_selection()
    region = ""
    s3_client = create_connection_and_test(access_key_id, secret_access_key, region, bucket)

    object_response_paginator = s3_client.get_paginator('list_object_versions')
    delete_marker_list = []
    version_list = []

    print("$ paginating and adding versions to array")
    for object_response_itr in object_response_paginator.paginate(Bucket=bucket):
        if 'DeleteMarkers' in object_response_itr:
            for delete_marker in object_response_itr['DeleteMarkers']:
                delete_marker_list.append({'Key': delete_marker['Key'], 'VersionId': delete_marker['VersionId']})

        if 'Versions' in object_response_itr:
            for version in object_response_itr['Versions']:
                if version['IsLatest'] is False:
                    version_list.append({'Key': version['Key'], 'VersionId': version['VersionId']})
    print("$ pagination complete")
    print("$ starting deletes now...")
    print("$ removing delete markers")
    for i in range(0, len(delete_marker_list), 1000):
        response = s3_client.delete_objects(
            Bucket=bucket,
            Delete={
                'Objects': delete_marker_list[i:i + 1000],
                'Quiet': True
            }
        )
        print(response)
    print("$ removing old versioned objects")
    for i in range(0, len(version_list), 1000):
        response = s3_client.delete_objects(
            Bucket=bucket,
            Delete={
                'Objects': version_list[i:i + 1000],
                'Quiet': True
            }
        )
        print(response)

    print("$ process completed successfully")
