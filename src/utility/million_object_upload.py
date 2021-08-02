# PYTHON script to create random files:

import boto3

from threading import Thread

session = boto3.Session(profile_name="ravi")
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key

s3 = boto3.resource('s3',
                    endpoint_url='https://s3.wasabisys.com',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)


def upload(myfile):
    f = open(myfile, "rb")
    s3.Bucket('ravi-voleti-bucket-test').put_object(Key=myfile, Body=f)
    f.close()
    return myfile


if __name__ == '__main__':
    filenames = []
    for i in range(33333):
        fname = "data/external_vars" + str(i) + ".yml"
        filenames.append(fname)
        f = open(fname, "w")
        f.write("Check Wasabi Status!!")
        f.close()
    t_i = 1

    for fname in filenames:
        t = Thread(target=upload, args=(fname,)).start()
        print(t_i)
        t_i = t_i + 1
