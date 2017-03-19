# -*- coding: utf-8 -*-

# Load xgpp configurations
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import os
import urllib
import zipfile

class XgppDownload():
    
    root_folder = "xgppdownload"

    if not os.path.exists(root_folder):
        os.mkdir(root_folder)
    os.chdir(root_folder)


    def ask_current_dir(self):
        path = os.getcwd()
        print 'current path: ', path

    def goto_dir(self, dir, latest):
        print 'goto_dir: from--> ', os.getcwd()
        print 'goto_dir: to  --> ', dir

        if latest or dir is "":
            print 'goto_dir: do nothing'
            return

        if not os.path.exists(dir):
            os.makedirs(dir)
        os.chdir(dir)
        print 'goto_dir: now--> ', dir


    def get_file(self, absoluteSrc, fileName, unZip):
        print 'absoluteSrc:', absoluteSrc
        print 'fileName:', fileName
        urllib.urlretrieve(absoluteSrc, fileName)

        if unZip and zipfile.is_zipfile(fileName):
            zipFile = zipfile.ZipFile(fileName, 'r')
            for file in zipFile.namelist():
                zipFile.extract(file)
            zipFile.close()



