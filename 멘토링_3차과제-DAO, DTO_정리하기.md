DAO, DTO란 무엇일까?

은근히 생소한 용어라서, 다른 백엔드 친구한테 물어보니까 JAVA 쓰는 얘들은 확실히 알려주더라구요,  
다시한번 용어에 대해 무지함을 되돌아 보았습니다 ㅎㅎ ^^;;

# DAO, DTO, VO

처음보는 단어라면 꽤 난해할 것이다. 그러나, 단어 뜻을 풀어쓰면 금세 어떤 용어인지 알 수 있다.

- **DAO(Data Access Object)** : 데이터(Data)를 접근(Access)하기위해 생성된 객체(Object)
  = DB 접근 로직과, 비즈니스 로직을 구분하기 위해 사용
  = 간단하게는 DB 접속해 데이터 조회, 조작(CRUD) 기능을 해주는 클래스
  = DB 세부적인 내용을 노출할 필요없이 데이터 조작 기능 제공
- **DTO(Data Transfer Object)** : 계층간 데이터(Data) 전달(Transfer)을 위한 객체(Object)
  = 다른 시스템(DB, 파일, 메모리 등)의 데이터를 접속할 수 있는 객체
  = 로직 없는 순수한 데이터의 객체 (객체에는 객체 속성과 getter, setter 만 존재)
  = 웹 서비스에서 다른 시스템(DB)이 필요할 때마다 호출하면 시간이 소모되서, 데이터를 모으는 DTO를 이용 -> 한번만 호출하게 함

- **VO(Value Object)** : DTO랑 같은 뜻인데, **읽기 전용(Read Only)** 특성 가짐 (DTO랑 자주 혼용)
  = 대체로 불변성 특징 (자바에서 equals()로 비교시 객체 모든 값을 비교해야 한다고함)

## 장고에서 DAO, DTO란?

단순히 내 추측에 안주하지 않고, 다양한 자료들을 찾아보았지만,
현재 결론으론, **장고는 DTO 하나만 만들면, DAO, 테이블이 자동 생성** 된다고 정리했다.

