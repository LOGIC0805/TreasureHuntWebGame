from flask import request, render_template, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import time
import random

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cui,logic@127.0.0.1/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '24'
db = SQLAlchemy(app)
   
class Userinfo(db.Model):
    __tablename__ = 'userinfo'
    phonenum = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))
    username = db.Column(db.String(20))
    userlucky = db.Column(db.Integer)
    userwork = db.Column(db.Integer)
    money = db.Column(db.String(20))
    luckytime = db.Column(db.String(30))
    worktime = db.Column(db.String(30))

class Treasure(db.Model):
    __tablename__ = 'treasure'
    name = db.Column(db.String(20), primary_key=True)
    level = db.Column(db.Integer)
    startnum = db.Column(db.Integer)
    endnum = db.Column(db.Integer)

class Userpackage(db.Model):
    __tablename__ = 'userpackage'
    phonenum = db.Column(db.String(20), primary_key=True)
    state = db.Column(db.Integer)
    name = db.Column(db.String(20), primary_key=True)
    typename = db.Column(db.String(20), primary_key=True)
    flag = db.Column(db.Integer)
    price = db.Column(db.String(20))
    level = db.Column(db.Integer)

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
            login_user = db.session.query(Userinfo).filter_by(phonenum = phonenum).first()
            if login_user == None:
                msg = "电话号码还未注册！"
                return jsonify({'code': 2, 'msg': msg})
            else:
                if login_user.password != password:
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
            result = db.session.query(Userinfo).filter_by(phonenum = phonenum).first()
            if result == None:
                money = str(float(set_money))
                register_user = Userinfo()
                register_user.phonenum = phonenum
                register_user.password = password
                register_user.username = username
                register_user.phonenum = phonenum
                register_user.userlucky = 1
                register_user.userwork = 1
                register_user.money = money
                register_user.luckytime = '0'
                register_user.worktime = '0'
                db.session.add(register_user)
                db.session.commit()
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
            forget_user = db.session.query(Userinfo).filter_by(phonenum = phonenum).first()
            if forget_user == None:
                msg = "手机号码还未注册！"
                return jsonify({'code': 3, 'msg': msg})
            else:
                if forget_user.username != username:
                    msg = "用户名错误！"
                    return jsonify({'code': 4, 'msg': msg})
                else:
                    forget_user.password = password
                    db.session.commit()
                    msg = "修改成功！"
                    return jsonify({'code': 0, 'msg': msg})
    else:
        return render_template("forget.html")

