# Support Tools  for Wasabi Technologies, LLC

This repository consists of scripts for Wasabi Technologies, LLC

automation
--

Follow this link for the [automation script repository](https://github.com/xelese/Wasabi-Automation).

delete_delete_markers
--
This Script will take the following inputs:

1. Profile name / Access key and Secret Key
2. Bucket name
3. Region
4. Prefix

Calculate the size and count of the total number of delete markers, current and non-current objects.with filtered prefix
or not Will ask for a prompt delete the delete-markers.

delete_old_versioned_objects
--
This Script will take the following inputs:

1. Profile name / Access key and Secret Key
2. Bucket name
3. Region
4. Prefix

Calculate the size and count of the total number of delete markers, current and non-current objects.with filtered prefix
or not Will ask for a prompt delete the delete-markers and non-current objects.

get_size_and_count_of_objects
--
This Script will take the following inputs:

1. Profile name / Access key and Secret Key
2. Bucket name
3. Region
4. Prefix

Calculate the size and count of the total number of delete markers, current and non-current objects with filtered prefix
or not.

lifecycle
--
This directory consists of lifecycle replacement scripts for Wasabi, allows one to set up a cron job with the python
script to remove old versioned and current objects based on the type of script you set up.

terraform-automation
--
This directory contains the Terraform scripts that can be used for Wasabi automation. Follows the same automation as
this [automation model](https://github.com/xelese/Wasabi-Automation). Implementation details are in the directory.

janitor
--
This is a simple python file that can wipe a wasabi account of all users, groups buckets to give a clean slate to work
on.

billing_job
--
Uses the billing API to send egress data, deleted, active storage and other important notifications as an email to the
user.

gui_egress_calculator
--
self-contained kivy application that calculates the egress for a set number days. Just need to download and run the app.


Thanks for reading and improving this repo :)
