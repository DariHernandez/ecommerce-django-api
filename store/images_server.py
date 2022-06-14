import os
import datetime

def upload_keagan (test_id="", test_start=True, file_name=""):

    "Upload images to keagan image server on github"
    
    # Move to images folder
    parent_folder = os.path.dirname(__file__)
    images_folder = os.path.join (os.path.dirname (parent_folder), "media", "keagan")
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


    # Commit and push files
    os.system (f'git add *{file_name}')
    os.system (f'git commit -m "{commit_name}"')
    os.system (f'git push origin master')

    # Found new files
    # found_files = []
    # for root, dirs, files in os.walk(images_folder):
    #     for name in files:
    #         if file_name in name:
    #             file_path = os.path.join(root, name)
    #             found_files.append (file_path)

    # Delete new files in local
    # for file in found_files:
    #     os.remove(file)