#!/usr/bin/env python
#-*- coding:utf-8 -*-

import psycopg2
from ReadIni import ReadIni





class ConnSql :
    filename = "ip.ini"
    readIni = ReadIni(filename)
    conn = None

    def __init__(self,pro_name):
        self.pro_name = pro_name

    def getConn(self):
        # conn = None
        dbbase = self.readIni.getValue(self.pro_name,"dbname")
        dbuser = self.readIni.getValue(self.pro_name,"username")
        dbpassword = self.readIni.getValue(self.pro_name,"password")
        dbhost = self.readIni.getValue(self.pro_name,"dbhost")
        dbport = self.readIni.getValue(self.pro_name,"dbport")

        try :
            self.conn = psycopg2.connect(database=dbbase,user=dbuser,password=dbpassword,host=dbhost,port=dbport)

            print "数据库连接成功"

        except Exception ,e :
            print e

        return self.conn


    def getCursor(self,sql) :
        cursor = self.getConn().cursor()
        try :
            cursor.execute(sql)
        except Exception ,e :
            print e
            print "查询信息失败"
        return cursor





if __name__ == "__main__" :
    connSql = ConnSql("GS")
    sql = "select * from game "

    cur = connSql.getCursor(sql)
    for value in cur.fetchall() :
        print value[0]




