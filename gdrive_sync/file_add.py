from __future__ import absolute_import
from pkg_resources import resource_filename
# stores default file address
import os
import ntpath
import errno
from pydrive import settings

dir_path = os.path.dirname(os.path.realpath(__file__))
home = os.path.expanduser("~")


# list of manual addresses
# when launched as non-package
try:
    ver_file = os.path.join(dir_path, "docs/ver_info.txt")
    help_file = os.path.join(dir_path, "docs/readme.txt")
    arg_file = os.path.join(dir_path, "docs/args.txt")
    config_file = os.path.join(dir_path, "config_dicts/config.json")
    mime_dict = os.path.join(dir_path, "config_dicts/mime_dict.json")
    format_dict = os.path.join(dir_path, "config_dicts/formats.json")
    client_secrets = os.path.join(dir_path, ".client_secrets.json")
    settings_file = os.path.join(dir_path, "settings.yaml")
# when launched as package
except settings.InvalidConfigError or OSError:
    ver_file = resource_filename(__name__, "docs/ver_info.txt")
    help_file = resource_filename(__name__, "docs/readme.txt")
    arg_file = resource_filename(__name__, "docs/args.txt")
    config_file = resource_filename(__name__, "config_dicts/config.json")
    mime_dict = resource_filename(__name__, "config_dicts/mime_dict.json")
    format_dict = resource_filename(__name__, "config_dicts/formats.json")
    client_secrets = resource_filename(__name__, ".client_secrets.json")
    settings_file = resource_filename(__name__, "settings.yaml")


# returns credentials file address
def cred_file():

    # when launched as non-package
    try:
        return os.path.join(home, ".credentials.json")
    # when launched as package
    except settings.InvalidConfigError or OSError:
        return os.path.join(home, ".credentials.json")


# Checks if directory present, otherwise make it
def dir_exists(addr):
    if not os.path.exists(addr):
        try:
            os.makedirs(addr)
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise


# Extracts file name or folder name from full path
def get_f_name(addr):
    head, tail = ntpath.split(addr)
    return tail or ntpath.basename(head)  # return tail when file, otherwise other one for folder


# to eradicate circular import problems
if __name__ == "__main__":
    pass
