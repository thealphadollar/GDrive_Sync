#!/usr/bin/env python2

# all important imports go below

from pydrive.drive import GoogleDrive
import sys
import file_add
import auth
import edit_config
import file_ops
import cron_handle


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


# checks if number of expected arguments and given arguments mismatch
def is_matching(index, len_arg):
    if index >= len_arg:
        print("Error: arguments less than what expected")
        return False
    return True


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

        elif arguments[arg_index] == "-v" or arguments[arg_index] == "-version" or arguments[arg_index] == "version":
            p_info("ver")

        elif arguments[arg_index] == "-h" or arguments[arg_index] == "-help" or arguments[arg_index] == "help":
            p_info("help")

        elif arguments[arg_index] == "-re" or arguments[arg_index] == "-reset" or arguments[arg_index] == "reset":
            auth.reset_account()

        elif arguments[arg_index] == "-st" or arguments[arg_index] == "-start" or arguments[arg_index] == "start":
            cron_handle.cron_process(drive, "start")

        elif arguments[arg_index] == "-x" or arguments[arg_index] == "-stop" or arguments[arg_index] == "stop":
            cron_handle.cron_process(drive, "stop")

        elif arguments[arg_index] == "-y" or arguments[arg_index] == "-status" or arguments[arg_index] == "status":
            cron_handle.cron_process(drive, "status")

        elif arguments[arg_index] == "-c" or arguments[arg_index] == "-config" or arguments[arg_index] == "config":
            edit_config.write_config()

        elif arguments[arg_index] == "-d" or arguments[arg_index] == "-download" or arguments[arg_index] == "download":
            arg_index += 1
            file_ops.f_down(drive, arguments[arg_index], file_add.down_addr())

        elif arguments[arg_index] == "-u" or arguments[arg_index] == "-upload" or arguments[arg_index] == "upload":
            arg_index += 1
            if is_matching(arg_index, len(arguments)):
                # adding to root folder hence None
                file_ops.f_create(drive, arguments[arg_index], None, str(file_add.get_f_name(arguments[arg_index])),
                                  True)

        elif arguments[arg_index] == "-s" or arguments[arg_index] == "-share" or arguments[arg_index] == "share":
            arg_index += 1
            if is_matching(arg_index, len(arguments)):
                file_ops.share_link(drive, arguments[arg_index], True)

        elif arguments[arg_index] == "-r" or arguments[arg_index] == "-remove" or arguments[arg_index] == "remove":
            arg_index += 2
            # in case of less arguments than required
            if is_matching(arg_index, len(arguments)):
                file_ops.f_remove(drive, arguments[arg_index - 1], arguments[arg_index:len(arguments)])
                arg_index = len(arguments)

        elif arguments[arg_index] == "-o" or arguments[arg_index] == "-open" or arguments[arg_index] == "open":
            arg_index += 1
            if is_matching(arg_index, len(arguments)):
                file_ops.f_open(arguments[arg_index])

        elif arguments[arg_index] == "-ls_files" or arguments[arg_index] == "-laf" or \
                arguments[arg_index] == "ls_files":
            arg_index += 1
            if is_matching(arg_index, len(arguments)):
                file_ops.f_list(drive, arguments[arg_index], 1)

        elif arguments[arg_index] == "-ls" or arguments[arg_index] == "-l" or arguments[arg_index] == "ls":
            if (arg_index + 1) < len(arguments):
                if arguments[arg_index + 1] == "remote":
                    arg_index += 1
                    file_ops.f_list(drive, "all", 0)
                # list of files in downloads directory
                elif arguments[arg_index + 1] == "local":
                    arg_index += 1
                    file_ops.f_list_local()
                # no argument matching -ls
                else:
                    file_ops.f_list(drive, "all", 0)

            # no argument after -ls
            else:
                file_ops.f_list(drive, "all", 0)

        elif arguments[arg_index] == "-ls_trash" or arguments[arg_index] == "-lt" or arguments[arg_index] == "ls_trash":
            file_ops.f_list(drive, "trash", 0)

        elif arguments[arg_index] == "-ls_folder" or arguments[arg_index] == "-lf" or \
                arguments[arg_index] == "ls_folder":
            arg_index += 1  # increase arg_index to read the query argument
            if is_matching(arg_index, len(arguments)):
                file_ops.f_list(drive, arguments[arg_index], 0)

        else:
            print(str(arguments[arg_index]) + " is an unrecognised argument. Please report if you know this is an error"
                                              ".\n\n")
            p_info("arg")

        arg_index += 1
