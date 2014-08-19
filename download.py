#-*- coding:utf-8 -*-
'''
@date: March,1,2014

@author: holybin

@description: Module 1 - download result pages of search engine
'''

#######################Module 1##################################
import urllib2
import sys
import os
import re
import bs4
from time import localtime, strftime

reload(sys)
sys.setdefaultencoding('utf-8')

def startdownload(region, company, keyword, BING, pagenum):
    print 'Module 1 - download result pages of search engine.'

    #search result file
    search = '%s+%s'%(company,keyword)
    filename = region+os.sep+company+os.sep+'%s.html'%search    #os.sep=os.path.sep,split character of system(win32:\\, linux: /)

    #file for saving parsing results
    txtfilename = region+os.sep+company+os.sep+'%s_result.txt'%search
    
    #open file and write contents
    outfile = open(filename,'w')
    txtfile = open(txtfilename,'w')
    count = 0

    #re pattern for getting time
    pattern = '<div class="sb_meta">.*?</span></span>(.*?)</div></div></div>'  #two </span> because bs4 parsing

    #re pattern for transfering time
    pattern_day = u'天前'
    pattern_hour = u'小时前'
    for i in range(pagenum):  #the first N items: N = 10items/page * pagenum
        url = BING %(search,i*10 + 1)
        url = unicode(url, 'mbcs')  #unicode coding
        print url
        try:
            #time.sleep(5)
            result = urllib2.urlopen(url)
            content = result.read()
            result.close()

            if content != None:
                local_time = localtime()
                Y = int(strftime("%Y",local_time))
                m = int(strftime("%m",local_time))
                d = int(strftime("%d",local_time))
                    
                #save result
                outfile.write(content)  #default coding: UTF-8
                
                #save time
                bs_res = bs4.BeautifulSoup(content)
                find_res = bs_res.findAll('div', {"class":"sa_cc"})
                for j in range(len(find_res)):
                    dd = d
                    count = count + 1       
                    time = re.search(pattern, str(find_res[j]), re.S | re.I)
                    #adjust time: YYYY-MM-DD
                    if time == None:
                        time = str(Y)+'-'+str(m)+'-'+str(dd)
                    else:
                        time = unicode(time.group(1),'utf-8')
			if(time.rfind(pattern_day)!=-1):
                            dd = dd - int(time.split()[0])
                            time = str(Y)+'-'+str(m)+'-'+str(dd)
			elif(time.rfind(pattern_hour)!=-1):
                            time = str(Y)+'-'+str(m)+'-'+str(dd)
			#else:
                            #normal case
                    txtfile.write(str(count)+'*'+time+'\n')

            print '::Download page %d ok'%(i+1)
        except Exception,e:
            print e,'::Download page %d error !!!'%(i+1)

    outfile.close()
    txtfile.close()
