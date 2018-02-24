GDrive_Sync by thealphadollar
Github @thealphadollar
mailto thealphadollar@iitkgp.ac.in

GDrive_Sync aims at making life simpler when switching from Windows to Linux

This was developed with the aim to create a free and open source GDrive client to make things simpler and users won't
need to switch to other cloud file storing platforms or have to pay for commercial clients doing the same.

The parameters that can be used are:

* -init :

Initiate GDrive_Sync for the first time and give it the read and write permissions to your Google Drive.

* -version :

Shows the current version of the GDrive_Sync.

* -config :

Gives option to edit the configuration file on which automatic upload and download works.
- Up_Directory:   The directory where the files that are to be uploaded are given.
- Down_Directory: The directory where the files are downloaded.
- Down_All: Accepts Y or N; Y downloads all files in your file to local.
- Share_Link: Accepts Y or N; Y puts the shareable link of the file in share.txt in Up_Directory

Configuration is stored in config.json as a dictionary which can be manually edited as well.

* -download [file_name] :

Downloads the given file from GDrive.

* -upload [file_add]

Upload file corresponding to the address given to GDrive.

* -share [file_name]

Outputs the shareable link of the file.