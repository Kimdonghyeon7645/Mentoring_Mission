class Post:
    def __init__(self, title, body):
        self.title = title
        self.body = body


class Service:
    def __init__(self):
        self.post_list = []

    def add_post(self, title, body):
        if not (title and body):
            print("[!] 제목과 본문은 공백일 수 없습니다!")

        new_post = Post(title, body)
        self.post_list.append(new_post)

    def read_posts(self):
        print("- 출력 결과 -")
        self.get_posts()

    def get_posts(self):
        for ele in self.post_list:
            index = self.post_list.index(ele)
            print(f"{index:>3}번 포스트 \t 제목: {ele.title} / 본문: {ele.body}")

    def delete_post(self, index):
        target = self.post_list[index]
        self.post_list.remove(target)

    def exe_command(self):
        while True:
            print("\n어떤 명령을 실행하시겠습니까? \n(1.글 추가  2.글목록 조회  3.글 삭제  4.프로그램 종료)")
            num = input("(원하는 명령의 숫자를 입력하세요) : ").strip()

            if num == '1':
                t, b = input("글의 제목을 입력하세요 : "), input("글의 본문을 입력하세요 : ")
                self.add_post(t, b)
            elif num == '2':
                self.read_posts()
            elif num == '3':
                index = int(input("삭제할 글의 인덱스를 입력하세요 : "))
                self.delete_post(index)
            elif num == '4':
                print("\n프로그램을 종료합니다......")
                break
            else:
                print("[!] 존재하지 않는 명령 입니다!\n")
                continue


if __name__ == '__main__':
    print("-- 게시판 관리 콘솔 어플리케이션이 정상 실행되었습니다 ^^7 --")
    my_post = Service()
    my_post.exe_command()
