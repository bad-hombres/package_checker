import sys
import os
import shutil
import subprocess


def package_download(package_name):
    # Check Folder is exists 
        if not os.path.exists("/root/packages-download"):
            os.mkdir("/root/packages-download")
        else:
             subprocess.Popen(['/usr/bin/yum', 'install', '--downloadonly', '--downloaddir=/root/packages-download', package_name])

def main():
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
  
    with open(filepath) as fp:
        for line in fp:
            print("Downloading package with name {}".format(line))
            t = package_download(line)

if __name__ == '__main__':
    main()

