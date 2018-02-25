import json
import os
import file_add

'''
config = {
    'Up_Dir': ['/local'],
    'Down_Dir': '/remote',
    'Remove_Post_Upload': True,
    'Down_All': False,
    'Share_Link': True
}
'''

config = {}


def add_up_folder(addr):
    if os.path.isdir(addr):
        if addr.lower() not in config['Up_Dir']:
            config['Up_Dir'].append(addr.lower())
            return True
        else:
            print("Folder already exists!")
            return False

    else:
        print("Not a directory! Please check the address.")
        return False


def del_up_folder(addr):
    if os.path.isdir(addr):
        if addr.lower() in config['Up_Dir']:
            config['Up_Dir'].remove(addr.lower())
            return True
        else:
            print("Directory not in upload list!")
            return False

    else:
        print("Not a directory! Please check the address.")
        return False


def modify_down_folder(addr):
    if os.path.isdir(addr):
        config['Down_Dir'] = addr.lower()
        return True

    else:
        print("Not a directory! Please check the address.")
        return False


def rm_post_upload(value):
    if value.lower() == 'n':
        config['Remove_Post_Upload'] = False
        return True

    elif value.lower() == 'y':
        config['Remove_Post_Upload'] = True
        return True

    else:
        print("Wrong parameter to change to!")
        return False


def down_all(value):
    if value.lower() == 'n':
        config['Down_All'] = False
        return True

    elif value.lower() == 'y':
        config['Down_All'] = True
        return True

    else:
        print("Wrong parameter to change to!")
        return False


def share_link(value):
    if value.lower() == 'n':
        config['Share_Link'] = False
        return True

    elif value.lower() == 'y':
        config['Share_Link'] = True
        return True

    else:
        print("Wrong parameter to change to!")
        return False


option = {
    1: add_up_folder,
    2: del_up_folder,
    3: modify_down_folder,
    4: rm_post_upload,
    5: down_all,
    6: share_link
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
    print("7. List current settings [type \"7 ls\"]")
    print("\nInput \"0 exit\" at anytime to exit config edit")

    while True:
        opt, value = map(str, raw_input().split())
        if int(opt) == 0:
            break

        elif int(opt) == 7:
            print(config)

        elif int(opt) not in range(1, 7):
            print("Wrong value entered, please try again!")

        elif option[int(opt)](value):
            print("Success")

    with open(file_add.config_file, "w") as output:
        json.dump(config, output)


def read_config():

    with open(file_add.config_file, 'r') as f_input:
        temp = json.load(f_input)

    return temp
