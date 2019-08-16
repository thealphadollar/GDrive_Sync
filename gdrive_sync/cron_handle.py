from __future__ import print_function, absolute_import
import os
import sys
import pwd
import json
from crontab import CronTab

try:
    # set directory for relativistic import
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import file_add
    import file_ops
    import edit_config
except ImportError:
    from . import file_add
    from . import file_ops
    from . import edit_config


# returns current username
def get_username():
    return pwd.getpwuid(os.getuid())[0]


# code to be launched by cron periodically
def by_cron(drive,file_id=None):
    """
    Modified para get the file_id to save in the same directory
    """
    # traversing through all upload folders
    for folder in edit_config.up_addr():
        # stores if the file is being uploaded
        uploading = {}

        # load if status.json exists in the folder
        path = os.path.join(folder, "status.json")
        if os.path.exists(path):
            with open(path, 'r') as f_input:
                uploading = json.load(f_input)

        to_up = []  # stores files/folders to be uploaded by this cron instance
        for f in os.listdir(folder):
            if f not in uploading:
                uploading[f] = False

            # check if the file is not being uploaded
            if not uploading[f]:
                to_up.append(f)
                uploading[f] = True

        # saving back the status of files
        try:
            with open(path, 'w') as f_output:
                json.dump(uploading, f_output)
        except IOError:
            print("Error: insufficient permission to write to %s" % folder)
            return

        # processing upload queue
        for item in to_up:
            # ignoring status.json
            if item == "status.json":
                continue

            file_ops.f_up(drive, os.path.join(folder, item), file_id)

            # remove uploaded item from status.json
            with open(path, 'r') as f_input:
                uploading = json.load(f_input)
            del uploading[item]
            with open(path, 'w') as f_output:
                json.dump(uploading, f_output)


# returns true if GDrive_Sync is running
def is_running(remove):  # remove tells if the function was called from stop
    running = False
    cron = CronTab(user=get_username())
    for job in cron:
        if job.comment == 'start GDrive_Sync':
            if remove:
                cron.remove(job)
                print("GDrive_Sync stopped")
            running = True
    cron.write()
    return running


# cron progress execution from crontab
def cron_process(arg):
    if arg == "start":
        # add cron script if cron not running
        if not is_running(False):
            cron = CronTab(user=get_username())
            # when not run as drive_sync from command line
            if __package__ is None:
                gdrive_job = cron.new(command='%s -by_cron' % os.path.join(file_add.dir_path, 'main.py'),
                                      comment='start GDrive_Sync')
            # when run as package from command line
            else:
                gdrive_job = cron.new(command='drive_sync -by_cron', comment='start GDrive_Sync')
            gdrive_job.minute.every(5)  # setting to run every five minutes
            cron.write()
            print("GDrive_Sync started")

        else:
            print("GDrive_Sync is already running")

    elif arg == "stop":
        # removing gdrive_job from cron
        if not is_running(True):
            print("Error: GDrive_Sync is not running")

    elif arg == "status":
        # print the current status of cron

        if is_running(False):
            print("GDrive_Sync is running in background")
        else:
            print("GDrive_Sync is not running in background")
