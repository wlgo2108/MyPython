#!/usr/bin/env python
#-*- coding:utf-8 -*-

from OpenExcel import OpenExcel
from ConnSql import ConnSql 
from ConnSocket import doSocket
import sys
import datetime
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='mySearch.log',
                filemode='w')



reload(sys)
sys.setdefaultencoding("utf-8")

str_log = ""
log_in = []

class toSearch :
    def __init__(self,pro_code,game_name,tsn=0,wager_issue=0,station_id=0,cz_type=1):
        self.pro_code = pro_code
        self.game_name = game_name
        self.tsn = tsn
        self.wager_issue = wager_issue
        self.station_id = station_id
        self.cz_type = cz_type
        self.connSQL = ConnSql()
        
    def getGameID(self):
        game_id = 0 
        sql = "select game_id from tb_game,tb_proinfo where tb_game.pro_id = tb_proinfo.pro_id and tb_proinfo.pro_name = '%s' and tb_game.game_name = '%s'  "%(self.pro_code,self.game_name)
        cur = self.connSQL.getCursor(sql)
        for value in cur.fetchall() :
            game_id =  value[0]
        return game_id
    
    #获取游戏期号
    def getWagerIssue(self):
        wager_issue = self.wager_issue
        if wager_issue == 0 :
            sql = "select game_issue from tb_game,tb_proinfo where tb_game.pro_id = tb_proinfo.pro_id and tb_proinfo.pro_name = '%s' and tb_game.game_name = '%s'  "%(self.pro_code,self.game_name)
            cur = self.connSQL.getCursor(sql)
            for value in cur.fetchall() :
                wager_issue =  value[0]
        else :
            sql = "update tb_game,tb_proinfo set tb_game.game_issue = '%d' where tb_game.pro_id = tb_proinfo.pro_id and tb_proinfo.pro_name = '%s' and tb_game.game_name = '%s'  "%(self.wager_issue,self.pro_code,self.game_name)
            #print "期号更新"+self.connSQL.updateSQL(sql)
        return wager_issue
    
    #获取站点编号
    def getStationId(self):
        station_id = self.station_id
        if station_id == 0 :
            sql = "select station_id from tb_game,tb_proinfo where tb_game.pro_id = tb_proinfo.pro_id and tb_proinfo.pro_name = '%s' and tb_game.game_name = '%s'  "%(self.pro_code,self.game_name)
            cur = self.connSQL.getCursor(sql)
            for value in cur.fetchall() :
                station_id =  value[0]
        else :
            sql = "update tb_game,tb_proinfo set tb_game.station_id = '%d' where tb_game.pro_id = tb_proinfo.pro_id and tb_proinfo.pro_name = '%s' and tb_game.game_name = '%s'  "%(self.station_id,self.pro_code,self.game_name)
            #print "站点更新"+self.connSQL.updateSQL(sql)
        return station_id
    
    def getFileName(self):
        filename = ""
        if filename == "" :
            sql = "select file_name from tb_game,tb_proinfo where tb_game.pro_id = tb_proinfo.pro_id and tb_proinfo.pro_name = '%s' and tb_game.game_name = '%s'  "%(self.pro_code,self.game_name)
            cur = self.connSQL.getCursor(sql)
            for value in cur.fetchall() :
                filename =  value[0]
        return filename
    
    def getSheetName(self):
        sheetname = ""
        if sheetname == "" :
            sql = "select sheet_name from tb_game,tb_proinfo where tb_game.pro_id = tb_proinfo.pro_id and tb_proinfo.pro_name = '%s' and tb_game.game_name = '%s'  "%(self.pro_code,self.game_name)
            cur = self.connSQL.getCursor(sql)
            for value in cur.fetchall() :
                sheetname =  value[0]
        return sheetname
    
    #获取服务器ip
    def getServerIP(self):
        server_ip = ""
        if server_ip == "" :
            sql = "select server_ip from tb_game,tb_proinfo where tb_game.pro_id = tb_proinfo.pro_id and tb_proinfo.pro_name = '%s' and tb_game.game_name = '%s'  "%(self.pro_code,self.game_name)
            cur = self.connSQL.getCursor(sql)
            for value in cur.fetchall() :
                server_ip =  value[0]
        return server_ip
    
    #获取服务器端口
    def getServerPort(self):
        server_port = ""
        if server_port == "" :
            sql = "select server_port from tb_game,tb_proinfo where tb_game.pro_id = tb_proinfo.pro_id and tb_proinfo.pro_name = '%s' and tb_game.game_name = '%s'  "%(self.pro_code,self.game_name)
            cur = self.connSQL.getCursor(sql)
            for value in cur.fetchall() :
                server_port =  value[0]