@app.route('/self?phonenum=<phonenum>', methods=['POST', 'GET'])
def self(phonenum):
    self_user = db.session.query(Userinfo).filter_by(phonenum = phonenum).first()
    user_lucky = []
    user_work = []
    lucky = db.session.query(Userpackage).filter(Userpackage.phonenum == phonenum, Userpackage.flag == 0).all()
    for item in lucky:
        data = {}
        data['phonenum'] = item.phonenum
        data['luckyname'] = item.name
        data['luckylevel'] = item.level
        data['luckytype'] = item.typename
        if item.state == 0:
            data['luckystate'] = '储藏中'
            data['luckydeal'] = ['佩戴', '上架']
        elif item.state == 1:
            data['luckystate'] = '佩戴中'
            data['luckydeal'] = ['取下']
        else:
            data['luckystate'] = '上架中'
            data['luckydeal'] = ['下架']
        user_lucky.append(data)
    work = db.session.query(Userpackage).filter(Userpackage.phonenum == phonenum, Userpackage.flag == 1).all()
    for item in work:
        data = {}
        data['phonenum'] = item.phonenum
        data['workname'] = item.name
        data['worklevel'] = item.level
        data['worktype'] = item.typename
        if item.state == 0:
            data['workstate'] = '储藏中'
            data['workdeal'] = ['佩戴', '上架']
        elif item.state == 1:
            data['workstate'] = '佩戴中'
            data['workdeal'] = ['取下']
        else:
            data['workstate'] = '上架中'
            data['workdeal'] = ['下架']
        user_work.append(data)
    if request.method == 'POST':
        posttype = int(request.form['posttype'])
        state = request.form['state']
        name = request.form['name']
        typename = request.form['typename']
        deal = db.session.query(Userpackage).filter(Userpackage.phonenum == phonenum, Userpackage.flag == posttype, Userpackage.name == name, Userpackage.typename == typename).first()
        if state == '1':
            deal.state = 0
            if posttype == 0:
                self_user.userlucky -= deal.level
            else:
                self_user.userwork -= deal.level
            db.session.commit()
            msg = '成功取下！'
            return jsonify({'code': 0, 'msg': msg})
        elif state == '2':
            deal.state = 0
            db.session.commit()
            msg = '成功下架！'
            return jsonify({'code': 1, 'msg': msg})
        else:
            if state == '00' or state == '10':
                wear = db.session.query(Userpackage).filter(Userpackage.phonenum == phonenum, Userpackage.flag == posttype, Userpackage.state == 1).all()
                wearnum = 0
                if wear != None:
                    wearnum= len(wear)
                if posttype == 0:
                    if wearnum > set_lucky - 1:
                        msg = '饰品佩戴位置已满，佩戴失败！'
                        return jsonify({'code': 2, 'msg': msg})
                    else:
                        deal.state = 1
                        self_user.userlucky += deal.level
                        db.session.commit()
                        msg = '佩戴成功！'
                        return jsonify({'code': 3, 'msg': msg})
                else:
                    if wearnum > set_work - 1:
                        msg = '工具佩戴位置已满，佩戴失败！'
                        return jsonify({'code': 6, 'msg': msg})
                    else:
                        deal.state = 1
                        self_user.userwork += deal.level
                        db.session.commit()
                        msg = '佩戴成功！'
                        return jsonify({'code': 7, 'msg': msg})
            else:
                price = request.form['price']
                if price == '':
                    msg = '上架失败，请输入价格！'
                    return jsonify({'code': 4, 'msg': msg})
                else:
                    price = float(price)
                    deal.state = 2
                    deal.price = str(price)
                    db.session.commit()
                    msg = '成功上架！'
                    return jsonify({'code': 5, 'msg': msg})
    else:
        return render_template("self.html", user = self_user, lucky = user_lucky, work = user_work, user_id = '')

@app.route('/store?phonenum=<phonenum>', methods=['POST', 'GET'])
def store(phonenum):
    store_user = db.session.query(Userinfo).filter_by(phonenum = phonenum).first()
    store_lucky = db.session.query(Userpackage).filter(Userpackage.flag == 0, Userpackage.state == 2).all()
    store_work = db.session.query(Userpackage).filter(Userpackage.flag == 1, Userpackage.state == 2).all()
    if request.method == 'POST':
        posttype = int(request.form['posttype'])
        user = request.form['user']
        if user == store_user.phonenum:
            msg = '购买失败，不能购买自己上架的商品！'
            return jsonify({'code': 0, 'msg': msg})
        else:
            seller = db.session.query(Userinfo).filter_by(phonenum = user).first()
            msg = '购买成功！'
            name = request.form['name']
            typename = request.form['typename']
            buy = db.session.query(Userpackage).filter(Userpackage.phonenum == user, Userpackage.flag == posttype, Userpackage.name == name, Userpackage.typename == typename, Userpackage.state == 2).first()
            flag = db.session.query(Userpackage).filter(Userpackage.phonenum == phonenum, Userpackage.flag == posttype, Userpackage.name == name, Userpackage.typename == typename).first()
            if flag != None:
                msg = '存储库已存在该物品，购买失败！'
                return jsonify({'code': 1, 'msg': msg})
            else:
                if float(store_user.money) < float(buy.price):
                    msg = '金币余额不足，购买失败！'
                    return jsonify({'code': 2, 'msg': msg})
                else:
                    store_user.money = float(store_user.money) - float(buy.price)
                    seller.money = float(seller.money) + float(buy.price)
                    buy.phonenum = phonenum
                    buy.state = 0
                    db.session.commit()
                    user_lucky = db.session.query(Userpackage).filter(Userpackage.phonenum == phonenum, Userpackage.flag == 0).order_by(Userpackage.level.asc()).all()
                    user_work = db.session.query(Userpackage).filter(Userpackage.phonenum == phonenum, Userpackage.flag == 1).order_by(Userpackage.level.asc()).all()
                    if len(user_lucky) > set_backpack:
                        msg += '\n由于存储库已满，运气等级最低的饰品已自动删除！'
                        if user_lucky[0].state == 1:
                            store_user.userlucky -= user_lucky[0].level
                        db.session.delete(user_lucky[0])
                        db.session.commit()
                    if len(user_work) > set_backpack:
                        msg += '\n由于存储库已满，工作能力最低的工具已自动删除！'
                        if user_work[0].state == 1:
                            store_user.userwork -= user_work[0].level
                        db.session.delete(user_work[0])
                        db.session.commit()
                    return jsonify({'code': 3, 'msg': msg})
    else:
        return render_template("store.html", user = store_user, lucky = store_lucky, work = store_work)

