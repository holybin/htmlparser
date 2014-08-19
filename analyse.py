#-*- coding:utf-8 -*-
'''
@date: March,1,2014

@author: holybin

@description: Module 3 - analyse html pages to judge keyword related or not
'''

#######################Module 3##################################
import sys
import os
import re
from readability.readability import Document

reload(sys)
sys.setdefaultencoding('utf-8')

def startanalyse(region, company, keyword, count):
    print '\nModule 3 - analyse html pages to judge keyword related or not.'

    searchkey = '%s+%s'%(company,keyword)

    #file for saving analyzing results
    txtfilename = region+os.sep+company+os.sep+'%s_result.txt'%searchkey
    txtfile = open(txtfilename,'r')
    txtcont = txtfile.readlines()
    txtfile.close()

    #meta html page file name
    _htmlfilename = region+os.sep+company+os.sep+searchkey+'_%d.html'

    yes = 0
    no = 0

    #pattern: description, keywords, title
    pattern_title = '<title>(.*?)</title>'
    pattern_key = '<meta\s(name=["]?keywords["]?\scontent=\"(.*?)\"|content=\"(.*?)\"\sname=["]?keywords["]?).*?>'   #.*?>: not always end symbol & space character
    pattern_des = '<meta\s(name=["]?description["]?\scontent=\"(.*?)\"|content=\"(.*?)\"\sname=["]?description["]?).*?>'   #.*?>: not always end symbol & space character

    txtlist = []
    tmpfilename = 'tmp.txt' #temp usage
    for i in range(count):
        tmp = i + 1
        htmlfilename = _htmlfilename%tmp

        company_flag = False
        keyword_flag = False
            
        #judge html file is NULL or not
        file_size = os.stat(htmlfilename).st_size
        
        if file_size != 0:
            htmlfile = open(htmlfilename, 'r')
            htmlcontent = htmlfile.read()
            htmlfile.close()

            #1 - head content: description, keywords, title
            head_title = re.search(pattern_title,htmlcontent,re.I | re.S)
            head_key = re.search(pattern_key,htmlcontent,re.I | re.S)
            head_des = re.search(pattern_des,htmlcontent,re.I | re.S)
            #2 - body content: readability
            body_content = Document(htmlcontent).summary()
            tmpfile = open(tmpfilename,'w')
            tmpfile.write(body_content.encode('utf-8'))
            tmpfile.close()
            tmpfile = open(tmpfilename,'r')
            body_content = tmpfile.read()
            tmpfile.close()

            #is company related or not?
            if (head_title!=None and (company in head_title.group(1))) or (head_key!=None and (company in head_key.group(1))) or (head_des!=None and (company in head_des.group(1))):
                company_flag = True
            else:
                _company = unicode(company,'mbcs')
                if _company in body_content:
                    company_flag = True
            #if company not, stop judging
            if company_flag:
                #is keyword related or not?
                if (head_title!=None and (keyword in head_title.group(1))) or (head_key!=None and (keyword in head_key.group(1))) or (head_des!=None and (keyword in head_des.group(1))):
                    keyword_flag = True
                else:
                    _keyword = unicode(keyword, 'mbcs')
                    if _keyword in body_content:
                        keyword_flag = True
        #show results
        print tmp,' company related:',company_flag,' keyword related:',keyword_flag
    
        #store results
        if company_flag and keyword_flag:
            txtlist.append('yes')
        else:
            txtlist.append('no')
        i += 1

    #write back to analyzing result file
    for j in range(len(txtcont)):
        newcont = '*'+txtlist[j]+'\n'
        oldcont = txtcont[j]
        txtcont[j] = oldcont.replace('\n', newcont)
    txtfile = open(txtfilename,'w')
    txtfile.writelines(txtcont)
    txtfile.close()

    if os.path.exists(tmpfilename)==True:
        os.remove(tmpfilename)
