from dataclasses import dataclass


@dataclass
class Post:
    title: str
    body: str


class Service:
    def __init__(self):
        self.posts = []

    def add_post(self, title, body):
        if not (title and body):
            raise ValueError("[!] 제목과 본문은 공백일 수 없습니다!")

        new_post = Post(title, body)
        self.posts.append(new_post)

    def read_posts(self):
        print("- 출력 결과 -")
        self.get_posts()

    def get_posts(self):
        for ele in self.posts:
            index = self.posts.index(ele)
            if ele:
                print(f"{index:>3}번 포스트 \t 제목: {ele.title} / 본문: {ele.body}")

    def delete_post(self, index):
        if not index.isdigit():
            raise TypeError("[!] 인덱스는 숫자여야 합니다!")
        if len(self.posts) <= int(index) or not self.posts[int(index)]:
            raise IndexError("[!] 불가능한 범위의 인덱스 입니다!")

        self.posts[int(index)] = None

    def run_service(self):
        while True:
            print("\n어떤 명령을 실행하시겠습니까? \n(1.글 추가  2.글목록 조회  3.글 삭제  4.프로그램 종료)")
            num = input("(원하는 명령의 숫자를 입력하세요) : ").strip()

            try:
                if num == '1':
                    title = input("글의 제목을 입력하세요 : ")
                    body = input("글의 본문을 입력하세요 : ")
                    self.add_post(title, body)
                elif num == '2':
                    self.read_posts()
                elif num == '3':
                    index = input("삭제할 글의 인덱스를 입력하세요 : ")
                    self.delete_post(index)
                elif num == '4':
                    print("\n프로그램을 종료합니다......")
                    break
            except (TypeError, ValueError, IndexError) as e:
                print(e)


if __name__ == '__main__':
    print("-- 게시판 관리 콘솔 어플리케이션이 정상 실행되었습니다 ^^7 --")
    my_post = Service()
    my_post.run_service()
