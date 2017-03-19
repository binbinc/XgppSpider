# -*- coding: utf-8 -*-

# Load xgpp configurations
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import ConfigParser

class XgppConfig():
    
    start_urls = [
        #'http://www.3gpp.org/ftp/Specs/archive/36_series/36.331/'
        #'http://www.3gpp.org/ftp/Specs/archive/00_series/00.01U/',
        #'http://www.3gpp.org/ftp/Specs/archive/01_series/01.02/'
    ]

    conf = ConfigParser.ConfigParser()
    conf.read(r'config.ini')

    download_mode = conf.get('global', 'download_mode')
    un_zip = conf.get('global', 'un_zip')

    print 'download_mode = ', download_mode
    print 'un_zip = ', un_zip

    for i, url in enumerate(conf.items('xgpp')):
        start_urls.append(url[1])
        print start_urls[i]

    def is_un_zip(self):
        return XgppConfig.un_zip == "on"

    def is_latest_mode(self):
        return XgppConfig.download_mode == "latest"
