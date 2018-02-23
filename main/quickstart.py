#!/usr/bin/env python 

''' all important imports go below'''

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

first_file = drive.CreateFile({'title': 'Hello.txt'}) # create google drive file instance with name "Hello.txt"
first_file.SetContentString('Hello World!') # set content of the file to string given in argument
first_file.Upload()
