from connect import session
from user_module import User

def add_user():
#    person = User(name='zhu', password="123")
#    sesion.add(person)  # 添加一个
    session.add_all(
        [
            User(name='jia', password="456"),
            User(name='fu', password="789"),
            User(name='zhu', password="789"),
            User(name='test', password="ed789"),
            User(name='haha', password="sd789"),
            User(name='xixi', password="sd989"),
        ]
    )
    session.commit()

def search_user():
    rows = session.query(User).all()
    print(rows)

def update_user():
    rows = session.query(User).filter(User.name=='zhu').update({User.password:1234})
    print(rows)
    session.commit()

def delete_user():
    row = session.query(User).filter(User.name=='jia')[0]
    print(row)
    session.delete(row)
    session.commit()

if __name__ == '__main__':
    add_user()