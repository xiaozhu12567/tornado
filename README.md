# tornado

导入模块的顺序是内置模块、第三方模块、自定义模块

转义
tornado自动转义
1）在模版中全局关闭转义：{% autoescape None %}
2）在模版中局部关闭转义：{{ raw variables }}
3）在模版中设置全局关闭转义后，局部开启转义：{{ escape(variables) }}
4）在py文件中设置全局关闭转义：在application中添加autoescape=None

模版的引入
{% block ti %}base{% end %}
{% extends ./base.html %}
{% include  ./include.html %}

发送错误吗
class SendErrorHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('send error')
        self.send_error(404)

    def write_error(self, status_code, **kwargs):
        self.write('页面丢失，状态码：%s' % status_code )


静态文件的引入
在py文件中的application中配置完static_path后有两种方法引入
1）src="{{static_url('img/XX.jpg')}}"    带有version信息
2）src="/static/img/template.jpg"   其中static为关键字


设置ui_module和ui_methods
1）在项目同级目录下新建util文件夹，并在其中创建ui_methods.py和ui_modules.py
2）在ui_methods.py中编写函数，注意一定要加上self
    def methods1(self):
        return 'ui_methods1'
3）在ui_modules.py中编写类，注意继承UIModule，和重写render方法，其中还有css_files和javascript_files方法
    from tornado.web import UIModule

    class UiModule(UIModule):
        def render(self, *args, **kwargs):
            return '我是 UI_Module'
4）在外层的py文件中导入上述两个文件，并在application中配置ui_methods和ui_modules
5）在模版html中使用，示例如下：
  {{ methods1() }}
  {% module UiModule() %}
  

ORM
1）安装软件
pip install pymysql
pip install sqlalchemy

2）配置连接器
创建data目录，并新建connect.py文件

from sqlalchemy import create_engine

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'mydb'
USERNAME = 'root'
PASSWORD = '123.coM'

db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE
)

engine = create_engine(db_url)

#创建Base类
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(engine)


3）创建module
查看data/user_module.py文件

4）多表查询
cross join、inner join、left join、right join
on要优于where
左连接查询出来的数据条目以左侧表为准
sqlalchemy中没有右连接

5）sqlalchemy常用方法
见data下的query_test.py

6）表关系
外键不能表示表关系，是一个约束而已
表之间的关系是创建表的人加上去的
在相信信息表的module中添加如下属性，配合foreginkey使用，foreginkey在哪里就是正向查询
from sqlalchemy.orm import relationship
userdetails = relationship('User', backref='details', uselist=False, cascade='all')
参数说明：声明一下表关系，第一个传入关系表的类；
         第二个参数向关系表中添加新属性；
         第三个参数是声明表关系的，默认一对多，等于flase是一对一；
         第四个参数cascade是级联，与删除操作有关系
cascade可选参数：
         all，所有操作都会自动处理到关联对象上
         save-update，关联对象自动添加到会话
         delete，关联对象自动从会话中删除
         delete-orphan，属性中去掉关联对象，则会话中会自动删除关联对象
         merge，session.merge()时会处理关联对象
         expunge，session.expunge()时会处理关联对象

一对一：用户基本信息表和用户详细信息表
一对多：一个人与自己写的多篇文章的关系
多对多：多个人与多篇文章的关系

多对多关系表需要先创建中间表，然后使用relationship的secondary关键字

包管理：
1）在文件夹中创建__init__.py文件（python3已经是非必须的）
2）包内的自定义模块引入需要使用相对路径，就是加".",例如：from .connect import Base
3）包内的模块不能直接调用,只能引用


cookie
set_cookie(名，内容，expires=秒)
set_cookie(名，内容，expires_days=天)
set_cookie(名，内容，path='/', expires_days=天)   # 告诉浏览器，访问那些路由会发送该cookie
set_cookie(名，内容，httponly=True, expires_days=天) # cookie不可以被js读取
set_cookie(名，内容，max_age=120)    # 一般使用max_age设置过期时间，单位为秒
set_secure_cookie('cookie_test6', 'this_is_test')   # 设置加密cookie，必须在application中先定义cookie_secret
get_cookie和get_secure_cookie

登陆页面
判断是否存在cookie，如果不存在返回到登陆页面，登陆成功后，返回上一个页面
1）导入模块
from tornado.web import authenticated

2）创建BaseHandler，重写get_current_user方法
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        current_user = self.get_secure_cookie('ID')
        if current_user:
            return current_user

3）将所有handler中继承的类改成为BaseHandler，并引用装饰器
class BuyHandler(BaseHandler):
    @authenticated
    def get(self):
        self.write('sucessful')

4）在application中定义login_url = '/index'

5）在登陆成功后，在登陆页面的handler中设置ID的cookie
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('form.html')

    def post(self):
        username = self.get_argument('name', None)
        user = session.query(User).filter(User.name == username).first()
        passwd = self.get_argument('password', '')

        if user and user.password == passwd:
            self.write('登陆成功')
            self.set_secure_cookie('ID', username)
        else:
            self.write('failed')

6）设置返回跳转到登陆页面前的页面
没有登陆的时候会跳转到登陆页面，url后面自动增加了一个next参数，在登陆页面的handler的get中获取到next的值，并传递给渲染的页面中去，然后在post中获取到该值，并重定向即可
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        next = self.get_argument('next', None)
        self.render('form.html', next=next)


    def post(self):
        username = self.get_argument('name', None)
        user = session.query(User).filter(User.name == username).first()
        passwd = self.get_argument('password', '')
        next = self.get_argument('next',None)

        if user and user.password == passwd:
            self.set_secure_cookie('ID', username)
            self.redirect(next)
        else:
            self.write('failed')
            
<form method="post" action="/index?next={{ next }}">
    <p>用户名： <br><input type="text" name="name"></p>
    <p>密码： <br><input type="password" name="password"></p>
    <input type="submit">
</form>

session
将用户信息保存在服务器端（redis键值对形式），返回给用户一个cookie（键）
1）使用redis存放session信息
pip install pycket
pip install redis

2）导入模块
from pycket.session import SessionMixin

3）BaseHandler中增加SessionMixin类的继承
class SetHandler(tornado.web.RequestHandler):

4）在application中增加连接redis的配置
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

5）修改IndexHandler中get方法中的set_secure_cookie为session.set
        if user and user.password == passwd:
            # self.set_secure_cookie('ID', username)
            self.session.set('user', user)      # user为数据库查询处理的实例对象
           
6）修改BaseHandler中的current_user取值
        current_user = self.get_secure_cookie('ID') # 修改前
        current_user = self.session.get('user')     # 修改后


XSRF
在form表单的下面添加
{% module xsrf_form_html() %}
会在发送给用户的cookie中多发一个_xsrf,值与form表单中的值一致时，验证才能通过


长轮询
客户端不断的向服务器发送请求
缺点是开销大、浪费资源、浪费流量
案例：电脑上扫码登陆qq，展出二维码后，每隔一段时间向服务器发起请求，问有没有人扫码，如果有人扫了，服务器返回跳转页面，如果没人扫，过段时间二维码失效

websocket(客户端与服务端一直连接)
1）导入websocket
import tornado.websocket

2）重写基类
改写BaseHandler中的tornado.web.RequestHandler为tornado.websocket.WebSocketHandler
class BaseWebSocketHandler(tornado.websocket.WebSocketHandler, SessionMixin)
保留原有的BaseHandler

