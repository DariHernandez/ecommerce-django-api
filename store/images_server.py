import os
import datetime

def upload_keagan (test_id="", test_start=True):

    "Upload images to keagan image server on github"
    
    # Move to images folder
    parent_folder = os.path.dirname(__file__)
    images_folder = os.path.join (os.path.dirname (parent_folder), "media")
    os.chdir (images_folder)

    # make commit and upload to github
    time_str = str(datetime.datetime.now())[:22]

    # Create commit name
    if test_id:
        if test_start:
            commit_name = f"start test: {test_id}"
        else:
            commit_name = f"end test: {test_id}"
    else:
        commit_name = f"update images {time_str}"


    os.system (f'git add -A')
    os.system (f'git commit -m "{commit_name}"')
    os.system (f'git push origin master')