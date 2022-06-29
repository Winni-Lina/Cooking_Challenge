from recipebook import Recipebook
from login import Login


def user_choose():
    print("━━━━ 메뉴 ━━━━")
    print("1. 검색하기")
    print("2. 추가하기")
    print("3. 둘러보기")
    print("4. 종료하기")
    choose = input("메뉴를 선택하세요: ")
    return choose


def main():
    user = Login()
    my_id = user.id
    my_nickname = user.nickname
    use_recipebook = Recipebook(my_id, my_nickname)

    while True:
        choose = user_choose()
        if choose == '1':
            use_recipebook.search_recipe()
        elif choose == '2':
            use_recipebook.create_recipe()
        elif choose == '3':
            use_recipebook.show_categories()
        elif choose == '4':
            use_recipebook.save_and_end()
            print("프로그램을 종료합니다.")
            break


if __name__ == '__main__':
    main()