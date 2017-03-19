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
        self.level = 1
        self.root_folder = os.getcwd()

    def parse(self, response):
        
        print "self.level begin= ", self.level

        url_list = response.xpath('//a/@href').extract()

        print url_list

        for i, url in enumerate(url_list):

            absoluteSrc = 'http://www.3gpp.org' + url
            level1_folder = ''.join(re.findall(r'\d+_series', url))
            level2_folder = ''.join(re.findall(r'\d+\.\d[a-zA-Z0-9]{1,2}', url))
            fileName = ''.join(re.findall(r'[^\\/:*?"<>|\r\n]+$', url))

            print "absoluteSrc = ", absoluteSrc
            print "level1_folder = ", level1_folder
            print "level2_folder = ", level2_folder
            print "fileName = ", fileName

            XgppSpider.download.ask_current_dir()

            if i == 0:
                print 'skip current path :', absoluteSrc
                continue
            
            if fileName is "":
                yield scrapy.Request(url=absoluteSrc, callback=self.parse)

                if level1_folder: 
                    level1_path = os.path.join(self.root_folder, level1_folder)
                    XgppSpider.download.goto_dir(level1_path, XgppSpider.config.is_latest_mode())

                if level2_folder: 
                    level2_path = os.path.join(self.root_folder, level1_folder, level2_folder)
                    XgppSpider.download.goto_dir(level2_path, XgppSpider.config.is_latest_mode())
            else:
                shouldDownload = False
                if XgppSpider.config.is_latest_mode():
                    if i is len(url_list)-1 :
                        shouldDownload = True
                else:
                    shouldDownload = True
                    
                if shouldDownload:
                    path = os.path.join(self.root_folder, level1_folder, level2_folder)
                    XgppSpider.download.goto_dir(path, XgppSpider.config.is_latest_mode())
                    XgppSpider.download.get_file(absoluteSrc, fileName, XgppSpider.config.is_un_zip())
            

