delete_old_versioned_objects.py
--

For more details go here:
https://wasabi-support.zendesk.com/hc/en-us/articles/360045760851-How-do-I-mass-delete-current-and-old-object-versions-inside-a-bucket-

Prerequisites:

- Install python3.
- install requirements form requirements.txt file.

Run:

On a terminal run

`python3 delete_old_versioned_objects.py`

Build:

- Standalone executable can be found in dist directory. Just double-click to run

To make your own standalone file run:

`pyinstaller delete_old_versioned_objects.py --onefile`