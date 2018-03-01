from __future__ import print_function
from __future__ import absolute_import
# contains file operations and functions
from builtins import str
import json
import os
from os import sys, path
import shutil
from pydrive import files

# set directory for relativistic import
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import file_add
import edit_config


# list all files and folders in the downloads directory
def f_list_local():
    for f in os.listdir(file_add.down_addr()):
        print(f)


# Operations for file list commands
def f_list(drive, keyword, recursive):

    # get recursively all files in the folder
    if recursive:
        file_list = []
        if keyword == "root":
            for f in drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList():
                # if file in list is folder, get it's file list
                if f['mimeType'] == 'application/vnd.google-apps.folder':
                    f_all(drive, f['id'], file_list, False, None)
                else:
                    file_list.append(f)
        else:
            f_all(drive, keyword, file_list, False, None)

        for f in file_list:
            print('title: %s, id: %s' % (f['title'], f['id']))

    # lists all files and folder inside given folder
    else:
        if keyword == "all":
            file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
            for f in file_list:
                print('title: %s, id: %s' % (f['title'], f['id']))

        # lists all files and folders inside trash
        elif keyword == "trash":
            file_list = drive.ListFile({'q': "'root' in parents and trashed=true"}).GetList()
            for f in file_list:
                print('title: %s, id: %s' % (f['title'], f['id']))

        # lists all files and folders inside folder given as argument in keyword
        else:
            q_string = "'%s' in parents and trashed=false" % keyword
            file_list = drive.ListFile({'q': q_string}).GetList()
            for f in file_list:
                print('title: %s, id: %s' % (f['title'], f['id']))


# Grab all file names recursively inside a folder
def f_all(drive, fold_id, file_list, download, down_folder):
    q_string = "'%s' in parents and trashed=false" % fold_id
    for f in drive.ListFile({'q': q_string}).GetList():
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            if download:  # if we are to download the files
                temp_d_folder = os.path.join(down_folder, f['title'])
                file_add.dir_exists(temp_d_folder)
                f_all(drive, f['id'], None, True, temp_d_folder)

            else:  # we want to just list the files
                f_all(drive, f['id'], file_list, False, None)
        else:
            if download:
                f_down(drive, f['id'], down_folder)
            else:
                file_list.append(f)


# Download file using given file_id to downloads folder
def f_down(drive, f_id, down_folder):

    # check if file id not valid
    if not is_valid_id(drive, f_id):
        return

    d_file = drive.CreateFile({'id': f_id})

    # open mime_swap dictionary for changing mimeType if required
    with open(file_add.mime_dict) as f:
        mime_swap = json.load(f)

    # checking if the specified id belongs to a folder
    if d_file['mimeType'] == mime_swap['folder']:
        if d_file['title'] in os.listdir(down_folder):
            print("%s already present in %s" % (d_file['title'], down_folder))

        else:
            print("creating folder " + os.path.join(down_folder, d_file['title']))
            file_add.dir_exists(os.path.join(down_folder, d_file['title']))
            f_all(drive, d_file['id'], None, True, os.path.join(down_folder, d_file['title']))

    elif d_file['mimeType'] in mime_swap:  # for online file types like GDocs, GSheets etc.

        # open formats.json for adding custom format
        with open(file_add.format_dict) as f:
            format_add = json.load(f)

        f_name = d_file['title'] + format_add[d_file['mimeType']]  # changing file name to suffix file format
        if f_name in os.listdir(down_folder):
            print("%s already present in %s" % (f_name, down_folder))

        else:
            print("downloading " + os.path.join(down_folder, f_name))
            d_file.GetContentFile(os.path.join(down_folder, f_name),
                                  mimetype=mime_swap[d_file['mimeType']])

    else:
        if d_file['title'] in os.listdir(down_folder):
            print("%s already present in %s" % (d_file['title'], down_folder))

        else:
            print("downloading " + os.path.join(down_folder, d_file['title']))
            d_file.GetContentFile(os.path.join(down_folder, d_file['title']))


