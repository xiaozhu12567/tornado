import tornado.ioloop
import tornado.web
import tornado.httpserver   #单线程的HTTP服务
import tornado.options  # 命令行解析模块，让模块定义自己的选项
import time
from tornado.options import define, options

import util.ui_methods
import util.ui_modules

define('port', default=8003, help='run port', type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('extend.html', username='zhu',Cal=CalHandler)

    def post(self):
        self.render('extend.html',
                    username='zhu',
                    Cal=CalHandler,     # 模版中可以导入函数和类
                    )


class CalHandler:
    def sum(self, a, b):
        return a + b


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