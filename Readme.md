# Support Tools  for Wasabi Technologies, Inc.

This repository consists of scripts written by Ravi Voleti for Wasabi Technologies, Inc. for storage calculations.

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

Thanks for reading :)