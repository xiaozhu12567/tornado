import tornado.ioloop
import tornado.web
import tornado.httpserver   #单线程的HTTP服务
import tornado.options  # 命令行解析模块，让模块定义自己的选项
import time
from tornado.options import define, options
from tornado.web import authenticated
from pycket.session import SessionMixin


import util.ui_methods
import util.ui_modules
from data.user_module import User
from data.connect import session




define('port', default=8005, help='run port', type=int)


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        # current_user = self.get_secure_cookie('ID')
        current_user = self.session.get('user')
        if current_user:
            return current_user

class SetHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_cookie('cookie_test', 'this_is_test', expires=time.time() + 60)  # 不可以有空格
        self.set_cookie('cookie_test2', 'this_is_test', expires_days=1)
        self.set_cookie('cookie_test3', 'this_is_test', path='/set', expires_days=1)
        self.set_cookie('cookie_test4', 'this_is_test', httponly=True, expires_days=1)    # 设置js不可以获取cookie
        self.set_cookie('cookie_test5', 'this_is_test', max_age=120, expires_days=1)    # 用max_age设置过期时间，以它为准
        self.set_secure_cookie('cookie_test6', 'this_is_test')
        self.write('set cookie')


class GetHandler(tornado.web.RequestHandler):
    def get(self):
        c1 = self.get_cookie('cookie_test')
        print(c1)
        c3 = self.get_cookie('cookie_test')
        print(c3)
        c6 = self.get_secure_cookie('cookie_test6')
        print(c6)
        self.write('get_cookie')


class BuyHandler(BaseHandler):
    @authenticated
    def get(self):
        self.write('sucessful')


class IndexHandler(BaseHandler):
    def get(self):
        next = self.get_argument('next', None)
        self.render('form.html', next=next)


    def post(self):
        username = self.get_argument('name', None)
        user = session.query(User).filter(User.name == username).first()
        passwd = self.get_argument('password', '')
        next = self.get_argument('next',None)

        if user and user.password == passwd:
            # self.set_secure_cookie('ID', username)
            self.session.set('user', user)
            self.redirect(next)
        else:
            self.write('failed')




application = tornado.web.Application(
    handlers=[
        (r"/index",IndexHandler),
        (r"/set", SetHandler),
        (r"/get", GetHandler),
        (r"/buy", BuyHandler),
    ],
    template_path='templates',
    static_path='static',
    debug=True,
    autoescape=None,    # 配置关闭转义
    ui_methods=util.ui_methods,
    ui_modules=util.ui_modules,
    cookie_secret = 'aaa',
    login_url = '/index',
    pycket = {
        'engine': 'redis',
        'storage': {
            'host': '127.0.0.1',
            'port': 6379,
            'db_sessions': 5,   # 会话
            'db_notifications': 11,    # 通知
            'max_connections': 2 ** 31  # 最大连接数
        },
        'cookies': {
            'expires_days': 30,
            'max_age': 100
        }
    },
)



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()