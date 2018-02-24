#!/usr/bin/env python2

''' all important imports go below'''

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
import file_add


# function to handle authorisation of the user account

def drive_auth():  
    gauth = GoogleAuth()

    # looking for saved authentication data
    gauth.LoadCredentialsFile('credentials.json')

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()

    elif gauth.access_token_expired:
        # refresh authorisation if expired
        gauth.Refresh()

    else:
        # initialise the saved data
        gauth.Authorize()

    return gauth


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


if __name__ == "__main__":

    gauth = drive_auth()
    drive = GoogleDrive(gauth)

    arguments = sys.argv[1:]

    # if function called without any arguments print version info
    if len(arguments) == 0:
        p_info("ver")

    for arg_index in range(len(arguments)):
        if arguments[arg_index] == "-v" or arguments[arg_index] == "-version":
            p_info("ver")

        elif arguments[arg_index] == "-h" or arguments[arg_index] == "-help":
            p_info("help")

        elif arguments[arg_index] == "-i" or arguments[arg_index] == "-init":
            pass

        elif arguments[arg_index] == "-c" or arguments[arg_index] == "-config":
            pass

        elif arguments[arg_index] == "-d" or arguments[arg_index] == "-download":
            pass

        elif arguments[arg_index] == "-u" or arguments[arg_index] == "-upload":
            pass

        elif arguments[arg_index] == "-s" or arguments[arg_index] == "-share":
            pass




