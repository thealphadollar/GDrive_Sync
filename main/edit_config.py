from __future__ import print_function
from __future__ import absolute_import
import json
import os
from os import sys, path

# set directory for relativistic import
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import file_add

'''
Default values for config.json
config = {
    'Up_Dir': ['Documents/to_GDrive'],
    'Down_Dir': 'Documents/from_GDrive',
    'Remove_Post_Upload': True,
    'Share_Link': True,
    'Write_Permission': False,
}
'''

config = {}


def add_up_folder(addr):
    if addr is None:
        print("Error: missing parameter")
        return False

    if os.path.isdir(addr):
        if addr.lower() not in config['Up_Dir']:
            config['Up_Dir'].append(addr.lower())
            return True
        else:
            print("Folder already exists!")
            return False

    else:
        print("Error: Not a directory! Please check the address.")
        return False


def del_up_folder(addr):
    if addr is None:
        print("Error: missing parameter")
        return False

    if os.path.isdir(addr):
        if addr.lower() in config['Up_Dir']:
            config['Up_Dir'].remove(addr.lower())
            return True
        else:
            print("Error: Directory not in upload list!")
            return False

    else:
        print("Error: Not a directory! Please check the address.")
        return False


def modify_down_folder(addr):
    if addr is None:
        print("Error: missing parameter")
        return False

    if os.path.isdir(addr):
        config['Down_Dir'] = addr.lower()
        return True

    else:
        print("Error: Not a directory! Please check the address.")
        return False


def rm_post_upload(value):
    if value is None:
        print("Error: missing parameter")
        return False

    if value.lower() == 'n':
        config['Remove_Post_Upload'] = False
        return True

    elif value.lower() == 'y':
        config['Remove_Post_Upload'] = True
        return True

    else:
        print("Error: Wrong parameter to change to!")
        return False


def down_all(value):
    if value is None:
        print("Error: missing parameter")
        return False

    if value.lower() == 'n':
        config['Down_All'] = False
        return True

    elif value.lower() == 'y':
        config['Down_All'] = True
        return True

    else:
        print("Error: Wrong parameter to change to!")
        return False


def share_link(value):
    if value is None:
        print("Error: missing parameter")
        return False

    if value.lower() == 'n':
        config['Share_Link'] = False
        return True

    elif value.lower() == 'y':
        config['Share_Link'] = True
        return True

    else:
        print("Error: Wrong parameter to change to!")
        return False


def write_permit(value):
    if value is None:
        print("Error: missing parameter")
        return False

    if value.lower() == 'n':
        config['Write_Permission'] = False
        return True

    elif value.lower() == 'y':
        config['Write_Permission'] = True
        return True

    else:
        print("Error: Wrong parameter to change to!")
        return False


option = {
    1: add_up_folder,
    2: del_up_folder,
    3: modify_down_folder,
    4: rm_post_upload,
    5: down_all,
    6: share_link,
    7: write_permit
}


def write_config():
    global config

    config = read_config()

    print("GDrive_Sync")
    print("\nPlease look below at the options which you wish to update: ")
    print("(Enter the number followed by value, eg. \"1 input\")")
    print("1. Add Upload Folder [full path to folder]")
    print("2. Remove Upload Folder [full path to folder]")
    print("3. Change Download Directory [full path to folder]")
    print("4. Toggle Remove_Post_Upload [Y/N]")
    print("5. Toggle Down_All [Y/N]")
    print("6. Toggle Save_Share_Link [Y/N]")
    print("7. Toggle Write_Permission [Y/N]")
    print("8. List current settings [type \"8 ls\"]")
    print("\nInput \"0 exit\" at anytime to exit config edit")

    while True:
        user_input = str(raw_input())
        value = None  # define value to None to catch error
        try:
            if len(user_input.split()) == 1:
                opt = int(user_input)
            elif len(user_input.split()) > 1:
                opt, value = map(str, user_input.split())
        except ValueError:
            print("Error: please adhere to the input format")
            continue

        # if input is not acceptable by int
        try:
            if int(opt) == 0:
                break

            elif int(opt) == 8:
                print("---Current Configuration---")
                print("Download directory: " + config['Down_Dir'])
                print("Upload directories: " + str(config['Up_Dir']))
                print("Remove post upload: " + str(config['Remove_Post_Upload']))
                print("Download all: " + str(config['Down_All']))
                print("Save share link: " + str(config['Share_Link']))
                print("Write permission granted: " + str(config['Write_Permission']))

            elif int(opt) not in range(1, 8):
                print("Error: Wrong parameters entered")

            elif option[int(opt)](value):
                print("Success")
        except ValueError:
            print("Error: invalid input")
            continue

    with open(file_add.config_file, "w") as output:
        json.dump(config, output)


# returns the current configuration file
def read_config():

    with open(file_add.config_file, 'r') as f_input:
        temp = json.load(f_input)

    return temp
