# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import os
from config import XgppConfig
from download import XgppDownload

class XgppSpider(scrapy.Spider):
    
    name = "xgpp"
    allowed_domains = ['www.3gpp.org']
    start_urls = []

    config = XgppConfig()
    start_urls = config.start_urls

    download = XgppDownload()

    def __init__(self):
        self.level = 0
        self.root_folder = os.getcwd()
        self.latest_file_name = ""
        self.latest_file_url = ""

    def download_file(self, dir, absoluteSrc, fileName):
        print dir, ',', absoluteSrc, ',', fileName
        XgppSpider.download.goto_dir(dir, XgppSpider.config.is_latest_mode())
        XgppSpider.download.get_file(absoluteSrc, fileName, XgppSpider.config.is_un_zip())


    def parse(self, response):
        
        print "self.level begin= ", self.level

        url_list = response.xpath('//a/@href').extract()
        self.latest_file_name = ""
        self.latest_file_url = ""


        print url_list

        for i, url in enumerate(url_list):

            absolute_src = 'http://www.3gpp.org' + url
            level1_folder = ''.join(re.findall(r'\d+_series', url))
            level2_folder = ''.join(re.findall(r'\d+\.\d[a-zA-Z0-9]{1,2}', url))
            fileName = ''.join(re.findall(r'[^\\/:*?"<>|\r\n]+$', url))

            print "absolute_src = ", absolute_src
            print "level1_folder = ", level1_folder
            print "level2_folder = ", level2_folder
            print "fileName = ", fileName
            print 'last_file_name = ', self.latest_file_name

            XgppSpider.download.ask_current_dir()

            if i == 0:
                print 'skip current path :', absolute_src
                continue
            
            if fileName is "":
                if self.latest_file_name:
                    print 'should not dig inside ', self.level
                    path = os.path.join(self.root_folder, level1_folder, level2_folder)
                    print path, ',', self.latest_file_url, ',', self.latest_file_name
                    self.download_file(path, self.latest_file_url, self.latest_file_name)
                    return

                print 'should dig inside ', self.level
                yield scrapy.Request(url=absolute_src, callback=self.parse)

                if level1_folder: 
                    level1_path = os.path.join(self.root_folder, level1_folder)
                    XgppSpider.download.goto_dir(level1_path, XgppSpider.config.is_latest_mode())

                if level2_folder: 
                    level2_path = os.path.join(self.root_folder, level1_folder, level2_folder)
                    XgppSpider.download.goto_dir(level2_path, XgppSpider.config.is_latest_mode())
            
            else:
                shouldDownload = False
                
                if XgppSpider.config.is_latest_mode():
                    if fileName > self.latest_file_name:
                        print 'update fileName from ', self.latest_file_name, ' to ', fileName
                        self.latest_file_name = fileName
                        self.latest_file_url = absolute_src         
                else:
                    shouldDownload = True

                if i is len(url_list)-1 :
                    print 'last file is', self.latest_file_name, i 
                    shouldDownload = True
                    
                if shouldDownload:
                    path = os.path.join(self.root_folder, level1_folder, level2_folder)
                    print 'ready to download', path, absolute_src, self.latest_file_name
                    self.download_file(path, absolute_src, self.latest_file_name)

  

