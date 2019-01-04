import tornado.ioloop
import tornado.web
import tornado.httpserver   #单线程的HTTP服务
import tornado.options  # 命令行解析模块，让模块定义自己的选项
from tornado.options import define, options

define('port', default=8000, help='run port', type=int)

class FormHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('form.html')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class RedirectHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect(r'/index')


class InoutHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name', 'no')
        self.write(name)    # 不可以接受列表

    def post(self):
        name = self.get_argument('name', 'no')
        passwd = self.get_argument('password', 'no')
        self.write('姓名：%s， 密码是： %s' %(name, passwd))


class ArgHandler(tornado.web.RequestHandler):
    def get(self, name, age):
        self.write('name: %s <br> age: %s' % (name, age))


class Arg1Handler(tornado.web.RequestHandler):
    def get(self, name, age):
        self.write('name: %s <br> age: %s' % (name, age))


application = tornado.web.Application(
    handlers=[
        (r"/get",InoutHandler),
        (r"/index", IndexHandler),
        (r"/redirect", RedirectHandler),
        (r"/form", FormHandler),
        (r'/arg/(.+)/([0-9]+)', ArgHandler),    #rest风格，位置传参
        (r'/arg1/(?P<name>.+)/(?P<age>[0-9]+)', Arg1Handler),   #rest风格，关键字传参
    ],
    template_path='templates',
    debug=True
)



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
