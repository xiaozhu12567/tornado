import tornado.ioloop
import tornado.web
import tornado.httpserver   #单线程的HTTP服务
import tornado.options  # 命令行解析模块，让模块定义自己的选项
import time
from tornado.options import define, options

define('port', default=8002, help='run port', type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('form.html')

    def post(self):
        name = self.get_argument('name', 'no')
        at="<a href='https://www.baidu.com' target='_blank'> 百度</a><br>"
        self.render('template.html',
                    username=name,
                    time=time,
                    at=at
                    )


application = tornado.web.Application(
    handlers=[
        (r"/index",IndexHandler),
    ],
    template_path='templates',
    static_path='static',
    debug=True,
    autoescape=None,    # 配置关闭转义
)



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()