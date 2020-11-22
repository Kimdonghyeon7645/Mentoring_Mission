# Spring Web Application (스프링 웹 어플리케이션) 아키텍쳐

웹 어플리케이션을 만들때, 아무생각없이 코드를 나누지 않고, 하나로 짬뽕해놓으면 어떨까?  
서버를 식당으로 비유하자면, 역할에 따라 분리되지 않은 코드는 **식당에서 요리사가 모든 역할을 하는 꼴이다.**  

식당이 한산하다면 혼자서 모든 역할을 해도 되겠지만, 규모가 큰 식당이라면 어떨까?  
실제 식당에서도 서빙하는 사람, 요리하는 사람, 관리하는 사람이 분리되듯이,  
코드도 역할에 따라 분리할 필요가 있다.

이로써 코드의 **결합도(다른 모듈에 의존하는 정도)** 는 낮추고, **응집도(모듈 내부의 기능이 밀접하게 관련있는 정도)** 는 높일 수 있는 것이다.  
(결합도가 낮을 수록, 응집도는 높을 수록 -> 유지보수성과 가독성이 높아진다.)

## 3-티어 애플리케이션 아키텍쳐

![image](https://user-images.githubusercontent.com/48408417/99790334-4c7fc580-2b67-11eb-84c9-8a26c9d93373.png)
  
### - 웹 레이어(Web Layer, 프리젠테이션 계층)

- **컨트롤러(@Controller)** 와 JSP/타임리프 등의 **뷰 템플릿** 이 사용되는 영역
- 이것 말고도, 필터(@Filer), 인터셉터, 컨트롤러 어드바이스(@ControllerAdvice) 등 **외부 요청을 처리하고 응답을 반환하는 영역**

### - 서비스 레이어(Service Layer, 서비스 계층)

- 일반적으론 컨트롤러(Controller)와 데이터 엑세스 객체(DAO) 사이에서 사용되는 영역
- **@Service**를 쓰는 영역
- 트렌젝션<sup>[1](#트렌젝션)</sup>으로 처리하기 위해서, **@Transactional**(트렌젝션 경계)을 선언하는 영역
- 흔히 비즈니스 로직을 이 영역에서 처리하지만(트렌젝션 스크립트), 도메인 모델에서 로직을 처리하고, 서비스는 **트렌젝션과 도메인 간 순서만 보장**하는 것이 바람직  

### - 레포지토리 레이어(Repository Layer, 데이터 엑세스 계층)

- DB 같은 데이터 저장소에 접근하는 영역
- **DAO(Data Access Object)** 영역으로 이해하면 쉬움

### - DTO(data Transfer Object)

- 위의 3가지 **계층 간에 데이터 교환을 위한 객체 = DTO**, DTO 들의 영역 = **DTOs**   
- 뷰 템플릿에서 사용될 객체, 데이터 엑세스 계층에서 결과로 넘겨준 객체 등이 해당

### - 도메인 모델(Domain Model)

- 도메인<sup>[2](#도메인)</sup> 을 **모든 사람이 동일한 관점으로 이해, 공유 가능하도록 단순화(개념화) 시킨 것 = 도메인 모델**
- 도메인 모델은 3가지 종류의 객체로 구성
    - **엔티티(Entity)** : 영속성(=메모리영역 대신 DB에 저장, 애플리케이션 종료되도 데이터가 유지) 도메인 오브젝트  
        DB의 테이블과 연결되는 객체
    - **VO(Value Object, 값 객체)** : Entity와 비슷한 성격<sup>[3](#VO)</sup>
        - 연속성(=필요에 따라 속성이 변경 가능한지)에 따라, 불변하면 VO로 분류(->내부 프로퍼티를 final로 지정)
        - DB 테이블과 관계가 있을 필요 없음
    - **도메인 서비스(Domain Services)**<sup>[4](#도메인서비스)</sup> : 도메인 주도 개발(DDD)에서 서비스는 엔티티(Entity), 값 객체(Value Object)와 같은 계층에서 오브젝트로 취급되는 것  
        - 객체의 행위, 활동을 표현하는 단위로 사용
        - Aggregate<sup>[5](#Aggregate)</sup> 경계(=트렌젝션) 내의 객체 통제 권한은 Entity, VO 에서 처리 (이미 Entity, VO에서 충분히 다룰 수 있는 기능을 서비스로 제작하면 안됌)  
        - 서로 다른 Aggregate 경계를 가지는 도메인 끼리만 서비스 사용
        

## 주석

<li>    
<a name="트렌젝션">트렌젝션</a> 
: 더이상 쪼갤 수 없는 최소 단위의 작업,<br /> 
<a href="https://happyer16.tistory.com/entry/6-6-%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98-%EC%86%8D%EC%84%B1?category=692836">참고1</a>, 
<a href="https://goddaehee.tistory.com/167">참고2</a> 
</li>

<li>    
<a name="도메인">도메인</a> 
: 소프트웨어로 해결, 구현하고자 하는 문제영역<br />
    <ul>
    ex) 온라인 서점이 구현할 소프트웨어일때, (상품조회, 구매, 배송, 추적등의 기능을 구현할) 온라인 서점 = 도메인, 한 도메인(온라인 서점)은 여러 하위 도메인으로 나뉠 수 있음<br />
    자세한 내용은 DDD, 도메인 공학 참고<br />
    </ul>
<a href="https://medium.com/react-native-seoul/%EB%8F%84%EB%A9%94%EC%9D%B8-%EC%A3%BC%EB%8F%84-%EC%84%A4%EA%B3%84-domain-driven-design-in-real-project-1-%EB%8F%84%EB%A9%94%EC%9D%B8-83a5e31c5e45">참고1</a>, 
<a href="https://12bme.tistory.com/522">참고2</a> 
</li>

<li>    
<a name="VO">VO와 엔티티(Entity)를 분류하는 방법</a> 
: <a href="http://springmvc.egloos.com/624397">참고</a> 
</li>

<li>    
<a name="도메인서비스">도메인 서비스</a> 
: <a href="http://springmvc.egloos.com/726522">참고</a> 
</li>
  
<li>    
<a name="Aggregate">Aggregate</a> 
: <a href="http://blog.naver.com/PostView.nhn?blogId=loopbit&logNo=221201046142&parentCategoryNo=49&categoryNo=56&viewDate=&isShowPopularPosts=false&from=postView">참고</a> 
</li>