#                 print server_port
        return server_port
            
    
    def checkTest(self) :
        HOST = self.getServerIP()
        print HOST
        PORT = int(self.getServerPort())
        print PORT
        ADDR = (HOST,PORT)
        
        
        openX = OpenExcel(file=self.getFileName(),by_name=self.getSheetName())
        print self.getSheetName() 
        table = openX.excel_table_byname()
        x = doSocket(ADDR)
        for i in range(0,len(table)) :
            if table[i]["PlayType"] == "" :
                return ""
            game_type = int(table[i]["PlayType"])
            wager_money = int(table[i]["WagerMoney"])
            num = table[i]["WagerNum"]
            bs = int(table[i]["BS"])
            result_num = table[i]["PreWinNum"]
            result_check = table[i]["PreWinResult"]
            qs = int(table[i]["QS"])
            new_num = num.split(";")
            lottery_num = str(len(new_num) - 1)
            for i in range(0, len(new_num) - 1):
                lottery_num = lottery_num + ";" + str(i + 1) + ";3;" + str(game_type) + ";" + str(bs) + ";" + new_num[i]
            
            tranCode = int(table[i]["TranCode"])
            station_id = int(table[i]["Station_Id"])
            station_cert = int(table[i]["Station_cert"])
            tsn = int(table[i]["TSN"])
            print tranCode 
            msg = ""
            #投注
            if tranCode == 103200 or tranCode == 101200 :
                msg = '%d;0;1;%d;1;%d;%d;%d;%s;%d;%d;;;;%s;;' % (tranCode,station_id, self.getGameID(), self.getWagerIssue(), tsn, wager_money, tsn - 1,qs, lottery_num)
            #冲正
            elif tranCode == 103999 or tranCode == 101999 :
                msg = "%d;0;1;%d;1;;%d;%d;%d;%d;;0;"%(tranCode,station_id,self.getGameID() ,self.getWagerIssue(),station_id,tsn)
            #注销
            elif tranCode == 103300 or tranCode == 101300 :
                msg = "%d;0;103;%d;1;;%d;%d;%d;%d;;%d;"%(tranCode,station_id,self.getGameID(),self.getWagerIssue(),station_id,tsn,station_cert)
            #兑奖
            elif tranCode == 103009 or tranCode == 101009 :
                msg = "%d;0;103;%d;1;;%d;%d;%d;%d;;%d;"%(tranCode,station_id,station_id,self.getWagerIssue() - 1,self.getGameID(),tsn,station_cert)
            print msg 
            ADDR = (HOST, PORT)
            str_log = 'trans Msg is :' + msg
            print str_log
            get_msg = x.ourSendMsg(str(msg))
            print get_msg
            if "999999" in get_msg:
                print "\a"
                break
            ADDR = (HOST, PORT)

            x = doSocket(ADDR)

        return u"操作完成,请及时查看日志!"
                

        
            
        

    
    #投注及检索
    def search(self):
        HOST = self.getServerIP()
        print HOST
        PORT = int(self.getServerPort())
        print PORT
        ADDR = (HOST,PORT)
        
        
        openX = OpenExcel(file=self.getFileName(),by_name=self.getSheetName())
        print self.getSheetName() 
        table = openX.excel_table_byname()
        
        x = doSocket(ADDR)
        for i in range(0,len(table)) :
        
            # stationID = stationID + 1

            self.tsn += 1
            if table[i]["PlayType"] == "" :
                return ""
            game_type = int(table[i]["PlayType"])
            wager_money = int(table[i]["WagerMoney"])
            num = table[i]["WagerNum"]
            bs = int(table[i]["BS"])
            result_num = table[i]["PreWinNum"]
            result_check = table[i]["PreWinResult"]
            qs = int(table[i]["QS"])
            new_num = num.split(";")
            lottery_num = str(len(new_num) - 1)
            print lottery_num 
            for i in range(0, len(new_num) - 1):
                lottery_num = lottery_num + ";" + str(i + 1) + ";3;" + str(game_type) + ";" + str(bs) + ";" + new_num[i]
            
            msg = '103200;0;1;%d;1;%d;%d;%d;%s;%d;%d;;;;%s;;' % (self.getStationId(), self.getGameID(), self.getWagerIssue(), self.tsn, wager_money, self.tsn - 1,qs, lottery_num)
            #logging.info(msg)
            ADDR = (HOST, PORT)
            str_log = 'trans Msg is :' + msg
            print str_log
            get_msg = x.ourSendMsg(str(msg))
            print get_msg
            #logging.info(get_msg)
            if "999999" in get_msg:
                print "\a"
                break


            # 如果要不要中奖检索，将以下代码注释掉
            if self.cz_type == 2 :
                ADDR = (HOST, PORT)
                x = doSocket(ADDR)
                check_msg = "877805;0;1;%d;1;%d;%d;%d;%d;2;%s;%s"%(station_id,station_id,game_id,wager_issue,tsn,result_num,result_check)
                str_log = "trans Msg is :" + check_msg
                print str_log
                get_msg_result = x.ourSendMsg(str(check_msg))
                print get_msg_result
                logging.info("TSN:%d,ResultFromServer: %s"%(self.tsn,get_msg_result))
                if "999999" in get_msg_result:
                    print "\a"
                    break
                # 如果要不要中奖检索，将以上代码注释掉

            ADDR = (HOST, PORT)

            x = doSocket(ADDR)

        return u"操作完成,请及时查看日志!"
    
    #注销
    def cacelTick(self,tsn_num):
        HOST = self.getServerIP()
        print HOST
        PORT = int(self.getServerPort())
        print PORT
        ADDR = (HOST,PORT)
        x = doSocket(ADDR)
        station_cert = 801589720
        # station_cert = 9354 #站点51012222的认证码
        # station_cert =16323 #站点51010020的认证码
        msg = "103300;0;103;%d;1;;%d;%d;%d;%d;;%d;"%(self.getStationId(),self.getGameID(),self.getWagerIssue(),self.getStationId(),tsn_num,station_cert)
        str_log = 'trans Msg is :' + msg
        print str_log 
        get_msg = x.ourSendMsg(str(msg))
        print get_msg 
