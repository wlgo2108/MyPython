#!/usr/bin/env python
#-*- coding:utf-8 -*-

# import psycopg2
import MySQLdb
from ReadIni import ReadIni
# from psycopg2.tests.testconfig import dbpass





class ConnSql :
    filename = "ip.ini"
    readIni = ReadIni(filename)
    conn = None

    def __init__(self,pro_name=""):
        self.pro_name = pro_name

    def getConn(self):
        # conn = None
        dbbase = "db_search"
        dbuser = "root"
        dbpassword = "123456"
        dbhost = "localhost"
        dbport = 3306

        try :
            self.conn = MySQLdb.connect(host=dbhost,user=dbuser,passwd=dbpassword,db=dbbase,port=dbport)
#             self.conn = psycopg2.connect(database=dbbase,user=dbuser,password=dbpassword,host=dbhost,port=dbport)

#             print "数据库连接成功"

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
    
    def updateSQL(self,sql) :
        cursor = self.getConn().cursor()
        try :
            cursor.execute(sql) 
            self.conn.commit() 
        except :
            return  "数据更新失败" 
            self.conn.rollback()
        return "数据更新成功"
    
    def closeConn(self):
        try :
            if self.conn != None :
                self.conn.close()
        except :
            return  "conn调用close()失败" 
        return "conn调用close()成功"





if __name__ == "__main__" :
    connSql = ConnSql("SC")
#     sql = "update tb_game,tb_proinfo set tb_game.game_issue = '%d' where tb_game.pro_id = tb_proinfo.pro_id and tb_proinfo.pro_name = '%s' and tb_game.game_name = '%s'  "%(2015143,"SC","B001")
#     print connSql.updateSQL(sql)
    sql = "select * from tb_game  where game_name = '%s'"%("Q730")
#     sql = "select server_port from tb_game,tb_proinfo where tb_game.pro_id = tb_proinfo.pro_id and tb_proinfo.pro_name = '%s' and tb_game.game_name = '%s'  "%("SC","QL730")
    cur = connSql.getCursor(sql)
    for value in cur.fetchall() :
        print value[0]




