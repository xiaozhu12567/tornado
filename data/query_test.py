from connect import session
from user_module import User, UserDetails
from sqlalchemy import desc, func, extract, or_

# 查询结果
# rs = session.query(User).filter(User.name == 'jia')     #看sql语句，是一个query对象
# rs = session.query(User).filter(User.name == 'jia').all()     #返回一个sql查询的结果类的实例，类型是列表，需要索引取值
# rs = session.query(User).filter(User.name == 'jia').first()     #返回一个sql查询的结果类的实例，类型是具体实例，不要索引取值，但是query中不是表，就需要加索引取值
# rs = session.query(User).filter(User.name == 'jia')[0]     #等同于all()查询后的索引取值
# print(rs.name, getattr(rs, 'name'))      #取值的两种方法
#
# 查询条件
# print(session.query(User).filter(User.name == 'jia'))     # filter和filter_by是过滤函数，相当于where，
# print(session.query(User).filter_by(name = 'jia'))     # 函数传参，只能是"="号；不用写表名
# print(session.query(User).filter(User.name.like('ji%')).all())     # like和notlike模糊匹配
#
# print(session.query(User).filter(User.password.in_(['123', '456'])).all())  # sql中的in和notin在sqlalchemy中使用in_代替，不要轻易使用in，消耗大，慢
# print(session.query(User).filter(User.password.is_(None)).all())  # is和isnot判断是否为空
#
# print(session.query(User).limit(2).all())       # limit用法，限制查询条数
# print(session.query(User).offset(1).all())      # offset 用法, 偏移量
# print(session.query(User).slice(1,5).all())      # slice 用法, 切片
#print(session.query(User).filter(User.name == 'jia').one())   # 判断值是不是唯一，如果是打印出来，不是返回报错异常

# print(session.query(User).order_by(desc(User.id)).all())  # 排序和升降序
# print(session.query(User.password, func.count("*")).group_by(User.password).having(func.count("*") > 1).all())  # group_by 分组统计和having分组过滤
print(session.query(extract('minute',User.createtime).label('minute'), func.count("*")).group_by('minute').all())  # group_by 分组统计和having分组过滤

# 多表查询
print(session.query(User, UserDetails).all()) # cross join 笛卡尔全集
print(session.query(User, UserDetails.last_login).join(UserDetails, UserDetails.id == User.id)) # inner join
print(session.query(User, UserDetails.last_login).outerjoin(UserDetails, UserDetails.id == User.id)) # outer join也是左连接

q1 = session.query(User.id)
q2 = session.query(UserDetails.id)
print(q1.union(q2).all())       # 联合后不会出现相同的数据

sql_0 = session.query(UserDetails.last_login).subquery()
print(session.query(User, sql_0.c.last_login).all())        # 子查询语法，.c.必须这样写

# 原生sql
sql_1 = """select * from user"""
rows = session.execute(sql_1)
# print(rows, dir(rows))
print(rows.fetchone())  #取一条数据
print(rows.fetchmany()) #列表取所有数据
print(rows.fetchall())

for i in rows:
    print(i)
