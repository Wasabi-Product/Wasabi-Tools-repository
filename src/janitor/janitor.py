#  Copyright (c) 2021. This script is available as fair use for users. This script can be used freely with
#  Wasabi Technologies.inc. Distributed by the support team at wasabi.

from boto3 import client, Session


def delete_user(_iam_client):
    users_paginator = _iam_client.get_paginator('list_users')
    access_key_paginator = iam_client.get_paginator('list_access_keys')
    users_pagination_object = []
    all_users = []

    for users_response in users_paginator.paginate():
        users_pagination_object.append(users_response['Users'])

    for user_object in users_pagination_object:
        for u in user_object:
            all_users.append(u['UserName'])

    for user in all_users:
        user_name = user
        print("$ Deleting: " + user_name)

        # 1. Delete login profile
        try:
            response = _iam_client.delete_login_profile(UserName=user_name)
        except _iam_client.exceptions.NoSuchEntityException:
            print("$ no login profile to delete")
        except Exception as e:
            raise e

        # 2. delete user access keys.
        for response in access_key_paginator.paginate(UserName=user_name):
            if len(response['AccessKeyMetadata']) > 0:
                for keys in response['AccessKeyMetadata']:
                    # 2.a deactivate key
                    iam_client.update_access_key(AccessKeyId=keys['AccessKeyId'], Status='Inactive',
                                                 UserName=user_name)
                    # 2.b delete key
                    iam_client.delete_access_key(AccessKeyId=keys['AccessKeyId'], UserName=user_name)

        # 3. delete user inline policies
        response = _iam_client.list_user_policies(UserName=user_name)
        if len(response['PolicyNames']) > 0:
            for policy in response['PolicyNames']:
                _iam_client.delete_user_policy(UserName=user_name, PolicyName=policy)

        # 4. delete user managed policies
        response = _iam_client.list_attached_user_policies(UserName=user_name)
        if len(response['AttachedPolicies']) > 0:
            for managed_policy in response['AttachedPolicies']:
                _iam_client.detach_user_policy(UserName=user_name, PolicyArn=managed_policy['PolicyArn'])

        # 5. Detach groups
        response = _iam_client.list_groups_for_user(UserName=user_name)
        if len(response['Groups']) > 0:
            for group in response['Groups']:
                _iam_client.remove_user_from_group(GroupName=group['GroupName'], UserName=user_name)

        # 6. Delete Users
        _iam_client.delete_user(UserName=user_name)

    return


def delete_policy(_iam_client):
    # 1. list all policies
    policies = _iam_client.list_policies(Scope='Local', OnlyAttached=False)['Policies']

    for policy in policies:
        # 2. List entities for each policy and detach them
        policy_arn = policy['Arn']
        response = _iam_client.list_entities_for_policy(PolicyArn=policy_arn)

        # 3. Detach all policies
        if 'PolicyGroups' in response:
            for policyGroups in response['PolicyGroups']:
                _iam_client.detach_group_policy(GroupName=policyGroups['GroupName'], PolicyArn=policy_arn)
        if 'PolicyUsers' in response:
            for policyUsers in response['PolicyUsers']:
                _iam_client.detach_user_policy(UserName=policyUsers['UserName'], PolicyArn=policy_arn)
        if 'PolicyRoles' in response:
            for policyRoles in response['PolicyRoles']:
                _iam_client.detach_role_policy(RoleName=policyRoles['RoleName'], PolicyArn=policy_arn)

        # 4. List all policy versions
        response = _iam_client.list_policy_versions(PolicyArn=policy_arn)

        # 5. Delete policy versions
        for version in response['Versions']:
            if not version['IsDefaultVersion']:
                _iam_client.delete_policy_version(PolicyArn=policy_arn, VersionId=version['VersionId'])

        # 6. Delete policies
        _iam_client.delete_policy(PolicyArn=policy['Arn'])

    return


def delete_group(_iam_client):
    # 1. list all groups
    response = _iam_client.list_groups()

    # 2. list all group policies
    for group in response['Groups']:
        group_name = group['GroupName']

        print("$ Deleting: " + group_name)

        # Delete group
        _iam_client.delete_group(GroupName=group_name)

    return


def delete_buckets(_s3_client):
    # 1. list all buckets.
    buckets = _s3_client.list_buckets()

    # 2. for each bucket delete all objects and delete markers
    object_response_paginator = _s3_client.get_paginator('list_object_versions')
    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']

        # 2.a Delete all delete markers and objects
        operation_parameters = {'Bucket': bucket_name}

        # initialize basic variables for in memory storage.
        delete_list = []

        print("$ Calculating, please wait... this may take a while")
        for object_response_itr in object_response_paginator.paginate(**operation_parameters):
            if 'DeleteMarkers' in object_response_itr:
                for delete_marker in object_response_itr['DeleteMarkers']:
                    delete_list.append({'Key': delete_marker['Key'], 'VersionId': delete_marker['VersionId']})

            if 'Versions' in object_response_itr:
                for version in object_response_itr['Versions']:
                    # add any key to delete list
                    delete_list.append({'Key': version['Key'], 'VersionId': version['VersionId']})

        print("$ Deleting objects and Delete Markers")
        for i in range(0, len(delete_list), 1000):
            _s3_client.delete_objects(
                Bucket=bucket_name,
                Delete={
                    'Objects': delete_list[i:i + 1000],
                    'Quiet': True
                }
            )

        # 2.b Delete bucket
        _s3_client.delete_bucket(Bucket=bucket_name)
    return


if __name__ == '__main__':
    session = Session(profile_name="profile-name")
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    s3_client = client('s3',
                       endpoint_url='https://s3.wasabisys.com',
                       aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key)

    iam_client = client('iam',
                        endpoint_url='https://iam.wasabisys.com',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name='us-east-1')

    print("*" * 10)
    print("$ Deleting users")
    print("*" * 10)
    delete_user(iam_client)

    print("*" * 10)
    print("$ Deleting policies")
    print("*" * 10)
    delete_policy(iam_client)

    print("*" * 10)
    print("$ Deleting groups")
    print("*" * 10)
    delete_group(iam_client)

    print("*" * 10)
    print("$ Deleting buckets")
    print("*" * 10)
    delete_buckets(s3_client)
