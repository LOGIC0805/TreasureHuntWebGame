import unittest
from server import app
import json


# 测试登录页面
class Test_login(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    # 测试手机号码和密码输入全空
    def test_phonenum_password_empty(self):
        response = self.client.post("/login", data = {'phonenum': '', 'password': ''})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试手机号码输入为空
    def test_phonenum_empty(self):
        response = self.client.post("/login", data = {'phonenum': '', 'password': '111'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试密码输入为空
    def test_password_empty(self):
        response = self.client.post("/login", data = {'phonenum': '123', 'password': ''})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试手机号码还未注册
    def test_phonenum_not_register(self):
        response = self.client.post("/login", data = {'phonenum': '1234', 'password': '1234'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 2)
    # 测试密码错误
    def test_password_wrong(self):
        response = self.client.post("/login", data = {'phonenum': '123', 'password': '1234'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 3)
    # 测试登录成功
    def test_login_success(self):
        response = self.client.post("/login", data = {'phonenum': '123', 'password': '111'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 0)


# 测试注册页面
class Test_register(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    # 测试手机号码、用户名和密码输入全空
    def test_phonenum_username_password_empty(self):
        response = self.client.post("/register", data = {'phonenum': '', 'username': '', 'password': '', 'password1': ''})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试手机号码输入为空
    def test_phonenum_empty(self):
        response = self.client.post("/register", data = {'phonenum': '', 'username': 'TestRegister','password': '111', 'password1': '111'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试用户名输入为空
    def test_username_empty(self):
        response = self.client.post("/register", data = {'phonenum': '111', 'username': '', 'password': '111', 'password1': '111'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试密码输入为空
    def test_password_empty(self):
        response = self.client.post("/register", data = {'phonenum': '111', 'username': 'TestRegister', 'password': '', 'password1': ''})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试两次输入密码不一致
    def test_password_not_equel_password1(self):
        response = self.client.post("/register", data = {'phonenum': '111', 'username': 'TestRegister', 'password': '111', 'password1': '1'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 2)
    # 测试手机号码已注册
    def test_phonenum_already_register(self):
        response = self.client.post("/register", data = {'phonenum': '123', 'username': 'TestRegister', 'password': '111', 'password1': '111'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 3)
    # 测试注册成功
    def test_register_success(self):
        response = self.client.post("/register", data = {'phonenum': '111', 'username': 'TestRegister', 'password': '111', 'password1': '111'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 0)


# 测试忘记密码页面
class Test_forget(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    # 测试手机号码、用户名和密码输入全空
    def test_phonenum_username_password_empty(self):
        response = self.client.post("/forget", data = {'phonenum': '', 'username': '', 'password': '', 'password1': ''})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试手机号码输入为空
    def test_phonenum_empty(self):
        response = self.client.post("/forget", data = {'phonenum': '', 'username': 'TestLogin','password': '11', 'password1': '11'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试用户名输入为空
    def test_username_empty(self):
        response = self.client.post("/forget", data = {'phonenum': '11', 'username': '', 'password': '11', 'password1': '11'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试密码输入为空
    def test_password_empty(self):
        response = self.client.post("/forget", data = {'phonenum': '11', 'username': 'TestForget_Wear', 'password': '', 'password1': ''})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试两次输入密码不一致
    def test_password_not_equel_password1(self):
        response = self.client.post("/forget", data = {'phonenum': '11', 'username': 'TestForget_Wear', 'password': '11', 'password1': '1'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 2)
    # 测试手机号码还未注册
    def test_phonenum_not_register(self):
        response = self.client.post("/forget", data = {'phonenum': '1234', 'username': '1234', 'password': '1234', 'password1': '1234'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 3)
    # 测试用户名错误
    def test_username_wrong(self):
        response = self.client.post("/forget", data = {'phonenum': '123', 'username': '1234', 'password': '1234', 'password1': '1234'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 4)
    # 测试修改成功
    def test_forget_success(self):
        response = self.client.post("/forget", data = {'phonenum': '11', 'username': 'TestForget_Wear', 'password': '1', 'password1': '1'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 0)


# 测试个人中心页面
class Test_self(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    # 测试取下已佩戴饰品
    def test_takeoff_lucky(self):
        phonenum = '1'
        url = 'http://127.0.0.1:5000/self%3Fphonenum%3D' + phonenum
        posttype = 0
        luckystate = '1'
        response = self.client.post(url, data = {'posttype': posttype, 'state': luckystate, 'name': '人工染色', 'typename': 'stone'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 0)
    # 测试下架已上架饰品
    def test_offshelf_lucky(self):
        phonenum = '1'
        url = 'http://127.0.0.1:5000/self%3Fphonenum%3D' + phonenum
        posttype = 0
        luckystate = '2'
        response = self.client.post(url, data = {'posttype': posttype, 'state': luckystate, 'name': '深红之网', 'typename': 'stone'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试佩戴饰品
    def test_wear_lucky_success(self):
        phonenum = '123'
        url = 'http://127.0.0.1:5000/self%3Fphonenum%3D' + phonenum
        posttype = 0
        luckystate = '00'
        response = self.client.post(url, data = {'posttype': posttype, 'state': luckystate, 'name': '外表生锈', 'typename': 'stone'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 3)
    # 测试佩戴饰品位置已满，佩戴失败
    def test_wear_lucky_fail(self):
        phonenum = '11'
        url = 'http://127.0.0.1:5000/self%3Fphonenum%3D' + phonenum
        posttype = 0
        luckystate = '00'
        response = self.client.post(url, data = {'posttype': posttype, 'state': luckystate, 'name': '枯焦之色', 'typename': 'stone'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 2)
    # 测试未输入上架饰品价格，上架失败
    def test_onshelf_lucky_fail(self):
        phonenum = '1'
        url = 'http://127.0.0.1:5000/self%3Fphonenum%3D' + phonenum
        posttype = 0
        luckystate = '01'
        response = self.client.post(url, data = {'posttype': posttype, 'state': luckystate, 'name': '传说', 'typename': 'stone', 'price': ''})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 4)
    # 测试上架饰品
    def test_onshelf_lucky(self):
        phonenum = '1'
        url = 'http://127.0.0.1:5000/self%3Fphonenum%3D' + phonenum
        posttype = 0
        luckystate = '01'
        response = self.client.post(url, data = {'posttype': posttype, 'state': luckystate, 'name': '传说', 'typename': 'stone', 'price': '1000.0'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 5)
    # 测试取下已佩戴工具
    def test_takeoff_work(self):
        phonenum = '1'
        url = 'http://127.0.0.1:5000/self%3Fphonenum%3D' + phonenum
        posttype = 1
        workstate = '1'
        response = self.client.post(url, data = {'posttype': posttype, 'state': workstate, 'name': '超导体', 'typename': 'machine'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 0)
    # 测试下架已上架工具
    def test_offshelf_work(self):
        phonenum = '1'
        url = 'http://127.0.0.1:5000/self%3Fphonenum%3D' + phonenum
        posttype = 1
        workstate = '2'
        response = self.client.post(url, data = {'posttype': posttype, 'state': workstate, 'name': '狩猎网格', 'typename': 'machine'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试佩戴工具
    def test_wear_work_success(self):
        phonenum = '123'
        url = 'http://127.0.0.1:5000/self%3Fphonenum%3D' + phonenum
        posttype = 1
        workstate = '00'
        response = self.client.post(url, data = {'posttype': posttype, 'state': workstate, 'name': '深红之网', 'typename': 'knife'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 7)
    # 测试佩戴工具位置已满，佩戴失败
    def test_wear_work_fail(self):
        phonenum = '11'
        url = 'http://127.0.0.1:5000/self%3Fphonenum%3D' + phonenum
        posttype = 1
        workstate = '00'
        response = self.client.post(url, data = {'posttype': posttype, 'state': workstate, 'name': '人工染色', 'typename': 'knife'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 6)
    # 测试未输入上架工具价格，上架失败
    def test_onshelf_work_fail(self):
        phonenum = '1'
        url = 'http://127.0.0.1:5000/self%3Fphonenum%3D' + phonenum
        posttype = 1
        workstate = '01'
        response = self.client.post(url, data = {'posttype': posttype, 'state': workstate, 'name': '传说', 'typename': 'knife', 'price': ''})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 4)
    # 测试上架工具
    def test_onshelf_work(self):
        phonenum = '1'
        url = 'http://127.0.0.1:5000/self%3Fphonenum%3D' + phonenum
        posttype = 1
        workstate = '01'
        response = self.client.post(url, data = {'posttype': posttype, 'state': workstate, 'name': '传说', 'typename': 'knife', 'price': '1000.0'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 5)


# 测试商店页面
class Test_store(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    # 测试不能购买自己上架的商品
    def test_buy_self_fail(self):
        phonenum = '3'
        user = '3'
        url = 'http://127.0.0.1:5000/store%3Fphonenum%3D' + phonenum
        posttype = '0'
        response = self.client.post(url, data = {'posttype': posttype, 'user': user, 'name': '深红之网', 'typename': 'crystal'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 0)
    # 测试不能购买已有的饰品
    def test_buy_repeat_lucky(self):
        phonenum = '4'
        user = '3'
        url = 'http://127.0.0.1:5000/store%3Fphonenum%3D' + phonenum
        posttype = '0'
        response = self.client.post(url, data = {'posttype': posttype, 'user': user, 'name': '深红之网', 'typename': 'crystal'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试金币不足，购买饰品失败
    def test_no_money_lucky(self):
        phonenum = '4'
        user = '123'
        url = 'http://127.0.0.1:5000/store%3Fphonenum%3D' + phonenum
        posttype = '0'
        response = self.client.post(url, data = {'posttype': posttype, 'user': user, 'name': '传说', 'typename': 'stone'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 2)
    # 测试购买饰品
    def test_buy_lucky(self):
        phonenum = '4'
        user = '3'
        url = 'http://127.0.0.1:5000/store%3Fphonenum%3D' + phonenum
        posttype = '0'
        response = self.client.post(url, data = {'posttype': posttype, 'user': user, 'name': '都市伪装', 'typename': 'crystal'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 3)
    # 测试不能购买已有的工具
    def test_buy_repeat_work(self):
        phonenum = '4'
        user = '3'
        url = 'http://127.0.0.1:5000/store%3Fphonenum%3D' + phonenum
        posttype = '1'
        response = self.client.post(url, data = {'posttype': posttype, 'user': user, 'name': '澄澈之水', 'typename': 'pliers'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试金币不足，购买工具失败
    def test_no_money_work(self):
        phonenum = '4'
        user = '123'
        url = 'http://127.0.0.1:5000/store%3Fphonenum%3D' + phonenum
        posttype = '1'
        response = self.client.post(url, data = {'posttype': posttype, 'user': user, 'name': '传说', 'typename': 'knife'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 2)
    # 测试购买工具
    def test_buy_work(self):
        phonenum = '4'
        user = '3'
        url = 'http://127.0.0.1:5000/store%3Fphonenum%3D' + phonenum
        posttype = '1'
        response = self.client.post(url, data = {'posttype': posttype, 'user': user, 'name': '青竹', 'typename': 'shovel'})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 3)


# 测试每日收获页面
class Test_daily(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    # 测试开启宝箱（满足间隔时间）
    def test_openbox_success(self):
        posttype = '0'
        phonenum = '2'
        url = 'http://127.0.0.1:5000/daily%3Fphonenum%3D' + phonenum
        response = self.client.post(url, data = {'posttype': posttype})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 0)
    # 测试开启宝箱（不满足间隔时间）
    def test_openbox_fail(self):
        posttype = '0'
        phonenum = '2'
        url = 'http://127.0.0.1:5000/daily%3Fphonenum%3D' + phonenum
        response = self.client.post(url, data = {'posttype': posttype})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 1)
    # 测试开始赚钱（满足间隔时间）
    def test_earnmoney_success(self):
        posttype = '1'
        phonenum = '2'
        url = 'http://127.0.0.1:5000/daily%3Fphonenum%3D' + phonenum
        response = self.client.post(url, data = {'posttype': posttype})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 2)
    # 测试开始赚钱（不满足间隔时间）
    def test_earnmoney_fail(self):
        posttype = '1'
        phonenum = '2'
        url = 'http://127.0.0.1:5000/daily%3Fphonenum%3D' + phonenum
        response = self.client.post(url, data = {'posttype': posttype})
        result = json.loads(response.data)
        self.assertIn('code', result)
        self.assertEqual(result['code'], 3)


if __name__ == '__main__':
    unittest.main()
