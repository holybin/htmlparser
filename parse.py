#-*- coding:utf-8 -*-
'''
@date: March,1,2014

@author: holybin

@description: Module 2 - parse search result page to get url and download html pages
'''

#######################Module 2##################################
import urllib2
import sys
import os
import re
import bs4
import chardet

reload(sys)
sys.setdefaultencoding('utf-8')

def download(urlinfo,region,search,count):
    company = (search.split('+'))[0]
    htmlfilename = region+os.sep+company+os.sep+search+'_'+str(count)+'.html'
    htmlfile = open(htmlfilename,'w')

    try:
        result = urllib2.urlopen(urlinfo)
        content = result.read()
        info = result.info()
        result.close()

        print '::download No. %d page ok'%count
    except Exception,e:
        print '::download No. %d page error!!!'%count
        print e
    else:
        
        if content != None:
            charset1 = (chardet.detect(content))['encoding'] #get real encoding type
            charset2 = info.getparam('charset') #get declared encoding type
            
            print charset1,' ', charset2
            try:
                # case1: all the charset is not None.
                if charset1 != None and charset2 != None:
                    #charset is different
                    if charset1.lower() != charset2.lower():
                        newcont = bs4.BeautifulSoup(content, from_encoding='GB18030')
                    #charset is the same
                    else:
                        newcont = bs4.BeautifulSoup(content, from_encoding=charset1)
                    #write to file
                    for cont in newcont:
                        htmlfile.write('%s\n'%cont)
                
                # case2: either charset is None.
                else:
                    if charset1 != None and charset2 == None:
                        _charset = charset1
                    elif charset1 == None and charset2 != None:
                        _charset = charset2
                    else:
                        _charset = sys.getdefaultencoding()
                    #write to file
                    newcont = bs4.BeautifulSoup(content, from_encoding=_charset)
                    for cont in newcont:
                        htmlfile.write('%s\n'%cont)
            except Exception,e:
                print e, 'parsing error!!!'
                    
    htmlfile.close()

def startparse(region, company, keyword):
    print '\nModule 2 - parse search result page to get url and download html pages.'

    searchkey = '%s+%s'%(company,keyword)
    
    #file for saving search results
    resfilename = region+os.sep+company+os.sep+'%s.html'%searchkey
    resfile = open(resfilename,'r')
    rescont = resfile.read()
    resfile.close()

    #file for saving parsing results
    txtfilename = region+os.sep+company+os.sep+'%s_result.txt'%searchkey
    txtfile = open(txtfilename,'r')
    txtcont = txtfile.readlines()
    txtfile.close()

    #use re to find urls and titles
    #<div class="sa_cc"
    pattern1 = '<div.*?class="sa_cc".*?>(.*?)</div>'
    pattern2 = '.*?<h3><a.*?href="(.*?)".*?>(.*?)</a></h3>'
    _rescont = re.findall(pattern1,rescont,re.S | re.I)   #re.S: replace("\n","")
    
    txtlist = []
    count = 0
    for res in _rescont:
        #get urls and titles
        items = re.search(pattern2, res, re.S | re.I)
        urlinfo = items.group(1)
        #titleinfo = items.group(2).replace('<strong>','').replace('</strong>','')

        txtlist.append(urlinfo)
        
        #download html pages
        count = count + 1
        download(urlinfo,region,searchkey,count)

    #write back to parsing result file
    for i in range(len(txtcont)):
        newcont = '*'+txtlist[i]+'\n'
        oldcont = txtcont[i]
        txtcont[i] = oldcont.replace('\n', newcont)
    txtfile = open(txtfilename,'w')
    txtfile.writelines(txtcont)
    txtfile.close()

    #return number of html pages downloaded
    return count
