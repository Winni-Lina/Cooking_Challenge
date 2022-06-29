from recipe import Recipe
import pymysql
from ast import literal_eval


class Recipebook:

    def __init__(self, user_id, user_nickname):
        self.db = pymysql.connect(
            user='',
            password='',
            host='',
            db='',
            charset='utf8'
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

        self.user_id = user_id
        self.user_nickname = user_nickname
        self.difficulty = ['매우 쉬움', '쉬움', '보통', '어려움', '매우 어려움']
        self.like_list = []
        self.try_list = []
        self.load_user_recipelist()

    def create_recipe(self):
        print('━━━━━━━━━━━━━━ 레시피 추가하기 ━━━━━━━━━━━━━━')
        self.cursor.execute('SELECT name FROM Recipelist;')
        result = self.cursor.fetchall()

        name = input('만들 레시피의 이름을 입력해주세요: ')
        for recipe in result:
            if recipe['name'] == name:
                self.show_recipe(name)
                print('이미 존재하는 레시피입니다.')
                return

        new_recipe = Recipe(name)
        new_recipe.set_recipe()
        choose = input('추가하시겠습니까? (1:예 / 2: 아니오): ')
        if choose == '2':
            return
        ingredient = str(new_recipe.ingredient).replace("\'", "\"")
        cookery = str(new_recipe.cookery).replace("\'", "\"")
        self.cursor.execute(
            f"""INSERT INTO Recipelist (name, ingredient, cook_time, cookery, cnt_like, cnt_try, difficulty, adder) VALUES ('{new_recipe.name}', '{ingredient}','{new_recipe.time}','{cookery}', 0, 0, {new_recipe.difficulty}, '{self.user_nickname}');""")
        self.db.commit()
        print("레시피가 추가되었습니다.\n")

    def search_recipe(self):
        print('━━━━━━━━━━━━━━ 레시피 검색하기 ━━━━━━━━━━━━━━')
        recipe_name = input('검색할 레시피 이름을 입력해주세요: ')
        self.cursor.execute(f"SELECT name FROM Recipelist WHERE name LIKE '%{recipe_name}%';")
        result = self.cursor.fetchall()
        searched_list = []
        if len(result) == 0:
            print("관련된 레시피가 없습니다.")
            choose = input('추가하시겠습니까 (1. 예 / 2. 아니오): ')
            if choose == '1':
                self.create_recipe()
            return

        for recipe in result:
            searched_list.append(recipe['name'])

        while True:
            print('━━━━━━━━━━━━━━ 레시피 확인하기 ━━━━━━━━━━━━━━')
            for index, recipe in enumerate(searched_list):
                print(f"{index + 1}. {recipe}")
            choose_recipe = input('어느 레시피를 확인하시겠습니까 (공백 입력시 종료): ')
            if choose_recipe == '':
                return
            else:
                choose_recipe = int(choose_recipe)

            if 0 < choose_recipe <= len(searched_list):
                self.show_recipe(searched_list[choose_recipe - 1])
                self.do_recipe(searched_list[choose_recipe - 1])
            else:
                print('알맞지 않는 값을 입력했습니다. 다시 입력해주세요')

    def show_recipe(self, name):
        print(f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━ {name} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        ingredient = ''
        self.cursor.execute(f"SELECT * FROM Recipelist WHERE name = '{name}';")
        recipe = (self.cursor.fetchall())[0]
        ingredient_list = literal_eval(recipe['ingredient'])

        for ingr in ingredient_list:
            ingredient += f"\t{ingr} {ingredient_list[ingr]}\n"
        print(
            f"요리 이름: {recipe['name']}\t난이도: {self.difficulty[recipe['difficulty']]}\t추가자: {recipe['adder']}\n추가 날짜: {recipe['add_date']}\n요리 재료:\n{ingredient}\n총 조리시간: {recipe['cook_time']}\n좋아요 수: {recipe['cnt_like']}\t도전 수: {recipe['cnt_try']}")

    def do_recipe(self, name):
        do_recipe = input("1. 좋아요 또는 좋아요 취소 / 2. 도전하기 / 공백. 돌아가기 : ")
        if do_recipe == "1":
            if name in self.like_list:
                self.like_list.remove(name)
                self.cursor.execute(f"UPDATE Recipelist SET cnt_like = cnt_like - 1 WHERE name = '{name}';")
                self.db.commit()
            else:
                self.like_list.append(name)
                self.cursor.execute(f"UPDATE Recipelist SET cnt_like = cnt_like + 1 WHERE name = '{name}';")
                self.db.commit()
        elif do_recipe == "2":
            if name in self.try_list:
                pass
            else:
                self.try_list.append(name)
                self.cursor.execute(f"UPDATE Recipelist SET cnt_try = cnt_try + 1 WHERE name = '{name}';")
                self.db.commit()
            self.try_recipe(name)
        else:
            return



    def try_recipe(self, name):
        print(f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━ {name} 도전하기! ━━━━━━━━━━━━━━━━━━━━━━━━━━━━')

        self.cursor.execute(f"SELECT cookery FROM Recipelist WHERE name = '{name}'")
        cookery = literal_eval((self.cursor.fetchall()[0])['cookery'])
        page = 1

        while 0 < page <= len(cookery):
            print(f"━━━ {page}단계 ━━━")
            print(f"{cookery[page]}")
            choose = input("1. 이전 단계 2. 다음 단계 3. 도전 멈추기 : ")
            if choose == '1':
                if page == 1:
                    print('첫번째 단계입니다.')
                else:
                    page -= 1
            elif choose == '2':
                if page == len(cookery):
                    print('마지막 단계입니다.')
                else:
                    page += 1
            else:
                return

    def show_categories(self):
        while True:
            choose = self.choose_category()

            if choose == '':
                break
            else:
                choose = int(choose)

            if 0 < choose <= 5:
                self.show_category_recipe(choose)

    def choose_category(self):
        print('━━━━━━ 카테고리 메뉴 ━━━━━━')
        print("1. 인기 레시피")
        print("2. 신규 레시피")
        print("3. 쉬운 난이도순 레시피")
        print("4. 시도한 레시피")
        print("5. 좋아요를 표시한 레시피")

        category_choose = input("원하는 카테고리를 선택해주세요(공백을 입력하면 메뉴로 돌아갑니다):")

        return category_choose

    def show_category_recipe(self, category_num):
        name_list = []
        page = 1

        # 인기, 신규, 쉬운, 시도, 좋아요
        if 0 < category_num <= 3:
            if category_num == 1:
                self.cursor.execute(f"SELECT name FROM Recipelist ORDER BY cnt_like desc, cnt_try desc;")
                result = self.cursor.fetchall()
            elif category_num == 2:
                self.cursor.execute(f"SELECT name FROM Recipelist ORDER BY add_date desc;")
                result = self.cursor.fetchall()
            elif category_num == 3:
                self.cursor.execute(f"SELECT name FROM Recipelist ORDER BY difficulty;")
                result = self.cursor.fetchall()
            for recipe in result:
                name_list.append(recipe['name'])
        else:
            if category_num == 4:
                name_list = self.try_list
            else:
                name_list = self.like_list

        while 0 < page <= len(name_list):
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 현재 페이지 : {page} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            self.show_recipe(name_list[page - 1])

            choose = input('1. 이전 페이지 / 2. 다음 페이지 / 3. 레시피 추가 기능 / 공백. 돌아가기 : ')

            if choose == '1':
                if page == 1:
                    print('첫번째 페이지입니다.')
                else:
                    page -= 1
            elif choose == '2':
                if page == len(name_list):
                    print('마지막 페이지입니다.')
                else:
                    page += 1
            elif choose == '3':
                if name_list[page - 1] in self.try_list:
                    pass
                else:
                    self.try_list.append(name_list[page - 1])
                self.do_recipe(name_list[page - 1])
            else:
                return

    def load_user_recipelist(self):
        self.cursor.execute(
            f"SELECT user_id, try_list, like_list FROM UserRecipelist WHERE user_id = '{self.user_id}';")
        user_list = self.cursor.fetchall()

        for user in user_list:
            if user['user_id'] == self.user_id:
                self.try_list = user['try_list'].split(':')
                self.like_list = user['like_list'].split(':')
                if '' in self.try_list:
                    self.try_list = []
                if '' in self.like_list:
                    self.like_list = []
                return

        self.cursor.execute(
            f"INSERT INTO UserRecipelist (user_id, try_list, like_list) VALUES ('{self.user_id}', '', '');")
        self.db.commit()

    def save_and_end(self):
        like_recipe = ":".join(self.like_list)
        try_recipe = ":".join(self.try_list)
        self.cursor.execute(
            f"UPDATE UserRecipelist SET try_list = '{try_recipe}', like_list = '{like_recipe}' WHERE user_id = '{self.user_id}';")
        self.db.commit()
        self.db.close()
        print("좋아요 레시피와 시도한 레시피를 저장합니다.")
