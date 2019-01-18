import tornado.ioloop
import tornado.web
import tornado.httpserver   #单线程的HTTP服务
import tornado.options  # 命令行解析模块，让模块定义自己的选项
import time
from tornado.options import define, options

import util.ui_methods
import util.ui_modules
from data.user_module import User
from data.connect import session

define('port', default=8004, help='run port', type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('form.html')

    def post(self):
        username = self.get_argument('name', None)
        user = session.query(User).filter(User.name == username).first()
        passwd = self.get_argument('password', '')

        if user and user.password == passwd:
            self.write('hehe')
        else:
            self.write('failed')




application = tornado.web.Application(
    handlers=[
        (r"/index",IndexHandler),
    ],
    template_path='templates',
    static_path='static',
    debug=True,
    autoescape=None,    # 配置关闭转义
    ui_methods=util.ui_methods,
    ui_modules=util.ui_modules,
)



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()