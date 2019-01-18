from datetime import datetime
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from .connect import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    password = Column(String(50))
    createtime = Column(DateTime, default=datetime.now)
    _locked = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return 'User(id=%s, name=%s, password=%s, createtime=%s, _locked=%s)' % (
            self.id,
            self.name,
            self.password,
            self.createtime,
            self._locked
        )


class UserDetails(Base):
    __tablename__ = 'user_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_card = Column(Integer, nullable=False, unique=True)
    last_login = Column(DateTime)
    login_num = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('user.id'))

    userdetails = relationship('User', backref='details', uselist=False, cascade='all') # 声明一下表关系，第一个传入关系表的类，第二个参数向关系表中添加新属性，第三个参数是声明表关系的，默认一对多，等于flase是一对一，第四个参数是级联


    def __repr__(self):
        return 'User(id=%s, id_card=%s, last_login=%s, login_num=%s, user_id=%s)' % (
            self.id,
            self.id_card,
            self.last_login,
            self.login_num,
            self.user_id
        )


user_article = Table('user_article', Base.metadata,
                     Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
                     Column('article_id', Integer, ForeignKey('article.id'), primary_key=True),     # 联合主键
                     )

class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(500), nullable=True)
    create_time = Column(DateTime, default=datetime.now)

    article_user = relationship('User', backref='article', secondary=user_article)

    def __repr__(self):
        return "Atricle(id:%s, content:%s, create_time:%s)" %(
            self.id,
            self.content,
            self.create_time
        )


if __name__ == '__main__':
    Base.metadata.create_all()