#         sys.exit(0) 
        
    #冲正注销
    def cacelCZTick(self,tsn_num):
        HOST = self.getServerIP()
        print HOST
        PORT = int(self.getServerPort())
        print PORT
        ADDR = (HOST,PORT)
        x = doSocket(ADDR)
        msg = "103999;0;1;%d;1;;%d;%d;%d;%d;;0;"%(self.getStationId(),self.getGameID() ,self.getWagerIssue(),self.getStationId(),tsn_num)
        str_log = 'trans Msg is :' + msg
        print str_log 
        get_msg = x.ourSendMsg(str(msg))
        print get_msg 
#         sys.exit(0)
        
        
    #单期兑奖
    def cashTick(self,game_issue,tsn_num):
        HOST = self.getServerIP()
        print HOST
        PORT = int(self.getServerPort())
        print PORT
        ADDR = (HOST,PORT)
        x = doSocket(ADDR)
        station_cert = 801589720 #站点51010005的认证码  
        # station_cert =16323 #站点51010020的认证码
        # station_cert = 9354 #站点51012222的认证码
        msg = "103009;0;103;%d;1;;%d;%d;%d;%d;;%d;"%(self.getStationId(),self.getStationId(),game_issue,self.getGameID(),tsn_num,station_cert)
        str_log = 'trans Msg is :' + msg
        print str_log 
        get_msg = x.ourSendMsg(str(msg))
        print get_msg 
    
    #多期兑奖
    def cashDQTick(self,game_issue,tsn_num):
        HOST = self.getServerIP()
        print HOST
        PORT = int(self.getServerPort())
        print PORT
        ADDR = (HOST,PORT)
        x = doSocket(ADDR)
        station_cert =801589720 #站点51010020的认证码
        msg = "103056;0;103;%d;1;;%d;%d;%d;%d;;%d;"%(self.getStationId(),self.getStationId(),game_issue,self.getGameID(),tsn_num,station_cert)
        str_log = 'trans Msg is :' + msg
        print str_log 
        get_msg = x.ourSendMsg(str(msg))
        print get_msg 


    #多期退票
    def refundTick(self,game_issue,tsn_num):
        HOST = self.getServerIP()
        print HOST
        PORT = int(self.getServerPort())
        print PORT
        ADDR = (HOST,PORT)
        x = doSocket(ADDR)
        station_cert = 801589720
        msg = "103058;0;103;%d;1;;%d;%d;%d;%d;;%d;"%(self.getStationId(),self.getStationId(),game_issue,self.getGameID(),tsn_num,station_cert)
        str_log = 'trans Msg is :' + msg
        print str_log 
        get_msg = x.ourSendMsg(str(msg))
        print get_msg 
     
    #银行缴款602201
    def ttD602201(self,station_id,money):
        HOST = self.getServerIP()
        print HOST
        PORT = int(self.getServerPort())
        print PORT
        ADDR = (HOST,PORT)
        x = doSocket(ADDR)
        now = datetime.datetime.now()        
        print now.strftime('%Y-%m-%d %H:%M:%S') 
        dDate_time  = now.strftime('%Y-%m-%d %H:%M:%S') 
        print dDate_time 
        msg = "602201;1;12345678;%d;1;12345678;%d;%d;%d;%s;5;"%(station_id,station_id,station_id,money,dDate_time )
        str_log = 'trans Msg is :' + msg
        print str_log
        get_msg = x.ourSendMsg(str(msg))

        print get_msg

        
   
