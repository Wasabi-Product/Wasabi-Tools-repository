delete_old_versioned_objects.py
--

For more details go here:
[How do I mass delete non-current versions inside a bucket?
](https://wasabi-support.zendesk.com/hc/en-us/articles/360058028992-How-do-I-mass-delete-non-current-versions-inside-a-bucket-)

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