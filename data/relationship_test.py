from user_module import User, UserDetails
from connect import session

if __name__ == '__main__':
    # row = session.query(User).get(1)    # 取id为1的方法
    # print(row, dir(row))
    # print(row.details)                  # details中存的是用户表对应详细信息表中的信息

    row2 = session.query(UserDetails).get(2)
    # print(row2, row2.userdetails)

    row3 = session.query(User).get(1)
    print(row3)
    print(row3.article)