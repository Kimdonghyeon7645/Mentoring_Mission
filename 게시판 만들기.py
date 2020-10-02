import sys


class Post:
    post_list = []

    def __init__(self, title, body):
        self.title = title
        self.body = body

    @classmethod
    def add_post(cls):
        title = input("추가할 글의 제목을 입력 : ").rstrip()
        body = input("추가할 글의 본문을 입력 : ").rstrip()
        if not (title and body):
            print("[!] 제목과 본문은 공백일 수 없습니다!")
        if not (type(title) == type(body) == type('str')):
            print("[!] 제목과 본문은 문자열이여야 합니다!")

        new_post = cls(title, body)
        cls.post_list.append(new_post)

    @classmethod
    def read_post_list(cls):
        print("\n- 출력 결과 -")
        for p in cls.post_list:
            print(f'- 제목: {p.title}', f'본문: {p.body}\n', sep='\n')

    @classmethod
    def delete_post(cls):
        title = input("삭제할 글의 제목을 입력 (모든 제목 선택시 공백 입력) : ").rstrip()
        body = input("삭제할 글의 본문을 입력 (모든 본문 선택시 공백 입력) : ").rstrip()
        if not (type(title) == type(body) == type('str')):
            print("[!] 제목과 본문은 문자열이여야 합니다!")
        for target in cls.find_post(title, body):
            cls.post_list.remove(target)

    @classmethod
    def find_post(cls, title, body):
        found_list = [p for p in cls.post_list
                      if (p.title == title or not title) and (p.body == body or not body)]
        return cls.choice_post(found_list)

    @staticmethod
    def choice_post(li):
        if len(li) > 1:
            print("\n- 검색결과 -")
            for i, p in enumerate(li):
                print(f'{i}번째 post, 제목 : {p.title}, 본문 : {p.body}')
            index = int(input("[!] 검색된 결과가 여러개 입니다. 선택할 요소의 인덱스를 입력하세요\n(모두 선택시 문자를 입력) : ").rstrip())
            if 0 <= index < len(li):
                li = [li[index]]
            else:
                print("[!] 불가능한 인덱스입니다! 모두 선택한 상태로 유지합니다...")
        return li

    @classmethod
    def exe_command(cls, num):
        commands = {'1': 'add_post', '2': 'read_post_list', '3': 'delete_post'}
        if num == '4':
            print("...프로그램을 종료합니다...")
            sys.exit(0)
        if num not in commands.keys():
            print("[!] 존재하지 않는 명령 입니다!\n")
            return -1
        exec(f"cls.{commands[num]}()")


if __name__ == '__main__':
    print("-- 게시판 관리 콘솔 어플리케이션이 정상 실행되었습니다 ^^7 --\n")
    while True:
        print("어떤 명령을 실행하시겠습니까? \n(1.글 추가  2.글목록 조회  3.글 삭제  4.프로그램 종료)")
        choice = input("(원하는 명령의 숫자를 입력하세요) : ").strip()
        Post.exe_command(choice)
