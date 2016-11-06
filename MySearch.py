#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Flask
from flask import render_template
from ToSearch import toSearch
from flask import request
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/')
@app.route('/index')
def index() :
    return render_template("index.html")

@app.route('/search/',methods=['GET','POST'])
def search():
    # if request.method == 'POST' :
    pro_code = request.form.get("pro_code")
    print pro_code
    old_game_name = str(request.form.get("game_name"))
    print type(old_game_name)
    game_name = ""
    print old_game_name
    if old_game_name == "GS" :
        game_name = "GS"
    wager_issue = int(request.form.get("wager_issue"))
    print wager_issue
    tsn = request.form.get("tsn")
    print tsn
    cz_type = request.form.get("cz_type")
    print cz_type
    station_id = request.form.get("station_id")
    print station_id

    if pro_code == None or pro_code == "" :
        return u"省份为空,请重新输入!"
    elif game_name == None or game_name == "" :
        return u"游戏名称为空,请重新输入!"
    elif wager_issue == None or wager_issue == "" :
        return u"游戏期号为空,请重新输入!"
    elif tsn  == None or tsn == "" :
        return u"流水号为空,请重新输入!"
    elif cz_type == None or cz_type == "" :
        return u"操作类型为空,请重新输入!"
    elif station_id ==None or station_id == "" :
        return u"站点编号为空,请重新输入!"

    search = toSearch(pro_code,game_name,tsn,wager_issue,station_id,cz_type)
    print search.search()

    return "Success!"

if __name__ == '__main__':
    app.run()
