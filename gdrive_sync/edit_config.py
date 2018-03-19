from __future__ import print_function, absolute_import
from builtins import input, str, map, range

import json
import os
import sys

try:
    # set directory for relativistic import
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import file_add
except ImportError:
    from . import file_add

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
    """
    appends address to upload list
    Args:
        addr: path of folder
    Returns:
        True if successful, False otherwise
    """
    if addr is None:
        print("Error: missing parameter")
        return False

    if os.path.isdir(addr):
        if addr not in config['Up_Dir']:
            config['Up_Dir'].append(addr)
            return True
        else:
            print("Folder already exists!")
            return False

    else:
        print("Error: Not a directory! Please check the address.")
        return False


def del_up_folder(addr):
    """
    removes address from upload list
    Args:
        addr: path of folder
    Returns:
        True if successful, False otherwise
    """
    if addr is None:
        print("Error: missing parameter")
        return False

    if os.path.isdir(addr):
        if addr in config['Up_Dir']:
            config['Up_Dir'].remove(addr)
            return True
        else:
            print("Error: Directory not in upload list!")
            return False

    else:
        print("Error: Not a directory! Please check the address.")
        return False


def modify_down_folder(addr):
    """
    changes address of downloads folder
    Args:
        addr: path of folder
    Returns:
        True if successful, False otherwise
    """
    if addr is None:
        print("Error: missing parameter")
        return False

    if os.path.isdir(addr):
        config['Down_Dir'] = addr
        return True

    else:
        print("Error: Not a directory! Please check the address.")
        return False


def rm_post_upload(value):
    """
    set value for remove post upload
    Args:
        value: True if file to be removed, false otherwise
    Returns:
        True if successful, False otherwise
    """
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


def share_link(value):
    """
    set value for share link
    Args:
        value: True if share link to be stored, false otherwise
    Returns:
        True if successful, False otherwise
    """
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
    """
    set value for write_permit
    Args:
        value: True if write permission to be given, false otherwise
    Returns:
        True if successful, False otherwise
    """
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
    5: share_link,
    6: write_permit
}


def write_config():
    """
    displays console for editing and manages input
    """
    global config

    config = read_config()

    print("GDrive_Sync")
    print("\nPlease look below at the options which you wish to update: ")
    print("(Enter the number followed by value, eg. \"1 input\")")
    print("1. Add Upload Folder [full path to folder]")
    print("2. Remove Upload Folder [full path to folder]")
    print("3. Change Download Directory [full path to folder]")
    print("4. Toggle Remove_Post_Upload [Y/N]")
    print("5. Toggle Save_Share_Link [Y/N]")
    print("6. Toggle Write_Permission [Y/N]")
    print("7. List current settings [type \"7 ls\"]")
    print("\nInput \"0 exit\" at anytime to exit config edit")

    while True:
        user_input = str(input())
        value = None  # define value to None to catch error
        try:
            if len(user_input.split()) == 1:
                opt = int(user_input)
            elif len(user_input.split()) > 1:
                opt, value = list(map(str, user_input.split()))
        except ValueError:
            print("Error: please adhere to the input format")
            continue

        # if input is not acceptable by int
        try:
            if int(opt) == 0:
                break

            elif int(opt) == 7:
                print("---Current Configuration---")
                print("Download directory: " + config['Down_Dir'])
                print("Upload directories: " + str(config['Up_Dir']))
                print("Remove post upload: " + str(config['Remove_Post_Upload']))
                print("Save share link: " + str(config['Share_Link']))
                print("Write permission granted: " + str(config['Write_Permission']))

            elif int(opt) not in list(range(1, 7)):
                print("Error: Wrong parameters entered")

            elif option[int(opt)](value):
                print("Success")
        except ValueError:
            print("Error: invalid input")
            continue

    try:
    	with open(file_add.config_file, "w") as output:
    	    json.dump(config, output)
   	except IOError:
   		print("Permission Denied: please run with sudo")


def read_config():
    """
    reads the configuration
    Args:
        None
    Returns:
        temp: dictionary having configuration data
    """
    with open(file_add.config_file, 'r') as f_input:
        temp = json.load(f_input)

    return temp


def down_addr():
    """
    reads download directory address from configuration
    Args:
        None
    Returns:
        addr: path to download directory
    """
    # Making file address for upload and downloads
    config = read_config()
    addr = os.path.join(os.path.expanduser('~'), config['Down_Dir'])
    # making directory if it doesn't exist
    file_add.dir_exists(addr)
    return addr


def up_addr():
    """
    reads upload directories' from configuration
    Args:
        None
    Returns:
        up_addr_list: list of path to upload directories
    """
    up_addr_list = []
    config = read_config()
    for addr in config['Up_Dir']:
        # making directory if it doesn't exist
        file_add.dir_exists(os.path.join(os.path.expanduser('~'), addr))
        up_addr_list.append(os.path.join(os.path.expanduser('~'), addr))
    return up_addr_list


# return the address of the file to store shares
share_store = os.path.join(down_addr(), "share_links.txt")
