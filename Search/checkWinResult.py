#!/usr/bin/env python 
#-*- coding:utf-8 -*- 

import psycopg2
import sys
# 数据库连接参数
reload(sys)
sys.setdefaultencoding('utf8')

game_id = 4 
issue = 2016326 
conn = psycopg2.connect(database="lottery", user="lottery", password="lottery", host="192.168.0.91", port="5432")
cur = conn.cursor()
sql = """select wager_issue,win_level_name,win_bet,prize_per_bet from win_result ,win_level where win_result.game_id = %s 
and win_result.wager_issue = %s and win_level.game_id = win_result.game_id AND
win_level.win_level = win_result.win_level order by win_result.win_level """%(game_id ,issue)
cur.execute(sql)
rows = cur.fetchall()        # all rows in table
# print(rows)
for i in rows:
    for result in i :
        print result ,
    print "\n"
conn.commit()
cur.close()
conn.close()