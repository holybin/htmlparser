#-*- coding:utf-8 -*-
'''
@date: March,1,2014

@author: holybin

@description: Module 4 - statistics results to get final data
'''

#######################Module 4##################################
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

def statisticsbydate(time_set):
    #analyse: 2012 and 4 seasons of 2013
    time_map = {}
        
    time_map['2013-1']=0
    time_map['2013-2']=0
    time_map['2013-3']=0
    time_map['2013-4']=0

    for time in time_set:
        times = time.split('-')
        year = times[0]
        month = int(times[1])
        #not 2013
        if year!='2013':
            if year in time_map:
                time_map[year] = time_map[year] + 1
            else:
                time_map[year] = 1
        #2013: 4 seasons
        else:
            if month<=3:
                time_map['2013-1'] = time_map['2013-1']+1
            elif month>=4 and month<=6:
                time_map['2013-2'] = time_map['2013-2']+1
            elif month>=7 and month<=9:
                time_map['2013-3'] = time_map['2013-3']+1
            else:
                time_map['2013-4'] = time_map['2013-4']+1
    #return
    return time_map

def startstatistics(region, company):
    print '\nModule 4 - statistics results to get final data.'
    startdir = '.'+os.sep+region+os.sep+company

    #get result files
    keyfiles = []
    for dirpath, dirnames, filenames in os.walk(startdir):
        flag = False
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.txt':
                flag = True
                keyfilename = startdir+os.sep+filename
                keyfiles.append(keyfilename)
        if not flag:
            print 'Error: no results available!!!'

    #final data file
    resultfilename = '.\\%s\\%s.txt'%(region,company)
    resultfile = open(resultfilename,'w')
    
    total_time_set = set([])
    total_keyword = ''
    for keyfilename in keyfiles:
        keyfile = open(keyfilename, 'r')
        keyfilecont = keyfile.readlines()
        keyfile.close()

        #repetition removal: use set to summarize date of 'yes' item
        time_set = set([])
        for cont in keyfilecont:
            cont = cont.rstrip('\n')    #remove '\n' on the right
            conts = cont.split('*')
            time = conts[1]
            label = conts[3]
            #if 'yes', add to set
            if label=='yes':
                time_set.add(time)

        #get union set for summary
        total_time_set = total_time_set | time_set
        #get keyword
        keyword = keyfilename.split('+')[1].split('_')[0]
        #get total keyword for summary
        total_keyword = total_keyword+keyword+' '
        print keyword
        
        #statistics by date
        time_map = statisticsbydate(time_set)

        #write results of each keyword to file
        resultfile.write(keyword+'\n')
        #sorting by date
        sort_keys = time_map.keys()
        sort_keys.sort()
        for key in sort_keys:
            resultfile.write(key+':'+str(time_map[key])+'\n')
        resultfile.write('\n')

    print total_keyword
    
    #statistics by date
    total_time_map = statisticsbydate(total_time_set)
    
    #write results of all keywords to file
    resultfile.write(total_keyword+'\n')
    #sorting by date
    sort_keys = total_time_map.keys()
    sort_keys.sort()
    for key in sort_keys:
        resultfile.write(key+':'+str(total_time_map[key])+'\n')
    resultfile.write('\n')

    resultfile.close()
    print resultfilename,' saved ok!'
    



    
