import zipfile
import os
import shutil
import boto3
from tkinter import Tk
from tkinter.filedialog import askdirectory
import paramiko

root = Tk()
root.withdraw()

folder_path = askdirectory(title="Choose source folder want deploy:")

print(folder_path)

if not folder_path:
    print("Wasn't choose folder.")
    exit()


file_paths = [
    folder_path+"/i18n.config.js",
    folder_path+"/package.json",
    folder_path+"/build",
    folder_path+"/next-image-loader.js",
    folder_path+"/payload.config.ts",
    folder_path+"/tailwind.config.js",
    folder_path+"/dist",
    folder_path+"/next.config.js",
    folder_path+"/.next",
    folder_path+"/yarn-error.log",
    folder_path+"/share",
    folder_path+"/yarn.lock",
]

zip_file_path = "archive.zip"

if os.path.exists(zip_file_path):
    os.remove(zip_file_path)
    print("Đã xóa file zip cũ.")

with zipfile.ZipFile(zip_file_path, 'w') as zipf:
    for path in file_paths:
        if os.path.isfile(path):
            zipf.write(path, os.path.basename(path))
        elif os.path.isdir(path):
            for foldername, subfolders, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    zip_file_path = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, zip_file_path)

# Thông tin kết nối SSH
host = 'ec2-13-229-222-13.ap-southeast-1.compute.amazonaws.com'
port = 22
username = 'ubuntu'
private_key_path = 'techJDIProduction.pem'

remote_file_path = '/server/'
unzip_file_name = 'archive.zip'

ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(host, port, username, key_filename=private_key_path)

sftp = ssh.open_sftp()

sftp.put(zip_file_path, remote_file_path)

sftp.close()

ssh.close()

os.system(f'unzip {zip_file_path}.zip -d {remote_file_path}/{unzip_file_name}')

os.system('pm2 restart all')