@app.route('/daily?phonenum=<phonenum>', methods=['POST', 'GET'])
def daily(phonenum):
    daily_user = db.session.query(Userinfo).filter_by(phonenum = phonenum).first()
    if request.method == 'POST':
        posttype = request.form['posttype']
        now_time = time.time()
        past_luckytime = float(daily_user.luckytime)
        past_worktime = float(daily_user.worktime)
        if posttype == '0':
            dtime = now_time - past_luckytime
            if dtime <= set_time:
                msg = '间隔时间不足，无法开启！'
                return jsonify({'code': 0, 'msg': msg})
            else:
                daily_user.luckytime = str(now_time)
                db.session.commit()
                all_type = ['stone', 'crystal', 'pliers', 'knife', 'shovel', 'machine']
                typenum = random.randint(0, 5)
                namenum = random.randint(0, 1000)
                luckynum = random.randint(0, daily_user.userlucky) * random.randint(0, 50)
                namenum += luckynum
                if namenum >= 1000:
                    namenum = 999
                result = db.session.query(Treasure).filter(Treasure.startnum <= namenum, Treasure.endnum >= namenum).first()
                typename = all_type[typenum]
                name = result.name
                level = result.level
                msg = '恭喜你开出：' + typename + '：' + name + '！'
                if typenum == 0 or typenum == 1:
                    flag = 0
                else:
                    flag = 1
                flag_result = db.session.query(Userpackage).filter(Userpackage.phonenum == phonenum, Userpackage.typename == typename, Userpackage.name == name).first()
                if flag_result != None:
                    msg += '\n存储库已存在该工具，该饰品已自动删除！'
                else:
                    treasure = Userpackage()
                    treasure.phonenum = phonenum
                    treasure.typename = typename
                    treasure.name = name
                    treasure.state = 0
                    treasure.flag = flag
                    treasure.level = level
                    db.session.add(treasure)
                    db.session.commit()
                    user_lucky = db.session.query(Userpackage).filter(Userpackage.phonenum == phonenum, Userpackage.flag == 0).order_by(Userpackage.level.asc()).all()
                    user_work = db.session.query(Userpackage).filter(Userpackage.phonenum == phonenum, Userpackage.flag == 1).order_by(Userpackage.level.asc()).all()
                    if len(user_lucky) > set_backpack:
                        msg += '\n由于存储库已满，运气等级最低的饰品已自动删除！'
                        if user_lucky[0].state == 1:
                            daily_user.userlucky -= user_lucky[0].level
                        db.session.delete(user_lucky[0])
                        db.session.commit()
                    if len(user_work) > set_backpack:
                        msg += '\n由于存储库已满，工作能力最低的工具已自动删除！'
                        if user_work[0].state == 1:
                            daily_user.userwork -= user_work[0].level
                        db.session.delete(user_work[0])
                        db.session.commit()
                return jsonify({'code': 1, 'msg': msg})
        else:
            dtime = now_time - past_worktime
            if dtime <= set_time:
                msg = '间隔时间不足，无法开始！'
                return jsonify({'code': 2, 'msg': msg})
            else:
                earn = float(daily_user.userwork) * 1000
                money = str(float(daily_user.money) + earn)
                daily_user.worktime = str(now_time)
                daily_user.money = money
                db.session.commit()
                msg = '恭喜你获得：' + str(earn) + '金币' + '！'
                return jsonify({'code': 3, 'msg': msg})
    else:
        return render_template("daily.html", user = daily_user)


if __name__ == '__main__':
    app.run()
