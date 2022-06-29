import pymysql
from datetime import datetime
import random


class Login:
    def __init__(self):
        self.id = ''
        self.nickname = ''
        self.db_user = pymysql.connect(
            user='',
            password='',
            host='',
            db='',
            charset='utf8'
        )
        self.cursor = self.db_user.cursor(pymysql.cursors.DictCursor)
        self.login_menu()
        self.db_user.close()

    def login_menu(self):
        while True:
            choose = input('무엇을 하시겠습니까? (1. 로그인 / 2. 회원가입) : ')
            if choose == '1':
                self.sign_in()
                if self.id != '':
                    break
            elif choose == '2':
                self.sign_up()
            else:
                print('1번과 2번 중에 선택해주세요.\n')

    def sign_in(self):
        self.cursor.execute('SELECT id, user_nickname, user_id, user_password FROM Userdb;')
        db_list = self.cursor.fetchall()

        if len(db_list) == 0:
            print('아직 회원가입한 유저가 없습니다. 회원가입해주세요!')
            return

        while True:
            print('━━━━━━━━━━━━━━ 로그인 ━━━━━━━━━━━━━━')
            user_id = input('아이디를 입력해주세요: ')
            user_password = input('비밀번호를 입력해주세요: ')

            for user in db_list:
                if user['user_id'] == user_id:
                    if user['user_password'] == user_password:
                        self.id = user['id']
                        self.nickname = user['user_nickname']
                        print('로그인에 성공하셨습니다.')
                        return

            print('아이디 또는 비밀번호가 잘못되었습니다. 다시 입력해주세요')

    def sign_up(self):
        while True:
            print('━━━━━━━━━━━━━━ 회원가입 ━━━━━━━━━━━━━━')
            new_user_name = input('사용할 닉네임을 입력해주세요: ')
            new_user_id = input('사용할 아이디를 입력해주세요: ')
            new_user_pw = input('사용할 비밀번호를 입력해주세요: ')

            self.cursor.execute("select id, user_id from Userdb;")
            db_list = self.cursor.fetchall()
            new_id = datetime.today().strftime("%Y%m%d%H%M%S") + str(random.randint(10000, 99999))

            if len(db_list) == 0:
                sql = f"INSERT INTO Userdb (id, user_nickname, user_id, user_password) VALUES ('{new_id}', '{new_user_name}', '{new_user_id}', '{new_user_pw}');"
                self.cursor.execute(sql)
                self.db_user.commit()
                print('회원가입에 성공하셨습니다.')
                return

            for user in db_list:
                if user['user_id'] == new_user_id:
                    print('같은 아이디가 이미 존재합니다. 다른 아이디를 사용해주세요.')
                    return

                sql = f"INSERT INTO Userdb (id, user_nickname, user_id, user_password) VALUES ('{new_id}', '{new_user_name}', '{new_user_id}', '{new_user_pw}');"
                self.cursor.execute(sql)
                self.db_user.commit()
                print('회원가입에 성공하셨습니다.')
                return
