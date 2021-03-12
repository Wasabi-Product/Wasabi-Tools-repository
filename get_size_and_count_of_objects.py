import sys
from boto3 import client, Session
from botocore.exceptions import ProfileNotFound, ClientError


def calculate_size(size, _size_table):
    count = 0
    while size // 1024 > 0:
        size = size / 1024
        count += 1
    return str(round(size, 2)) + ' ' + _size_table[count]


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
                            endpoint_url='https://s3.' + _region + '.wasabisys.com',
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
    size_table = {0: 'Bs', 1: 'KBs', 2: 'MBs', 3: 'GBs', 4: 'TBs', 5: 'PBs', 6: 'EBs'}
    access_key_id, secret_access_key = get_credentials()
    bucket = input("$ Please enter the name of the bucket: ").strip()
    region = region_selection()
    s3_client = create_connection_and_test(access_key_id, secret_access_key, region, bucket)

    s3_client.list_buckets()
    object_response_paginator = s3_client.get_paginator('list_object_versions')
    delete_marker_count = 0
    delete_marker_size = 0
    versioned_object_count = 0
    versioned_object_size = 0
    current_object_count = 0
    current_object_size = 0

    print("$ Calculating, please wait... this may take a while")
    for object_response_itr in object_response_paginator.paginate(Bucket=bucket):
        if 'DeleteMarkers' in object_response_itr:
            for delete_marker in object_response_itr['DeleteMarkers']:
                delete_marker_count += 1
                delete_marker_size += delete_marker['Size']

        if 'Versions' in object_response_itr:
            for version in object_response_itr['Versions']:
                if version['IsLatest'] is False:
                    versioned_object_count += 1
                    versioned_object_size += version['Size']
                elif version['IsLatest'] is True:
                    current_object_count += 1
                    current_object_size += version['Size']

    print("$ Total Delete marker: " + str(delete_marker_count))
    print("$ Number of Current objects: " + str(current_object_count))
    print("$ Current Objects size: ", calculate_size(current_object_size, size_table))
    print("$ Number of Versioned objects: " + str(versioned_object_count))
    print("$ Versioned Objects size: ", calculate_size(versioned_object_size, size_table))
    print("$ Total size: ", calculate_size(versioned_object_size + current_object_size, size_table))

    print("$ process completed successfully")
