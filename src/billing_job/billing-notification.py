"""
NOTE this script assumes that you are using gmail as your smtp server if not please configure it accordingly.
"""

import datetime
from email.message import EmailMessage

import requests
import smtplib


def calculate_size(size, _size_table):
    """
    This function dynamically calculates the right base unit symbol for size of the object.
    :param size: integer to be dynamically calculated.
    :param _size_table: dictionary of size in Bytes. Created in wasabi-automation.
    :return: string of converted size.
    """
    count = 0
    while size // 1024 > 0:
        size = size / 1024
        count += 1
    return str(round(size, 2)) + ' ' + _size_table[count]


if __name__ == '__main__':
    # Keys for accessing billing data.
    wasabi_access_key = 'Wasabi-Access-Key'
    wasabi_secret_key = 'Wasabi-Secret-Key'
    gmail_sender = 'sender@xyz.com'
    receiver = 'receiver@xyz.com'
    # If you have 2FA then please enable application passwords for separate instance login.
    gmail_password = 'sender-Password'

    # Generate a table for SI units symbol table.
    size_table = {0: 'Bs', 1: 'KBs', 2: 'MBs', 3: 'GBs', 4: 'TBs', 5: 'PBs', 6: 'EBs'}

    # request for the billing api
    try:
        response = requests.get("https://billing.wasabisys.com/utilization/bucket/",
                                headers={"Authorization": f'{wasabi_access_key}:{wasabi_secret_key}'})
    except Exception as e:
        raise e

    # get json data for billing
    json_data = response.json()

    # initialize a dict for adding up numbers
    result = {'PaddedStorageSizeBytes': 0,
              'NumBillableObjects': 0,
              'DeletedStorageSizeBytes': 0,
              'NumBillableDeletedObjects': 0
              }

    # get the initial time and check date only for this day.
    initial_time = datetime.datetime.strptime(json_data[0]['StartTime'], '%Y-%m-%dT%H:%M:%SZ')

    # for each bucket add the the data to the dict
    for bucket in json_data:
        # check the time from the last day.
        time = datetime.datetime.strptime(bucket['StartTime'], '%Y-%m-%dT%H:%M:%SZ')
        # summing logic.
        if time.date() == initial_time.date():
            result['PaddedStorageSizeBytes'] += bucket['PaddedStorageSizeBytes']
            result['DeletedStorageSizeBytes'] += bucket['DeletedStorageSizeBytes']
            result['NumBillableObjects'] += bucket['NumBillableObjects']
            result['NumBillableDeletedObjects'] += bucket['NumBillableDeletedObjects']

    body = f"Billing Summary for {initial_time.date()}" + "\n" \
           + 'Active storage: ' + calculate_size(result['PaddedStorageSizeBytes'], size_table) + "\n" \
           + 'Deleted storage: ' + calculate_size(result['DeletedStorageSizeBytes'], size_table) + "\n" \
           + 'Total Active objects: ' + str(result['NumBillableObjects']) + "\n" \
           + 'Total Deleted objects: ' + str(result['NumBillableDeletedObjects'])

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_sender, gmail_password)
        msg = EmailMessage()
        msg.set_content(body)

        msg['Subject'] = f'Wasabi Billing for {initial_time.date()}'
        msg['From'] = gmail_sender
        msg['To'] = receiver

        # Send the message via our own SMTP server.
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(e)
