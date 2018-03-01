from __future__ import print_function
from __future__ import absolute_import
# module contains all authorisation related functions

from pydrive.auth import GoogleAuth
from os import sys, path
import os

# set directory for relativistic import
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    import file_add
else:
    from . import file_add

# to handle authorisation of the user account


def drive_auth(reset):

    g_auth = GoogleAuth()

    # looking for saved authentication data
    g_auth.LoadCredentialsFile(file_add.cred_file)

    if g_auth.credentials is None or reset:
        if reset:
            if g_auth.credentials is not None:
                print("Error: Couldn't reset account. Please report at thealphadollar@iitkgp.ac.in")
                sys.exit(1)
        g_auth.LocalWebserverAuth()

    elif g_auth.access_token_expired:
        # refresh authorisation if expired
        g_auth.Refresh()

    else:
        # initialise the saved data
        g_auth.Authorize()

    return g_auth


# to handle account reset or change

def reset_account():
    if os.path.isfile(file_add.cred_file):
        os.remove(file_add.cred_file)

    drive_auth(1)
