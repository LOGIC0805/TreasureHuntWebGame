# -*- coding:utf-8 -*-

from flask import request, render_template, Flask, jsonify
import pymongo
from flask_pymongo import PyMongo
import time
import random

app = Flask(__name__)
app.debug = True
app.config['MONGO_URI'] = 'mongodb://localhost:27017/user'
app.config['MONGO_DBNAME'] = 'user'
app.config['SECRET_KEY'] = '24'
app.url_map.strict_slaches = False
mongo = PyMongo(app)
set_time = 3600
set_backpack = 10
set_lucky = 1
set_work = 2
set_money = 1000

@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        phonenum = request.form['phonenum']
        password = request.form['password']
        if phonenum == '' or password == '':
            msg = "请输入完整信息！"
            return jsonify({'code': 1, 'msg': msg})
        else:
            login_user = mongo.db.userinfo.find_one({"phonenum": phonenum})
            if login_user == None:
                msg = "电话号码还未注册！"
                return jsonify({'code': 2, 'msg': msg})
            else:
                if login_user['password'] != password:
                    msg = "密码错误！"
                    return jsonify({'code': 3, 'msg': msg})
                else:
                    msg = "登录成功！"
                    return jsonify({'code': 0, 'msg': msg})
    else:
        return render_template("login.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        phonenum = request.form['phonenum']
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        if phonenum == '' or username == '' or password == '':
            msg = "请输入完整信息！"
            return jsonify({'code': 1, 'msg': msg})
        if password != password1:
            msg = "两次输入密码不一致！"
            return jsonify({'code': 2, 'msg': msg})
        else:
            result = mongo.db.userinfo.find({"phonenum": phonenum})
            if result.count() == 0:
                money = str(float(set_money))
                mongo.db.userinfo.insert_one({"phonenum": phonenum, "username": username, "password": password, "luckylevel": 1, "worklevel": 1, "money": money})
                mongo.db.usertime.insert_one({"phonenum": phonenum, "luckytime": '0', "moneytime": '0'})
                msg = "注册成功！"
                return jsonify({'code': 0, 'msg': msg})
            else:
                msg = '手机号码已注册！'
                return jsonify({'code': 3, 'msg': msg})
    else:
        return render_template("register.html")

@app.route('/forget', methods=['POST', 'GET'])
def forget():
    if request.method == 'POST':
        phonenum = request.form['phonenum']
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        if phonenum == '' or username == '' or password == '':
            msg = "请输入完整信息！"
            return jsonify({'code': 1, 'msg': msg})
        if password != password1:
            msg = "两次输入密码不一致！"
            return jsonify({'code': 2, 'msg': msg})
        else:
            forget_user = mongo.db.userinfo.find_one({"phonenum": phonenum})
            if forget_user == None:
                msg = "手机号码还未注册！"
                return jsonify({'code': 3, 'msg': msg})
            else:
                if forget_user['username'] != username:
                    msg = "用户名错误！"
                    return jsonify({'code': 4, 'msg': msg})
                else:
                    mongo.db.userinfo.update_one({"phonenum": phonenum},{'$set': {"password": password}})
                    msg = "修改成功！"
                    return jsonify({'code': 0, 'msg': msg})
    else:
        return render_template("forget.html")

@app.route('/self?phonenum=<phonenum>', methods=['POST', 'GET'])
def self(phonenum):
    self_user = mongo.db.userinfo.find_one({"phonenum": phonenum})
    user_lucky = []
    user_work = []
    lucky = mongo.db.userlucky.find({"phonenum": phonenum})
    for item in lucky:
        data = {}
        data['phonenum'] = item['phonenum']
        data['luckyname'] = item['luckyname']
        data['luckylevel'] = item['luckylevel']
        data['luckytype'] = item['luckytype']
        if item['luckystate'] == 0:
            data['luckystate'] = '储藏中'
            data['luckydeal'] = ['佩戴', '上架']
        elif item['luckystate'] == 1:
            data['luckystate'] = '佩戴中'
            data['luckydeal'] = ['取下']
        else:
            data['luckystate'] = '上架中'
            data['luckydeal'] = ['下架']
        user_lucky.append(data)
    work = mongo.db.userwork.find({"phonenum": phonenum})
    for item in work:
        data = {}
        data['phonenum'] = item['phonenum']
        data['workname'] = item['workname']
        data['worklevel'] = item['worklevel']
        data['worktype'] = item['worktype']
        if item['workstate'] == 0:
            data['workstate'] = '储藏中'
            data['workdeal'] = ['佩戴', '上架']
        elif item['workstate'] == 1:
            data['workstate'] = '佩戴中'
            data['workdeal'] = ['取下']
        else:
            data['workstate'] = '上架中'
            data['workdeal'] = ['下架']
        user_work.append(data)
    if request.method == 'POST':
        posttype = request.form['posttype']
        if posttype == '0':
            luckystate = request.form['luckystate']
            luckyname = request.form['luckyname']
            luckytype = request.form['luckytype']
            lucky_deal = mongo.db.userlucky.find_one({"phonenum": phonenum, "luckyname": luckyname, "luckytype": luckytype})
            if luckystate == '1':
                mongo.db.userlucky.update_one({"phonenum": phonenum, "luckyname": luckyname, "luckytype": luckytype},{'$set': {"luckystate": 0}})
                luckylevel = self_user['luckylevel'] - lucky_deal['luckylevel']
                mongo.db.userinfo.update_one({"phonenum": phonenum}, {'$set': {"luckylevel": luckylevel}})
                msg = '成功取下！'
                user_lucky = mongo.db.userlucky.find({"phonenum": phonenum, 'luckystate': 0}).sort('luckylevel', pymongo.ASCENDING)
                if user_lucky.count() > set_backpack:
                    mongo.db.userlucky.delete_one(user_lucky[0])
                    msg += '\n由于存储库已满，运气等级最低的饰品已自动删除！'
                return jsonify({'code': 0, 'msg': msg})
            elif luckystate == '2':
                mongo.db.userlucky.update_one({"phonenum": phonenum, "luckyname": luckyname, "luckytype": luckytype},{'$set': {"luckystate": 0}})
                mongo.db.storelucky.delete_one({"phonenum": phonenum, 'luckyname': luckyname, 'luckytype': luckytype})
                msg = '成功下架！'
                user_lucky = mongo.db.userlucky.find({"phonenum": phonenum, 'luckystate': 0}).sort('luckylevel', pymongo.ASCENDING)
                if user_lucky.count() > set_backpack:
                    mongo.db.userlucky.delete_one(user_lucky[0])
                    msg += '\n由于存储库已满，运气等级最低的饰品已自动删除！'
                return jsonify({'code': 1, 'msg': msg})
            else:
                if luckystate == '00':
                    wear_lucky = mongo.db.userlucky.find({"phonenum": phonenum, "luckystate": 1})
                    wearnum_lucky = 0
                    if wear_lucky != None:
                        wearnum_lucky = wear_lucky.count()
                    if wearnum_lucky > set_lucky - 1:
                        msg = '饰品佩戴位置已满，佩戴失败！'
                        return jsonify({'code': 2, 'msg': msg})
                    else:
                        mongo.db.userlucky.update_one({"phonenum": phonenum, "luckyname": luckyname, "luckytype": luckytype},{'$set': {"luckystate": 1}})
                        luckylevel = self_user['luckylevel'] + lucky_deal['luckylevel']
                        mongo.db.userinfo.update_one({"phonenum": phonenum}, {'$set': {"luckylevel": luckylevel}})
                        msg = '佩戴成功！'
                        return jsonify({'code': 3, 'msg': msg})
                else:
                    luckyprice = request.form['luckyprice']
                    if luckyprice == '':
                        msg = '上架失败，请输入价格！'
                        return jsonify({'code': 4, 'msg': msg})
                    else:
                        luckyprice = float(luckyprice)
                        mongo.db.userlucky.update_one({"phonenum": phonenum, "luckyname": luckyname, "luckytype": luckytype},{'$set': {"luckystate": 2}})
                        mongo.db.storelucky.insert_one({"phonenum": phonenum, 'luckyname': luckyname, 'luckytype': luckytype, 'luckyprice': str(luckyprice), 'luckylevel': lucky_deal['luckylevel']})
                        msg = '成功上架！'
                        return jsonify({'code': 5, 'msg': msg})
        else:
            workstate = request.form['workstate']
            workname = request.form['workname']
            worktype = request.form['worktype']
            work_deal = mongo.db.userwork.find_one({"phonenum": phonenum, "workname": workname, "worktype": worktype})
            if workstate == '1':
                mongo.db.userwork.update_one({"phonenum": phonenum, "workname": workname, "worktype": worktype},{'$set': {"workstate": 0}})
                worklevel = self_user['worklevel'] - work_deal['worklevel']
                mongo.db.userinfo.update_one({"phonenum": phonenum}, {'$set': {"worklevel": worklevel}})
                msg = '成功取下！'
                user_work = mongo.db.userwork.find({"phonenum": phonenum, 'workstate': 0}).sort('worklevel', pymongo.ASCENDING)
                if user_work.count() > set_backpack:
                    mongo.db.userwork.delete_one(user_work[0])
                    msg += '\n由于存储库已满，运气等级最低的饰品已自动删除！'
                return jsonify({'code': 6, 'msg': msg})
            elif workstate == '2':
                mongo.db.userwork.update_one({"phonenum": phonenum, "workname": workname, "worktype": worktype},{'$set': {"workstate": 0}})
                mongo.db.storework.delete_one({"phonenum": phonenum, 'workname': workname, 'worktype': worktype})
                msg = '成功下架！'
                user_work = mongo.db.userwork.find({"phonenum": phonenum, 'workstate': 0}).sort('worklevel', pymongo.ASCENDING)
                if user_work.count() > set_backpack:
                    mongo.db.userwork.delete_one(user_work[0])
                    msg += '\n由于存储库已满，运气等级最低的饰品已自动删除！'
                return jsonify({'code': 7, 'msg': msg})
            else:
                if workstate == '00':
                    wear_work = mongo.db.userwork.find({"phonenum": phonenum, "workstate": 1})
                    wearnum_work = 0
                    if wear_work != None:
                        wearnum_work = wear_work.count()
                    if wearnum_work > set_work - 1:
                        msg = '工具佩戴位置已满，佩戴失败！'
                        return jsonify({'code': 8, 'msg': msg})
                    else:
                        mongo.db.userwork.update_one({"phonenum": phonenum, "workname": workname, "worktype": worktype},{'$set': {"workstate": 1}})
                        worklevel = self_user['worklevel'] + work_deal['worklevel']
                        mongo.db.userinfo.update_one({"phonenum": phonenum}, {'$set': {"worklevel": worklevel}})
                        msg = '佩戴成功！'
                        return jsonify({'code': 9, 'msg': msg})
                else:
                    workprice = request.form['workprice']
                    if workprice == '':
                        msg = '上架失败，请输入价格！'
                        return jsonify({'code': 10, 'msg': msg})
                    else:
                        workprice = float(workprice)
                        mongo.db.userwork.update_one({"phonenum": phonenum, "workname": workname, "worktype": worktype},{'$set': {"workstate": 2}})
                        mongo.db.storework.insert_one({"phonenum": phonenum, 'workname': workname, 'worktype': worktype, 'workprice': str(workprice), 'worklevel': work_deal['worklevel']})
                        msg = '成功上架！'
                        return jsonify({'code': 11, 'msg': msg})
    else:
        return render_template("self.html", user = self_user, lucky = user_lucky, work = user_work, user_id = '')

@app.route('/store?phonenum=<phonenum>', methods=['POST', 'GET'])
def store(phonenum):
    store_user = mongo.db.userinfo.find_one({"phonenum": phonenum})
    store_lucky = mongo.db.storelucky.find()
    store_work = mongo.db.storework.find()
    if request.method == 'POST':
        posttype = request.form['posttype']
        user = request.form['user']
        if user == store_user['phonenum']:
            msg = '购买失败，不能购买自己上架的商品！'
            return jsonify({'code': 0, 'msg': msg})
        else:
            seller = mongo.db.userinfo.find_one({"phonenum": user})
            msg = '购买成功！'
            if posttype == '0':
                luckyname = request.form['luckyname']
                luckytype = request.form['luckytype']
                lucky_buy = mongo.db.storelucky.find_one({'luckyname': luckyname, 'luckytype': luckytype})
                flag = mongo.db.userlucky.find_one({'phonenum': phonenum, 'luckyname': luckyname, 'luckytype': luckytype})
                if flag != None:
                    msg = '存储库已存在该饰品，购买失败！'
                    return jsonify({'code': 1, 'msg': msg})
                else:
                    if float(store_user['money']) < float(lucky_buy['luckyprice']):
                        msg = '金币余额不足，购买失败！'
                        return jsonify({'code': 2, 'msg': msg})
                    else:
                        buyer_money = float(store_user['money']) - float(lucky_buy['luckyprice'])
                        seller_money = float(seller['money']) + float(lucky_buy['luckyprice'])
                        mongo.db.userinfo.update_one({"phonenum": phonenum},{'$set': {"money": str(buyer_money)}})
                        mongo.db.userinfo.update_one({"phonenum": user},{'$set': {"money": str(seller_money)}})
                        mongo.db.userlucky.delete_one({'phonenum': user, 'luckyname': luckyname, 'luckytype': luckytype})
                        mongo.db.storelucky.delete_one({"phonenum": user, 'luckyname': luckyname, 'luckytype': luckytype})
                        name = mongo.db.reference.find_one({'name': luckyname})
                        mongo.db.userlucky.insert_one({"phonenum": phonenum, "luckytype": luckytype, 'luckystate': 0, 'luckyname': name['name'], 'luckylevel': name['luckylevel']})
                        user_lucky = mongo.db.userlucky.find({"phonenum": phonenum, 'luckystate': 0}).sort('luckylevel', pymongo.ASCENDING)
                        if user_lucky.count() > set_backpack:
                            mongo.db.userlucky.delete_one(user_lucky[0])
                            msg += '\n由于存储库已满，运气等级最低的饰品已自动删除！'
                        return jsonify({'code': 3, 'msg': msg})
            else:
                workname = request.form['workname']
                worktype = request.form['worktype']
                work_buy = mongo.db.storework.find_one({'workname': workname, 'worktype': worktype})
                flag = mongo.db.userwork.find_one({'phonenum': phonenum, 'workname': workname, 'worktype': worktype})
                if flag != None:
                    msg = '存储库已存在该工具，购买失败！'
                    return jsonify({'code': 4, 'msg': msg})
                else:
                    if float(store_user['money']) < float(work_buy['workprice']):
                        msg = '金币余额不足，购买失败！'
                        return jsonify({'code': 5, 'msg': msg})
                    else:
                        buyer_money = float(store_user['money']) - float(work_buy['workprice'])
                        seller_money = float(seller['money']) + float(work_buy['workprice'])
                        mongo.db.userinfo.update_one({"phonenum": phonenum},{'$set': {"money": str(buyer_money)}})
                        mongo.db.userinfo.update_one({"phonenum": user},{'$set': {"money": str(seller_money)}})
                        mongo.db.userwork.delete_one({'phonenum': user, 'workname': workname, 'worktype': worktype})
                        mongo.db.storework.delete_one({"phonenum": user, 'workname': workname, 'worktype': worktype})
                        name = mongo.db.reference.find_one({'name': workname})
                        mongo.db.userwork.insert_one({"phonenum": phonenum, "worktype": worktype, 'workstate': 0, 'workname': name['name'], 'worklevel': name['worklevel']})
                        user_work = mongo.db.userwork.find({"phonenum": phonenum, 'workstate': 0}).sort('worklevel', pymongo.ASCENDING)
                        if user_work.count() > set_backpack:
                            mongo.db.userwork.delete_one(user_work[0])
                            msg += '\n由于存储库已满，工作能力最低的工具已自动删除！'
                        return jsonify({'code': 6, 'msg': msg})
        return msg
    else:
        return render_template("store.html", user = store_user, lucky = store_lucky, work = store_work)

@app.route('/daily?phonenum=<phonenum>', methods=['POST', 'GET'])
def daily(phonenum):
    daily_user = mongo.db.userinfo.find_one({"phonenum": phonenum})
    if request.method == 'POST':
        posttype = request.form['posttype']
        now_time = time.time()
        past = mongo.db.usertime.find_one({"phonenum": phonenum})
        past_luckytime = float(past['luckytime'])
        past_moneytime = float(past['moneytime'])
        if posttype == '0':
            dtime = now_time - past_luckytime
            if dtime <= set_time:
                msg = '间隔时间不足，无法开启！'
                return jsonify({'code': 0, 'msg': msg})
            else:
                mongo.db.usertime.update_one({"phonenum": phonenum},{'$set': {"luckytime": now_time}})
                all_type = ['stone', 'crystal', 'pliers', 'knife', 'shovel', 'machine']
                typenum = random.randint(0, 5)
                namenum = random.randint(0, 1000)
                luckynum = random.randint(0, daily_user['luckylevel']) * random.randint(0, 50)
                namenum += luckynum
                if namenum >= 1000:
                    namenum = 999
                name = mongo.db.reference.find_one({"startnum_possibility": {"$lte": namenum}, "endnum_possibility": {"$gt": namenum}})
                msg = '恭喜你开出：' + all_type[typenum] + '：' + name['name'] + '！'
                if typenum == 0 or typenum == 1:
                    flag = mongo.db.userlucky.find_one({"phonenum": phonenum, "luckytype": all_type[typenum], 'luckyname': name['name']})
                    if flag != None:
                        msg += '\n存储库已存在该工具，该饰品已自动删除！'
                    else:
                        mongo.db.userlucky.insert_one({"phonenum": phonenum, "luckytype": all_type[typenum], 'luckystate': 0, 'luckyname': name['name'], 'luckylevel': name['luckylevel']})
                        user_lucky = mongo.db.userlucky.find({"phonenum": phonenum, 'luckystate': 0}).sort('luckylevel', pymongo.ASCENDING)
                        if user_lucky.count() > set_backpack:
                            mongo.db.userlucky.delete_one(user_lucky[0])
                            msg += '\n由于存储库已满，运气等级最低的饰品已自动删除！'
                else:
                    flag = mongo.db.userwork.find_one({"phonenum": phonenum, "worktype": all_type[typenum], 'workname': name['name']})
                    if flag != None:
                        msg += '\n存储库已存在该工具，该饰品已自动删除！'
                    else:
                        mongo.db.userwork.insert_one({"phonenum": phonenum, "worktype": all_type[typenum], 'workstate': 0, 'workname': name['name'], 'worklevel': name['worklevel']})
                        user_work = mongo.db.userwork.find({"phonenum": phonenum, 'workstate': 0}).sort('worklevel', pymongo.ASCENDING)
                        if user_work.count() > set_backpack:
                            mongo.db.userwork.delete_one(user_work[0])
                            msg += '\n由于存储库已满，工作能力最低的工具已自动删除！'
                return jsonify({'code': 1, 'msg': msg})
        else:
            dtime = now_time - past_moneytime
            if dtime <= set_time:
                msg = '间隔时间不足，无法开始！'
                return jsonify({'code': 2, 'msg': msg})
            else:
                mongo.db.usertime.update_one({"phonenum": phonenum},{'$set': {"moneytime": now_time}})
                earn = float(daily_user['worklevel']) * 1000
                money = float(daily_user['money']) + earn
                mongo.db.userinfo.update_one({"phonenum": phonenum},{'$set': {"money": str(money)}})
                msg = '恭喜你获得：' + str(earn) + '金币' + '！'
                return jsonify({'code': 3, 'msg': msg})
    else:
        return render_template("daily.html", user = daily_user)


if __name__ == '__main__':
    app.run()
