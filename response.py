import tornado.ioloop
import tornado.web
import tornado.httpserver   #单线程的HTTP服务
import tornado.options  # 命令行解析模块，让模块定义自己的选项
from tornado.options import define, options

define('port', default=8001, help='run port', type=int)

class IndexHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print(' ---set_default_headers---: 设置好默认的响应头')

    def initialize(self):
        print('---initialize---: 初始化')

    def prepare(self):
        self.write('---prepare---: 准备工作')

    def get(self):
        self.write('---get---: 处理get请求')

    def post(self):
        self.write('---post---: 处理post请求')

    def write_error(self, status_code, **kwargs):
        print('---write---error: 处理错误')

    def on_finish(self):
        print('---on_finish---: 结束，释放资源')


class HeaderHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('set header')
        self.set_header('aaa', '111')   #设置响应头,不可重复


class AddHeaderHandler(tornado.web.RequestHandler):
    def get(self):
        self.add_header('aa', '111')    #设置响应头，可以重复添加
        self.add_header('aa', '222')    #设置响应头，可以重复添加
        self.clear_header('aa')                #清除header


class SendErrorHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('send error')
        self.send_error(404)

    def write_error(self, status_code, **kwargs):
        self.write('页面丢失，状态码：%s' % status_code )


class NotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        self.send_error(404)

    def write_error(self, status_code, **kwargs):
        self.write('页面丢失，状态码：%s' % status_code )

application = tornado.web.Application(
    handlers=[
        (r"/index",IndexHandler),
        (r"/main",HeaderHandler),
        (r"/add",AddHeaderHandler),
        (r'/send', SendErrorHandler),
#        (r'/(.*)', NotFoundHandler),        # 找不到的路由返回404的错误
    ],
    template_path='templates',
    debug=True
)



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()