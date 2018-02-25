# stores default file address
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


ver_file = os.path.join(dir_path, "docs/ver_info.txt")
help_file = os.path.join(dir_path, "docs/readme.txt")
arg_file = os.path.join(dir_path, "docs/args.txt")
cred_file = os.path.join(dir_path, "credentials.json")
config_file = os.path.join(dir_path, "config.json")
