#!/usr/bin/env python 
#-*- coding:utf-8 -*- 

import os
import sys
import re

reload(sys)

sys.setdefaultencoding("utf-8")
filename = "mySearch.log"
all_line = []
if not os.path.exists(filename) :
    print u"文件不存在，请检查" 
    System.exit(0)
else :
    try :
        pass_count = 0
        error_count = 0 
        error_str = ""
        file = open(filename,'r')
        for line in file.readlines():
          
            if "877805" in line and not ":877805" in line :
                print "test"  
                if not "0," in line and ',' in line:
                    each_line_in = line.split(",")
                    check = True 
                    check01 =  each_line_in[0].split(":")
                    check02 =  each_line_in[1].split(";")[0].split(":")
                    
                    if len(check01) != len(check02) :
                        check = False 
                    else :
                        for i in range(1,len(check01)) :
                            if check01[i] != check02[i] :
                                error_str = check01[i] + "\n" + check02[i] + "\n"
                                check = False 
                                break 
                    if check :
                        print line + "\t" + "pass"
                        pass_count += 1 
                    else :
                        print line + "\t" + "error"
                        error_count += 1
                        error_str += line + "\n"
                elif "0," in line :
                    if len(line.split("0,")[1]) == 35 :
                        print line + "\t" + "pass" 
                        pass_count += 1 
                    else :
                        print line + "\t" + "error"
                        error_count += 1
                        error_str += line + "\n"
        print "\n"
        print u"本次检索结果："
        print u"\t通过数："+str(pass_count )
        print u"\t不通过数：" + str(error_count)
        print error_str 
        
        file.close()
    except Exception ,e :
        print e 
