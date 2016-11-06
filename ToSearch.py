#!/usr/bin/env python
#-*- coding:utf-8 -*-

from OpenExcel import OpenExcel
from ConnSocket import doSocket
from ReadIni import ReadIni
from socket import *
import struct
import sys
import time
import os

reload(sys)
sys.setdefaultencoding("utf-8")

str_log = ""
log_in = []

class toSearch :
    def __init__(self,pro_code,game_name,tsn,wager_issue,station_id,cz_type):
        self.pro_code = pro_code
        self.game_name = game_name
        self.tsn = tsn
        self.wager_issue = wager_issue
        self.station_id = station_id
        self.cz_type = cz_type

    def search(self) :
        readIni = ReadIni("ip.ini")
        HOST = readIni.getValue(self.pro_code,"ip")
        print HOST
        PORT = int(readIni.getValue(self.pro_code,"port"))
        print PORT
        ADDR = (HOST,PORT)
        excelFile = readIni.getValue(self.pro_code,"file")
        # print excelFile

        if self.game_name == "3D" :
            game_id = int(readIni.getValue(self.pro_code,"3d_id"))
            by_name = readIni.getValue(self.pro_code,"3d")

        elif self.game_name == "BOOL" :
            game_id = int(readIni.getValue(self.pro_code,"bool_id"))
            by_name = readIni.getValue(self.pro_code, "bool")
        elif self.game_name == "Q730" :
            game_id = int(readIni.getValue(self.pro_code,"q730_id"))
            by_name = readIni.getValue(self.pro_code, "q730")
        elif self.game_name == "K3" :
            game_id = int(readIni.getValue(self.pro_code,"k3_id"))
            by_name = readIni.getValue(self.pro_code, "k3")
        elif self.game_name == "H520" :
            game_id = int(readIni.getValue(self.pro_code,"h520_id"))
            by_name = readIni.getValue(self.pro_code, "h520")
        # print game_id
        # print by_name

        openX = OpenExcel(file=excelFile,by_name=by_name)
        table = openX.excel_table_byname()

        x = doSocket(ADDR)

        for i in range(0,len(table)) :
            self.tsn += 1
            game_type = int(table[i]["PlayType"])
            wager_money = int(table[i]["WagerMoney"])
            num = table[i]["WagerNum"]
            bs = int(table[i]["BS"])
            result_num = table[i]["PreWinNum"]
            result_check = table[i]["PreWinResult"]
            new_num = num.split(";")
            lottery_num = str(len(new_num) - 1)
            for i in range(0, len(new_num) - 1):
                lottery_num = lottery_num + ";" + str(i + 1) + ";3;" + str(game_type) + ";" + str(bs) + ";" + new_num[i]

            #msg = '101200;0;1;%d;1;%d;%d;%d;%s;%d;1;;;;%s;;' % (self.station_id, game_id, self.wager_issue, self.tsn, wager_money, self.tsn - 1, lottery_num)
            #多期 2期
            msg = '101200;0;1;%d;1;%d;%d;%d;%s;%d;2;;;;%s;;' % (self.station_id, game_id, self.wager_issue, self.tsn, wager_money, self.tsn - 1, lottery_num)

            ADDR = (HOST, PORT)
            str_log = 'trans Msg is :' + msg
            print str_log
            get_msg = x.ourSendMsg(str(msg))
            print get_msg
            if "999999" in get_msg:
                print "\a"
                break


            # 如果要不要中奖检索，将以下代码注释掉
            if self.cz_type == 2 :
                ADDR = (HOST, PORT)
                x = doSocket(ADDR)
                check_msg = "877805;0;1;%d;1;%d;%d;%d;%d;2;%s;%s" % (self.station_id, self.station_id, game_id, self.wager_issue, self.tsn, result_num, result_check)
                str_log = "trans Msg is :" + check_msg
                print str_log
                get_msg_result = x.ourSendMsg(str(check_msg))
                print get_msg_result
                if "999999" in get_msg_result:
                    print "\a"
                    break
                # 如果要不要中奖检索，将以上代码注释掉

            ADDR = (HOST, PORT)

            x = doSocket(ADDR)

        return u"操作完成,请及时查看日志!"


if __name__ == "__main__" :
    #七乐彩
    # search = toSearch("XJ","Q730",0,2016010,65010754,1)
    #3D
    # search = toSearch("XJ","3D",0,2016017,65010754,1)
    #双色球
    #search = toSearch("XJ","BOOL",0,2016011,65010754,1)
    #山西快乐十分
    search = toSearch("SX","H520",0,161106054,14010003,1)
    print search.search() 
    # station_id = [41002003,41010012,41010013,41010014,41010015,41010016]
    # issue = 161103039
    # for i in range(0,len(station_id) ) :
    #     i = 0 
    #     search = toSearch("HeN","K3",0,issue,station_id[i],1)
    #     print search.search()
    # i = 1
    # issue = 161102044
    # search = toSearch("HeN","K3",0,issue,station_id[i],1)
    # print search.search()
    

