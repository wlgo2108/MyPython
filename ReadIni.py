#!/usr/bin/env python
#-*- coding:utf-8 -*-

import  ConfigParser
import os
import sys
import logging

class ReadIni :
    #配置参数相关的文件名
    filename = "ip.ini"

    def __init__(self,filename) :
        self.filename = filename


    def getValue(self,sect,key) :
        conf = ConfigParser.ConfigParser()
        conf.read(self.filename)
        sec = conf.sections()
        option = conf.options(sect)
        value = conf.get(sect,key)
        return value



if __name__ == "__main__" :
    readIni = ReadIni("ip.ini")
    value = readIni.getValue(u"SC","ip")
    print value


