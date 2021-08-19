import os
import smtplib

import pandas as pd

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime

from boto3 import client
from botocore.exceptions import ClientError

import io


class IngestNotifier:
    """
    This class sends a notification about chia users or trial users.
    """
    ingest_data = None
    s3_client = None
    bucket = None

    def __init__(self):
        """
        Generic Constructor initializing variables used across this class.
        """
        self.bucket = 'trial-user-reports'
        return

    def connect_to_wasabi_bucket(self):
        """
        Connects to the Wasabi bucket.
        :return: None
        """
        wasabi_access_key = 'access-test2'
        wasabi_secret_key = 'secret-test2-6023CAF1C64667'
        region = 'https://s3.us-east-2.wasabisys.com'
        try:
            _s3_client = client('s3',
                                endpoint_url=region,
                                aws_access_key_id=wasabi_access_key,
                                aws_secret_access_key=wasabi_secret_key)

            try:
                _s3_client.head_bucket(Bucket=self.bucket)
            except ClientError:
                # The bucket does not exist or you have no access.
                raise Exception("$ bucket does not exist in the account please re-check the name and try again")

            self.s3_client = _s3_client

        except ClientError:
            raise Exception("$ Invalid Access and Secret keys")
        except Exception as e:
            raise e
        return

    def fetch_csv_data(self):
        # create a paginator with default settings.
        paginator = self.s3_client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=self.bucket)  # , Prefix=""
        latest = None
        for page in page_iterator:
            if "Contents" in page:
                latest2 = max(page['Contents'], key=lambda x: x['LastModified'])
                if latest is None or latest2['LastModified'] > latest['LastModified']:
                    latest = latest2

        # if os.path.exists('previous_key.txt'):
        #     file = open('previous_key.txt', 'r')
        #     previous_key = file.read().splitlines()[0]
        #     file.close()
        #
        #     if previous_key == latest['Key']:
        #         return

        file = open('previous_key.txt', 'w+')
        file.write(latest['Key'])
        file.close()

        try:
            return self.s3_client.get_object(Bucket=self.bucket, Key=latest['Key'])
        except Exception as e:
            raise e

    def get_previous_data(self):
        if os.path.exists('previous_key.txt'):
            file = open('previous_key.txt', 'r')
            previous_key = file.read().splitlines()[0]
            file.close()
            if previous_key == "":
                return
            try:
                return self.s3_client.get_object(Bucket=self.bucket, Key=previous_key)
            except Exception as e:
                raise e
        else:
            file = open('previous_key.txt', 'w')
            file.close()
        return

    def read_csv_data(self, data_path):
        """
        Read data from csv file or an excel file and convert it into a dataframe for processing.
        :param data_path: path to the file [will be replaced when reading from S3 Bucket]
        :return:
        """

        cols = ["AcctNum", "AcctName", "Account Deleted / Non-Deleted State", "Account Active / Inactive State",
                "Account Type", "Account Created Date", "ParentAcctNum", "Current Account Plan Valid From",
                "CurrentBillingPlan", "Is Paid Plan", "Data Uploaded Last Hour GiB", "Data Uploaded Last Hour TiB",
                "Current Raw Account Storage TiB", "Last Invoice Date", "Last Invoice Total", "Last Invoice Status",
                "Total Lifetime Settled Invoice Amount", "HubSpot First Name", "HubSpot Last Name", "HubSpot Email",
                "HubSpot Country", "HubSpot IP Country", "Atom Time UTC", "ISO 8601 Zulu Time UTC", "Unix Timestamp"]
        return pd.read_csv(data_path, usecols=cols)

    def send_slack_notification(self, ingest_data):
        """
        This function sends a slack notification to ingest-alerts channel.
        :return: None.
        """

        # initialize sender for gmail SMPT.
        sender = 'rvoleti@wasabi.com'

        # ingest notification email address
        receiver = 'ingest-alerts-aaaaekerxdy4cbvqphzl6gvepa@wasabitech.slack.com'

        # using app password due to 2FA.
        password = 'cnuwtdjpaekwkqhg'

        # set the body from the dataframe.
        body = f'<html>' \
               f'<body>' \
               f'<p>' \
               f'<h3>Top 10 users</h3>' \
               f'</p>' \
               f'{ingest_data.to_html(index=False)}' \
               f'</body>' \
               f'</html>'
        current_time = datetime.now()

        try:
            # initiate the SMTP library to send the email.
            msg = MIMEMultipart('alternative')
            msg.attach(MIMEText(body, 'html'))

            # set basic email attributes.
            msg['Subject'] = f'{current_time.strftime("%m/%d/%Y %H:%M:%S EST")} Top 10 ingest users'
            msg['From'] = sender
            msg['To'] = receiver

            # Send the message via our temp SMTP server.
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
            server.quit()
        except Exception as e:
            # log error.
            raise e
        return

    def filter_data(self, ingest_data):
        """
        This function is used to filter top 10 users.
        :return: update the existing dataframe.
        """

        # simple ingest filter example
        return ingest_data.head(10)

    def post_process_data(self, old_data, new_data):
        return new_data.merge(old_data, how='outer', indicator=True).query('_merge == "left_only"').drop('_merge', 1)

    def main(self):
        """
        This function is the main execution loop.
        1. Find and Read new data from S3 bucket.
        2. Read the csv file.
        3. Filter the data for specific columns
        4. Send a slack notification
        5. Send a CSP call to limit Trial / chia User
        :return: None.
        """
        # connect to S3 bucket.
        self.connect_to_wasabi_bucket()

        # get the latest csv file from the bucket
        new_data = self.fetch_csv_data()

        # Read the csv for new data.
        new_ingest_data = self.read_csv_data(io.BytesIO(new_data['Body'].read()))

        # Clean and filter data
        new_ingest_data = self.filter_data(ingest_data=new_ingest_data)

        # post process to find any changes between them
        # new_players_in_top_x = self.post_process_data(None, new_ingest_data)

        # send slack notification
        self.send_slack_notification(new_ingest_data)

        # do CSP stuff.
        # TODO: CSP stuff

        print("Notification sent successfully.")
        return


if __name__ == '__main__':
    IngestNotifier().main()