if __name__== "__main__" :
    
    pro_name = "GS"     #省名拼音缩写
    game_name = "QL730"  #游戏名称 B001 ---双色球  QL730 --- 七乐彩  3D --- 3D  K512 --- 快乐十二
    
    issue = 2017069 #投注期号 
    #流水号
    #甘肃正常站点： 62011002 渠道站点 62660003 62011005 6 2011005
    station_id = 62011005   #正常投注站点  渠道自动兑奖站点 51990001 正常测试站点 51010005 51012222
    money = 2000  #缴款金额

    stat = 1 # 1 --- 投注  2 --- 注销   3 ---冲正  4 --- 单期兑奖  5 ---多期兑奖
    #  6 ---多期退票  7 ---银行缴款602201
    # 
#     station_id = 51990001 #四川渠道站点，用于测试自动兑奖
    cz_type = 2
    tsn = 684
    for i in range(0,1) : 
        search = toSearch(pro_name,game_name,tsn,issue,station_id,cz_type)
        if stat == 1 :
            search.search() #投注
        elif stat == 2 :
            search.cacelTick(tsn) #注销
        elif stat == 3 :
            search.cacelCZTick(tsn) #冲正
        elif stat == 4 :
            search.cashTick(issue,tsn) #单期兑奖
        elif stat == 5 :
            search.cashDQTick(issue, tsn) #多期兑奖
        elif stat == 6 :
            search.refundTick(issue, tsn) #多期退票
        elif stat == 7 :                #用于缴款T602201
            search.ttD602201(station_id, money)
        elif stat == 8 :
            search.checkTest() 
        else :
            print "系统维护中，请你稍等"
        tsn = tsn + 1917



   
