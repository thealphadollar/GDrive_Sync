# stores default file address
import os
import ntpath
import errno
import edit_config

dir_path = os.path.dirname(os.path.realpath(__file__))


# list of manual addresses
ver_file = os.path.join(dir_path, "docs/ver_info.txt")
help_file = os.path.join(dir_path, "docs/readme.txt")
arg_file = os.path.join(dir_path, "docs/args.txt")
cred_file = os.path.join(dir_path, "credentials.json")
config_file = os.path.join(dir_path, "config_dicts/config.json")
mime_dict = os.path.join(dir_path, "config_dicts/mime_dict.json")
format_dict = os.path.join(dir_path, "config_dicts/formats.json")


# Making file address for upload and downloads
config = edit_config.read_config()


# Checks if directory present, otherwise make it
def dir_exists(addr):
    if not os.path.exists(addr):
        try:
            os.makedirs(addr)
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise


# Returns the current download directory address
def down_addr():
    addr = os.path.join(os.path.expanduser('~'), config['Down_Dir'])
    # making directory if it doesn't exist
    dir_exists(addr)
    return addr


# Returns list with current set upload directories
def up_addr():
    up_addr_list = []
    for addr in config['Up_Dir']:
        # making directory if it doesn't exist
        dir_exists(os.path.join(os.path.expanduser('~'), addr))
        up_addr_list.append(os.path.join(os.path.expanduser('~'), addr))
    return up_addr_list


# Extracts file name or folder name from full path
def get_f_name(addr):
    head, tail = ntpath.split(addr)
    return tail or ntpath.basename(head)  # return tail when file, otherwise other one for folder


# list of manual addresses
share_store = os.path.join(down_addr(), "share_links.txt")