# Upload file/folder to GDrive, last argument is relative address
def f_create(drive, addr, fold_id, rel_addr, show_update):
    # check whether address is right or not
    if not os.path.exists(addr):
        print("Specified file/folder doesn't exist, check the address!")
        return

    # creating if it's a folder
    if os.path.isdir(addr):
        # print progress
        if show_update:
            print("creating folder " + rel_addr)
        # if folder to be added to root
        if fold_id is None:
            folder = drive.CreateFile()
        # if folder to be added to some other folder
        else:
            folder = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": fold_id}]})

        folder['title'] = file_add.get_f_name(addr)  # sets folder title
        folder['mimeType'] = 'application/vnd.google-apps.folder'  # assigns it as GDrive folder
        folder.Upload()

        # traversing inside files/folders
        for item in os.listdir(addr):
            f_create(drive, os.path.join(addr, item), folder['id'], rel_addr + "/" +
                     str(file_add.get_f_name(os.path.join(addr, item))), show_update)

    # creating file
    else:
        # print progress
        if show_update:
            print("uploading file " + rel_addr)
        # if file is to be added to root
        if fold_id is None:
            up_file = drive.CreateFile()
        # if file to be added to some folder in drive
        else:
            up_file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": fold_id}]})

        up_file.SetContentFile(addr)
        up_file['title'] = file_add.get_f_name(addr)  # sets file title to original
        up_file.Upload()

        # saves share link if required
        if not show_update and edit_config.read_config()['Share_Link']:
            share_link(drive, up_file['id'], False)

    return True


# Upload a file through cron
def f_up(drive, addr, fold_id):
    # checks if the specified file/folder exists
    if not os.path.exists(addr):
        print("Specified file/folder doesn't exist, please remove from upload list using -config")
        return

    # pass the address to f_create and on success delete/move file/folder
    if f_create(drive, addr, fold_id, str(file_add.get_f_name(addr)), False):
        # remove file if Remove_Post_Upload is true, otherwise move to GDrive downloads
        remove_post_upload = edit_config.read_config()['Remove_Post_Upload']
        if remove_post_upload:
            # use recursive removal if directory
            if os.path.isdir(addr):
                shutil.rmtree(addr)
            # normal os removal for file
            else:
                os.remove(addr)
        else:
            shutil.move(addr, file_add.down_addr())
    else:
        print("Upload unsuccessful, please try again!")


# Opens download/uploads folder
def f_open(folder):
    if folder.lower() == "download":
        os.system('xdg-open "%s"' % file_add.down_addr())

    elif folder.lower() == "upload":
        for addr in file_add.up_addr():
            os.system('xdg-open "%s"' % addr)

    else:
        print("%s is an unrecognised argument for open" % folder)


# removes a file from remote/local
def f_remove(drive, mode, addrs):

    if mode == "local":
        down_dir = file_add.down_addr()
        # Appending file/folder name to download directory
        for addr in addrs:
            f_path = os.path.join(down_dir, addr)
            if not os.path.exists(f_path):
                print("%s doesn't exist in %s" % (addr, down_dir))
            else:
                # use recursive removal if directory
                if os.path.isdir(addr):
                    shutil.rmtree(f_path)
                else:
                    os.remove(f_path)
                print("%s removed from %s" % (addr, down_dir))

    # Move file in GDrive to trash or delete permanently
    elif mode == "remote":
        for addr in addrs:
            # check if file_id valid
            if is_valid_id(drive, addr):
                # file to be removed
                r_file = drive.CreateFile({'id': addr})
                f_name = r_file['title']
                # delete permanently if in trash
                if is_trash(drive, r_file['id']):
                    r_file.Delete()
                    print("%s deleted permanently" % f_name)
                # move to trash
                else:
                    r_file.Trash()
                    print("%s moved to GDrive trash. List files in trash by -lt parameter" % f_name)
    else:
        print("%s is not a valid mode" % mode)
        return


# provide share link, last argument True prints to console, otherwise write to file
def share_link(drive, file_id, to_print):
    if is_valid_id(drive, file_id):
        # creating shared file
        s_file = drive.CreateFile({'id': file_id})
        # check if writing permission allowed by user
        if edit_config.read_config()['Write_Permission']:
            role = "writer"
        else:
            role = "reader"
        # inserting the new permissions
        s_file.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': role
        })
        # fetching the alternate link
        s_file.FetchMetadata(fields='alternateLink, title')

        if to_print:
            print(s_file['alternateLink'])
        # save to file end
        else:
            with open(file_add.share_store, "a") as share_store:
                share_store.write(s_file['title'] + ": " + s_file['alternateLink'] + "\n")


# return if file_id belongs to trash
def is_trash(drive, file_id):
    for f in drive.ListFile({'q': "'root' in parents and trashed=true"}).GetList():
        if file_id == f['id']:
            return True
    return False


# check if file_id is valid
def is_valid_id(drive, file_id):
    try:
        r_file = drive.CreateFile({'id': file_id})
        r_file['title']
    # catch invalid file id
    except files.ApiRequestError:
        print("%s is an invalid file_id!" % file_id)
        return False
    return True
