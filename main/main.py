#!/usr/bin/env python2

# all important imports go below

from pydrive.drive import GoogleDrive
import sys
import file_add
import auth
import edit_config
import file_ops


# function to print data to console
def p_info(p_str):

    if p_str == "ver":
        with open(file_add.ver_file) as p_file:
            if p_file is None:
                print("Error reading version file. Please report at thealphadollar@iitkgp.ac.in")
                return
            p_data = p_file.read()
            print(p_data)

    elif p_str == "help":
        with open(file_add.help_file) as p_file:
            if p_file is None:
                print("Error reading help file. Please report at thealphadollar@iitkgp.ac.in")
                return
            p_data = p_file.read()
            print(p_data)

    elif p_str == "arg":
        with open(file_add.arg_file) as p_file:
            if p_file is None:
                print("Error reading arguments' file. Please report at thealphadollar@iitkgp.ac.in")
                return
            p_data = p_file.read()
            print(p_data)


if __name__ == "__main__":

    gauth = auth.drive_auth(0)  # parameter to reset GAccount permissions
    drive = GoogleDrive(gauth)

    arguments = sys.argv[1:]

    # if function called without any arguments print version info
    if len(arguments) == 0:
        p_info("ver")

    arg_index = 0

    while True:

        if arg_index >= len(arguments):
            break

        elif arguments[arg_index] == "-v" or arguments[arg_index] == "-version":
            p_info("ver")

        elif arguments[arg_index] == "-h" or arguments[arg_index] == "-help":
            p_info("help")

        elif arguments[arg_index] == "-i" or arguments[arg_index] == "-init":
            auth.reset_account()

        elif arguments[arg_index] == "-c" or arguments[arg_index] == "-config":
            edit_config.write_config()

        elif arguments[arg_index] == "-d" or arguments[arg_index] == "-download":
            pass

        elif arguments[arg_index] == "-u" or arguments[arg_index] == "-upload":
            pass

        elif arguments[arg_index] == "-s" or arguments[arg_index] == "-share":
            pass

        elif arguments[arg_index] == "-r" or arguments[arg_index] == "-remove":
            pass

        elif arguments[arg_index] == "-o" or arguments[arg_index] == "-open":
            pass

        elif arguments[arg_index] == "-ls_files" or arguments[arg_index] == "-laf":
            arg_index += 1
            file_ops.f_list(drive, arguments[arg_index], 1)

        elif arguments[arg_index] == "-ls" or arguments[arg_index] == "-l":
            file_ops.f_list(drive, "all", 0)

        elif arguments[arg_index] == "-ls_trash" or arguments[arg_index] == "-lt":
            file_ops.f_list(drive, "trash", 0)

        elif arguments[arg_index] == "-ls_folder" or arguments[arg_index] == "-lf":
            arg_index += 1  # increase arg_index to read the query argument
            file_ops.f_list(drive, arguments[arg_index], 0)

        else:
            print("Unrecognised argument. Please report if you know this is an error.\n\n")
            p_info("arg")

        arg_index += 1




