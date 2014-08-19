#-*- coding:utf-8 -*-

import download
import parse
import analyse
import statistics

import os
import sys
import socket
import time

#set default coding type: utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

#socket timeout
socket.setdefaulttimeout(20)

#meta-search url
BING = "http://cn.bing.com/search?q=%s&qs=n&sc=8-3&sp=-1&sk=&first=%d"

#+++++++++++Specify SH or SZ+++++++++++#
region = 'SH'
#++++++++++Adjust Html Number++++++++++#
pagenum = 5  #totalnumber = 10 * pagenum
#++++++++++++++++++++++++++++++++++++++#

#create diretory for saving region results
if os.path.exists(region)==False:
    os.mkdir(region)

#read keywords file
infile = open('./%s.txt'%region,'r')
count_key = 1

for line in infile:
    line = line.strip()     #delete SPACE at left&right of keywords
    items = line.split()    #split line by SPACE character
    company = items[0]
    keyword = items[1]

    print '\n********* NO. %d - company: %s, keyword: %s *********\n'%(count_key, company, keyword)
    
    #create diretory for saving SEARCH results
    company_path = region+os.sep+company
    if os.path.exists(company_path)==False:
        os.mkdir(company_path)

    #Module1: download result pages of search engine
    download.startdownload(region, company, keyword, BING, pagenum)

    #Module2: parse search result page to get url and download html pages
    count = parse.startparse(region, company, keyword)

    #count = 50

    #Module3: analyse html pages to judge keyword related or not
    analyse.startanalyse(region, company, keyword, count)

    #Module4: statistics results to get final data
    statistics.startstatistics(region, company)
    
    count_key += 1
    
infile.close()
