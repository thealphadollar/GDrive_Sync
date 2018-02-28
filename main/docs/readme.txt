GDrive_Sync by thealphadollar
Github @thealphadollar
mailto thealphadollar@iitkgp.ac.in

----------------------------------------------------------------------------

GDrive_Sync aims at making life simpler when switching from Windows to Linux

This was developed with the aim to create a free and open source GDrive client to make things simpler and users won't
need to switch to other cloud file storing platforms or have to pay for commercial clients doing the same.

The parameters that can be used are:

* -init :

Initiate GDrive_Sync and give it the read and write permissions to your Google Drive. Automatically executed at the
first run of GDrive_Sync.

* -version :

Shows the current version of the GDrive_Sync.

* -config :

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
- Down_All: [Y/N] 'Y' downloads all files in your drive to local.
    (Default is 'N')
- Share_Link: [Y/N] 'Y' puts the shareable link of the file uploaded in share.txt in Up_Directory.
    (Default is 'Y')
- Write_Permission: [Y/N] 'Y' gives the write permission in the sharable link.
    (Default is 'N')

Configuration is stored in config.json as a dictionary which can be manually edited as well.

* -ls [local/remote] :

Lists all files and folders in your GDrive (default or when "remote" used).
Lists all files and folders in your downloads directory (when "local" used).

* -ls_trash

Lists all files and folders in your GDrive trash.

* -ls_folder [folder_id]:

Lists files and folders in the given folder id in your drive.

* -ls_files [folder_id/"root"]:

Lists all files recursively present in the folder id given.

* -download [file_id] :

Downloads the given file from GDrive.

* -upload [file_add] :

Upload file/folder corresponding to the address given to GDrive, for one time.

* -share [file_id] :

Outputs the shareable link of the file.

* -remove [local/remote] [file_name/folder_name/file_id/folder_id] :

Delete the mentioned file from GDrive download directory or GDrive remote. Please input file_id/folder_id if it's a
remote file. You can add multiple file_ids/folder_ids one after the other, e.g. -remove remote [file_id1] [file_id2]

* -open [upload/download]

Opens the upload or download directory in file explorer.