
class Recipe:
    def __init__(self, name):
        self.name = name
        self.ingredient = {}
        self.time = ""
        self.cookery = {}
        self.kind_difficulty = [1, 2, 3, 4, 5]
        self.difficulty = 0

    def set_ingredient(self):
        while True:
            ingredient = input("재료를 입력해주세요 (재료명 양): ")
            if ingredient == "":
                break
            name, gram = ingredient.split()
            self.ingredient[name] = gram

    def set_time(self):
        self.time = input('총 조리 시간을 입력해주세요: ')

    def set_cookery(self):
        print("조리법을 입력해주세요 (끝내려면 공백을 입력해주시면 됩니다.):")
        page = 1
        while True:
            cookery = input("")
            if cookery == "":
                break
            self.cookery[page] = cookery
            page += 1

    def set_difficulty(self):
        print('1. 쉬움\t2. 조금 쉬움\t3. 보통\t4. 조금 어려움\t5. 어려움')
        while True:
            num = int(input('난이도를 선택해주세요: '))
            if 1 <= num <= 5:
                self.difficulty = num
                return
            else:
                print('잘못 입력하셨습니다.')

    def set_recipe(self):
        self.set_ingredient()
        self.set_time()
        self.set_cookery()
        self.set_difficulty()
        print("레시피가 저장되었습니다.\n")
