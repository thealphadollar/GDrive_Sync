# GDrive_Sync [![Build Status](https://travis-ci.org/thealphadollar/GDrive_Sync.svg?branch=master)](https://travis-ci.org/thealphadollar/GDrive_Sync)

This repository contains scripts that make GDrive tasks easier using command line functions and PyDrive wrapper for Google Drive.

GDrive_Sync aims at making life simpler when switching from Windows to Linux

This was developed with the aim to create a free and open source GDrive client to make things simpler and users won't
need to switch to other cloud file storing platforms or have to pay for commercial clients doing the same.

## Operational Details

GDrive_Sync asks for permission from your Google Drive account to carry out the essential operations as are mentioned later
in the document.

GDrive_Sync uses [PyDrive](https://github.com/googledrive/PyDrive) and [crontab](https://pypi.python.org/pypi/python-crontab) to interact with GDrive and Unix cron process manager respectively. It also requires 
root permission for the "-start", "-stop" and "-status" argument since it needs to alter the CronTab files.

[futurize](http://python-future.org/overview.html) library is used for the purpose of making the code compatible with both, python 2 and python 3.  

## Installation And Usage

Current build works on Python 2 (Python 3 is supported but a [bug](https://github.com/thealphadollar/GDrive_Sync/issues/11) is there which does not allow connection to be established on systems using proxy).

### Dependencies
Please install pip before moving on if you don't have python-pip<br/>
`sudo apt-get update`<br/>
`sudo apt-get install python-pip`<br/>

Once pip is installed, download the below dependencies (you don't need to follow the below steps if using pip installation method).
1. PyDrive<br/>
`pip2 install PyDrive`
2. crontab<br/>
`pip2 install python-crontab`
3. future<br/>
`pip2 install future`

### Installing
The repository can be installed through pip or by manually cloning the repository. 

##### Using pip

1. Use the below command to install drive_sync using pip2 (till [python3 bug](https://github.com/thealphadollar/GDrive_Sync/issues/11) is resolved)<br/>
`pip2 install drive_sync`<br/>
This process also installs all the missing dependencies.
2. Open the crontab editor in terminal,<br/>
`crontab -e`<br/>
and add the [following lines](https://superuser.com/questions/784252/crontab-and-binaries-in-usr-local-bin) to it.<br/>
`PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin`<br/>
`LD_LIBRARY_PATH=/usr/local/lib`
3. To initiate the upload process from default directory.<br/>
`drive_sync -start` <br/>
This will open a web browser if its the first launch of GDrive_Sync. Later it'll be used to start the process with previously
associated GAccount unless "-reset" is used.
4. Now GDrive_Sync will be monitoring set upload/download folders. Use `-config` parameter to add/modify upload or download
directory.
5. To stop GDrive_Sync at any instance,<br/>
`drive_sync -stop`
6. To know if GDrive_Sync is active,<br/>
`./gdrive_sync/main.py -status` 

##### Manual Cloning

1. Clone the [repository](https://github.com/thealphadollar/GDrive_Sync.git), <br/>
`git clone https://github.com/thealphadollar/GDrive_Sync.git`
2. Open the folder and give<br/>
`./gdrive_sync/main.py -start`<br/>
This command adds `./gdrive_sync/main.py -start` to your cron jobs with periodicity of 5 minutes.
3. A link will open asking for GDrive access; allow for all.
4. Now GDrive_Sync will be monitoring set upload/download folders. Use `-config` parameter to add/modify upload or download
directory.
5. To stop GDrive_Sync at any instance,<br/>
`./gdrive_sync/main.py -stop`
6. To know if GDrive_Sync is active,<br/>
`./gdrive_sync/main.py -status` 

### What Cron Script Does?

The code for this is present in `gdrive_sync/cron_handle.py`

- Periodically checks (every 5 minutes) the upload folders for a file change.
- If a new file is found which is not being uploaded by any other instance of the same function, it marks it as being uploaded
and starts the upload process.
- status.json in every folder is used to monitor the "being_uploaded" status of each file in the folder.
- If Remove_Post_Upload is True in `config_dicts/config.json`, then the file is deleted post upload to GDrive. Otherwise, 
it is moved to the set download directory.
- If Share_Link is True in `config_dicts/config.json` then a share link for each uploaded file is placed in the set download
directory. 
- It is highly advisable to set your own download and upload directories.

### Why Require GDrive Authentication?

GDrive_Sync requires Google Drive full read and write access. 

It asks for "https://www.googleapis.com/auth/drive" which translates to,<br/>
"Full, permissive scope to access all of a user's files, excluding the Application Data folder. Request this scope only when it is strictly necessary."<br/>

This is required in order to download and upload files as well as create directories along with creation of sharable link.

The author cannot modify/manipulate any personal data or Google Drive files. All the write/read access are provided solely to
the user granting the permission.  
 
## Parameters

The parameters that can be used are:

* -reset

Reset account associated with GDrive_Sync and give it the read and write permissions to your Google Drive. Automatically executed at the
first run of GDrive_Sync.

* -start

Start the automatic GDrive syncing of the folders set as upload directories.

* -stop

Stop the automatic GDrive syncing of the folders set as upload directories.

* -status

Shows whether GDrive is uploading automatically or not.

* -version

Shows the current version of the GDrive_Sync.

* -config

Gives option to edit the configuration file on which automatic upload and download works.
- Up_Directory: The directory where the files that are to be uploaded are given, relative to home directory.
    (e.g. for "~/Documents/to_GDrive", input "Documents/to_GDrive")
    (Default is "to_GDrive" directory in your Documents folder)
- Down_Directory: The directory where the files are downloaded, relative to home directory.
    (e.g. for "~/Documents/from_GDrive", input "Documents/from_GDrive")
    (Default is "from_GDrive" directory in you Documents folder)
- Remove_Post_Upload: [Y/N] 'Y' removes the local file post upload. 'N' moves the file to GDrive download folder
post upload.
    (Default is 'N')
- Share_Link: [Y/N] 'Y' puts the shareable link of the file uploaded in share.txt in Up_Directory.
    (Default is 'Y')
- Write_Permission: [Y/N] 'Y' gives the write permission in the sharable link.
    (Default is 'N')

Configuration is stored in config.json as a dictionary which can be manually edited as well.

* -ls [local/remote]

Lists all files and folders in your GDrive (default or when "remote" used).
Lists all files and folders in your downloads directory (when "local" used).

* -ls_trash

Lists all files and folders in your GDrive trash.

* -ls_folder [folder_id]

Lists files and folders in the given folder id in your drive.

* -ls_files [folder_id/"root"]

Lists all files recursively present in the folder id given.

* -download [file_id1] [file_id2]

Downloads the given file from GDrive. Multiple files can be downloaded by putting file_ids one after the other.
Use "-d all" argument to download entire your entire GDrive.

* -upload [file_add]

Upload file/folder corresponding to the address given to GDrive, for one time.

* -share [file_id]

Outputs the shareable link of the file.

* -remove [local/remote] [file_name/folder_name/file_id/folder_id]

Delete the mentioned file from GDrive download directory or GDrive remote. Please input file_id/folder_id if it's a
remote file. You can add multiple file_ids/folder_ids one after the other, e.g. -remove remote [file_id1] [file_id2]

* -open [upload/download]

Opens the upload or download directory in file explorer.

## Contributing

Contributions to this project are highly encouraged. We will soon be having a contribution guide.<br/>
To begin, please have a look at the issues. They are simple and easy to implement/resolve.