- 장고 **DTO**

  장고의 DTO는 다름아닌, 애플리케이션에 있는 ```models.py``` 에 담겨있다.

  ```
  (프로젝트 폴더)
  ├───manage.py
  └───(프로젝트 기본 폴더)
          settings.py
          urls.py
          wsgi.py
          __init__.py
  └───(애플리케이션A 폴더)
          ├── migrations
          ├── __init__.py
          ├── admin.py
          ├── models.py
          ├── tests.py
          └── views.py
  ```

  설명에 앞서서, 장고 프로젝트의 구조를 보면,
  프로젝트 기본 파일이 1개 있으면, 애플리케이션은 그 프로젝트에서 N개 만큼 있을 수 있고, 
  각 애플리케이션은 기본적으로 파일들이 있는데,  

  그 중 ```models.py``` 는 해당 애플리케이션에서 사용할 **모델**을 작성할 수 있는데, 
  **django.db.models.Model**을 상속받아 작성한 모델 객체가 **DTO**다.

  ```python
  # models.py
  from django.db import models
  
  
  class Users(models.Model):
      email = models.CharField(primary_key=True, max_length=80)
      hashed_password = models.CharField(max_length=120)
      created_at = models.DateTimeField()
  
      class Meta:
          managed = False
          db_table = 'users'
  
  
  class Profiles(models.Model):
      user_email = models.OneToOneField(Users, on_delete=models.CASCADE, db_column='user_email', primary_key=True)
      name = models.CharField(max_length=80)
      profile_image = models.CharField(max_length=120)
      cover_image = models.CharField(max_length=120)
      about_me = models.CharField(max_length=100)
  
      class Meta:
          managed = False
          db_table = 'profiles'
  ```

  그리고 이것을 ```migrate``` 하면, 실제 DB에도 DTO와 같은 테이블이 생성되며, 
  거꾸로 테이블을 ```python manage.py inspectdb ``` 명령어로, 장고 모델(DTO)으로 자동 생성할 수 있다.

  ```bash
  (myvenv) C:\project_path\project>python manage.py inspectdb
  # This is an auto-generated Django model module.
  # You'll have to do the following manually to clean this up:
  #   * Rearrange models' order
  #   * Make sure each model has one field with primary_key=True
  #   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
  #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
  # Feel free to rename the models, but don't rename db_table values or field names.
  from django.db import models
  
  
  class AuthGroup(models.Model):
      name = models.CharField(unique=True, max_length=150)
  
      class Meta:
          managed = False
          db_table = 'auth_group'
  ```

  - 장고 **DAO**

    아까 DTO를 장고 모델로 생성하면, 테이블과 DAO가 자동으로 생성된다 했었고,
    DTO과 테이블이 서로를 자동 생성 할 수 있는 것은 위에서 보았었다.

    그럼 장고의 DAO는 어딨을까?

    장고에는 **기본(디폴트)으로 모델 클래스의 DB 데이터를 CRUD 할 수 있는 Model Manager(모델 매니저) 가 존재한다.**

    ```모델클래스명.objects``` 와 같이하면, 해당 모델 클래스의 **기본 모델 매니저**를 반환하며,

    이 뒤에, 기본 모델 매니저가 가지고 있는 다양한 메소드들로 쿼리문을 생성해, CRUD 를 할 수 있으며,  
    이 **SQL을 생성해주는 인터페이스를 쿼리셋(Query Set)** 이라고 하며, **모델 매니저(Model Manager)를 통해서 해당 Model의 쿼리셋을 구할 수 있다.** 따라서 그 역할에 맞는 SQL문을 생성한다.

    ```python
    Post.objects.all() 		# “SELECT * FROM post…” 와 같은 SQL문 생성
    Post.objects.create()	# “INSERT INTO post VALUES(…)” 와 같은 SQL문 생성
    ```

    이미 모델 매니저에서 제공하는 메소드도 엄청 많은데,

    ```markdown
    ## 모델 객체를 반환하는 메서드
    count() : 데이터의 개수 반환 
    first() :첫번째 객체 반환 
    last() :마지막 객체 반환 
    update() :지정한 필드만 갱신(일부 데이터만 변경하더라도 save()로 저장하면 모델의 필드 전체 변경. update를 이용할 경우 변경된 필드만 업데이트) 
    delete() : 데이터베이스 삭제 
    get_or_create(조건, default=생성할 데이터의 값): 지정한 데이터를 가져오되 없을 경우 생성. 생성될 데이터의 값은 dict 객체로 지정 
    update_or_create(조건, default = 생성할 데이터의 값) : 업데이트하거나 없으면 생성
    
    ## queryset 객체를 반환하는 메서드
    all() : 모든 데이터를 query set으로 반환 
    filter(조건) : 조건식으로 데이터를 찾는다. 
    exclude(조건) : 조건에 일치 하지 않는 데이터 
    order_by(정렬필드) : 지정한 필드를 기준으로 오른차순정렬. 내림차순은 '-'를 붙여주면된다. 
    distinct(필드이름) : 필드 이름이 같은 것이 있다면 겹치지 않게 가져오기
    
    ## 필터링에서 추가할 수 있는 조건
    -exact : 정확히 같은 데이터를 탐색 
    -iexact: 대소문자 무시하고 같은 데이터 탐색 
    -contains : 지정한 문자열을 포함하는 데이터 탐색 
    -icontains: 대소문자 무시하고..
    -in : 리스트나 튜플 자료형이 있는 값들에 해당하는 데이터 탐색 
    -gt : 지정한 값을 초과하는 데이터(greater than) 
    -gte : 지정한 데티어 이상 
    -it : 지정한 값미만 (less than) 
    -lte : 지정한 값 이하 
    -startswith : 지정한 문자열로 시작하는 데이터 
    -istartswith : 대소문자 무시하고... 
    -endswith : 지정한 문자열로 끝나는 
    -iendswith : 대소문자 무시하고... 
    -range : 범위에 해당하는 데이터 탐색. 리스트나 튜플로 지정 
    -year: dateField와 DateTimeField와 대응하여 지정년도의 데이터탐색 
    -month : 지정한 월 
    -week_day : 지정한 요일, 1은 일요일 7은 토요일 
    -hour, minute, secoond: 시,분, 초 지정) 
    -isnull: null 인 데이터 탐색(true 와 False 지정) 
    -search : contains와 비슷하지만 데이터베이스의 full-text indexing을 이용하여 좀더 빠르게 처리 -regex : 정규 표현식으로 데이터 탐색 
    -iregex: 대소문자 무시하고 ...
    ```

    이외에도 내가 추가하고 싶은 메소드가 있다면, ```models.Manager``` 를 상속하는 클래스로 해서, 직접 **모델 매니저**를 만들어 주고, 그것을 적용할 모델 클래스에, ```objects = 모델매니저이름()``` 과 같이 정의해주면, 그 모델 클래스는 직접 만들어준 모델 매니저를 사용할 수 있다.

    [참고 (장고 공식 문서)](https://docs.djangoproject.com/en/1.10/topics/db/managers/)

    이렇게 해서, 장고에서도 비즈니스 로직과, DB 접근 로직을 분리해서, DB 조회및 조작 로직을 **모델 매니저** 를 활용해 구현해 줄 수 있다.

    

## Reference

- https://iri-kang.tistory.com/5 : DAO, DTO, VO 개념
- https://genesis8.tistory.com/214 : DAO, DTO, VO 개념2
- https://m.blog.naver.com/ljc8808/220462395989 : DAO, DTO, VO 개념3
- https://m.blog.naver.com/PostView.nhn?blogId=youhr21&logNo=221590012242&categoryNo=40&proxyReferer=https:%2F%2Fwww.google.com%2F : 장고 DAO, DTO 설명
- https://docs.djangoproject.com/en/1.10/topics/db/managers/ : 장고 model Manager 공식 문서
- https://wayhome25.github.io/django/2017/04/01/django-ep9-crud/ : 장고 model Manager (DAO?)
- https://stackoverflow.com/questions/42295039/model-manager-class-for-dao-or-not-in-django : 장고 DAO (스텍오버플로우)
- https://www.programmersought.com/article/2814636229/ : 장고 DAO (외국자료)

