class Post:
    post_list = []

    def __init__(self, title, body):
        self.title = title
        self.body = body

    @classmethod
    def add_post(cls, title, body):
        if type(title) == type(body) == type('i am str'):
            new_post = cls(title, body)
            cls.post_list.append(new_post)
        else:
            print("제목과 본문은 문자열이여야 합니다!")

    @classmethod
    def read_post_list(cls, read_and_print=False):
        if read_and_print:
            print("\n- 출력 결과 -")
            for p in cls.post_list:
                print(f'제목 - {p.title}', f'- 본문 :{p.body}\n', sep='\n')
        else:
            return cls.post_list

    @classmethod
    def delete_post(cls, is_title='', is_body=''):
        for target in cls.find_post(is_title, is_body):
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
            index = int(input("<!> 검색된 결과가 여러개 입니다. 선택할 요소의 인덱스를 입력하세요\n모두 선택시 a를 입력 : ").rstrip())
            if 0 <= index < len(li):
                li = [li[index]]
            else:
                print("불가능한 인덱스입니다! 모두 선택한 상태로 유지합니다...")
        return li


# TODO 아래 부분 부터는 테스트 코드입니다
if __name__ == '__main__':
    # 첫 post 작성 & 출력
    Post.add_post('파이썬 vs 자바', '파이썬을 사랑하지만 내가 가고싶은 회사는 자바를 사랑한다. 회사인가 사랑인가?')
    Post.read_post_list(read_and_print=True)

    # 여러개 post 작성 & 출력
    write_list = [('의문점', '혹시 내가 기초가 부족하여서 이것을 하고 있는가?'),
                  ('늦잠', '일어나보니 12시다. 앞으로도 밤의 시간을 보낼까 아님 아침의 시간을 보낼까?')]
    for param in write_list:
        Post.add_post(param[0], param[1])
    Post.read_post_list(read_and_print=True)

    # 제목이 중복되는 post 작성 & 출력
    Post.add_post('늦잠', '좋은 아침인데 문명이 생각난다. 오늘은 이제 안녕인 것 같다.')
    Post.read_post_list(read_and_print=True)

    # 중복되지 않는 post 삭제 & 출력
    Post.delete_post(is_title='의문점')
    Post.read_post_list(read_and_print=True)

    # 제목이 중복되는 post 삭제 & 출력
    Post.delete_post(is_title='늦잠')
    Post.read_post_list(read_and_print=True)