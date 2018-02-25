# contains file operations and functions


def f_list(drive, keyword, recursive):

    if recursive:
        file_list = []
        if keyword == "root":
            for f in drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList():
                # if file in list is folder, get it's file list
                if f['mimeType'] == 'application/vnd.google-apps.folder':
                    f_all(drive, f['id'], file_list)
                else:
                    file_list.append(f)
        else:
            f_all(drive, keyword, file_list)

        for f in file_list:
            print('title: %s, id: %s' % (f['title'], f['id']))

    # lists all files and folder except trash
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


# function to list all files recursively inside a folder


def f_all(drive, fold_id, file_list):
    q_string = "'%s' in parents and trashed=false" % fold_id
    for f in drive.ListFile({'q': q_string}).GetList():
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            f_all(drive, f['id'], file_list)
        else:
            file_list.append(f)
