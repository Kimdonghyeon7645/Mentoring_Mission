# CDC

CDC(Changed Data Capture)는 데이터 캡처라는 뜻으로,
실시간으로 서로 다른 저장공간(DB)의 데이터를 동기화 해주는 기술이다.

이외에도 CDC는 다양한 정의로 설명되고 있다.

```markdown
- 데이터베이스 내 데이터에 대한 변경을 식별해 필요한 후속처리(데이터 전송, 공유 등)을 자동화하는 기술 (or 설계 기법이자 구조)
-  개별 데이터의 변경분(Transactions, 트렌젝션)만 캡처(추출)하는 기술
```

흔히 CDC라고 하는 것은 DB 로그 기반 CDC를 의미하며,
ETL(Extarct, Transfrom, Load)처럼 소스 DB에서 타겟 DB로 데이터를 전송하는 것은 동일하나, SQL 쿼리문을 직접 보내는 데이터 자체가 아닌, 트렌젝션을 보내는 것에 차이점이 있다.

(물론 CDC가 무조건 DB 로그 기반인 것은 아니다.
CDC의 구현기법에는 아래처럼 7가지가 있을 수 있다. DB(트렌젝션)로그는 그 중 하나다)

<details>
    <summary>CDC의 7가지 구현기법</summary>

    1. Time Stamp on Rows
    
          • 테이블 내 마지막 변경 시점을 기록하는 타임스탬프 칼럼 존재
          • 더 최근의 타임스탬프 값을 갖는 레코드가 발견되면 변경된 것으로 식별
    
     2. Version Numbers on Rows
    
          • 테이블 내 버전을 기록하는 칼럼 존재
          • 더 최근의(=더 높은) 버전을 보유한 레코드가 발견되면 변경된 것으로 식별
    
     3. Status on Rows
    
          • 타임 스탬프 및 버전 넘버 기법에 대한 보완 용도로 활용
          • 타임 스탬프 및 버전에 따라 데이터 변경의 여부를 True/False의 불린(boolean)값으로 저장하는 칼럼 존재
          • 불린(boolean)값을 기반으로 변경 여부 판단
    
     4. Time/Version/Status on Rows
    
          • 타임스탬프, 버전 넘버, 상태 값의 세가지 특성을 모두 활용하는 기법
    
     5. Triggers on Tables
    
          • 데이터베이스 트리거를 활용 사전에 등록(Subscribe)된 다수 대상 시스템(Target)에 변경 데이터를 배포(Publish)하는 형태로 CDC를 구현
          • 데이터베이스 트리거는 시스템 복잡도 증가, 변경 관리의 어려움, 확장성의 감소를 유발하는 등 시스템 유지보수성을 저하시키는 특성이 있음
    
     6. Event Programming
    
          • 데이터 변경 식별 기능을 애플리케이션에 구현
          • 이로인해 애플리케이션 개발 부담과 복잡도를 증가시키나, 다양한 조건에 의해 CDC 매커니즘을 구현
    
     7. Log Scanner on Database
    
          • 트랜잭션 로그에 대한 스캐닝 및 변경 내역에 대한 해석을 통해 CDC 매커니즘을 구현
          • 다수의 서로 다른 데이터베이스를 사용하는 환경에서 적용 시 작업 규모가 증가될 수 있으므로 주의가 필요
          • 장점 : 데이터베이스와 사용 애플리케이션에 대한 영향도 최소화, 변경 식별 지연시간 최소화, 트랜잭션 무결성에 대한 영향도 최소화, 데이터베이스 스키마 변경 불필요

</details>



## 알고가기, 트렌젝션과 트렌젝션 로그

[트렌젝션 로그]([https://ko.wikipedia.org/wiki/%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98_%EB%A1%9C%EA%B7%B8](https://ko.wikipedia.org/wiki/트랜잭션_로그)), DB 방과후에서 **장애와 회복기법** 공부하면서 배웠던 내용이므로, 간단히 정리해도 될 것 같다 ㅎㅎ

**트렌젝션 로그**, 데이터베이스(DB) 로그, 바이너리 로그라고도 불리며, 있는 이유는 이렇다.

DB가 예기치 못한 장애로 ㅂㅂ하면, DB 관리자도 함께 손 흔들며 떠나보내줄 수 없다. 
떠나보내준다면, 회사도 DB 관리자를 떠나보내줄 것이기 때문이다.

따라서 DB 장애가 생겨서 위의 상황이 일어나지 않게, DB에는 장애 회복(장애를 복구)하는 방법이 존재한다. 
그 중에서 **로그기반 회복기법**으로 한번쯤 들어봤을 즉시 갱신기법, 지연 갱신기법이 사용되는 것이였다.

암튼 이때 복구과정에서 undo로 되돌리고, redo로 재실행할 수 있는데, 
이 redo 로그를 잘 추출해 분석한다면, DB의 변화도 따른 곳에서 재실행할 수 있지 않을까? 
맞다!

## CDC 활용방안

1. DB 마이그레이션 : 
   DB 마이그레이션이란, 이주라는 단어 뜻의 마이그레이션처럼, DB를 합치거나, 현재 DB를 딴 DB로 옮기는 것이다.

   기존의 사용하던 DB에 대한 이동과 변환에 CDC를 사용하면, 비용절감, 다운타입(=시스템을 이용할 수 없는 시간) 최소화 등등에 쓰기 좋으며, 실제로도 많이 쓰인다.

2. DR(Disater Recovery=재해복구), 백업용 시스템 :
   비상 상황을 위한 백업용 시스템에서 CDC를 활용할 경우, 네트워크 비용이 해소되며, 서비스 재개가 빠르고, 시스템 대기 자원을 원래 그대로 사용하여 비용을 할 수 있는 장점 덕분에 많이 쓰인다.

## CDC 확장 (다른 기종 DB간에서도)

CDC의 솔루션(=CDC를 구현 소프트웨어)은 다양하게 존재하는데,
이중에는 Oracle 간의 데이터 캡쳐만 지원하는 솔루션도 있지만,
다른 기종간의 (이기종간) DB 데이터 통합을 지원하는 솔루션도 있다.

그리고 흔히 사용해보았던 MySQL의 데이터 캡쳐를 사용하는 방법도 있다.

MySQL에서 트렌젝션 로그는 활용하려면, 

```
[mysqld]

server-id  = 1
log_bin  = /var/log/mysql/mysql-bin.log
expire_logs_days = 10
max_binlog_size  = 100M
binlog-format    = row 
```

적용후, 서버를 ```-log-bin```옵션으로 시작해야 된다하는데,
그 이후에, 트렌젝션 로그를 추출하는 것을 쉽게 이해하도록, 트렌젝션 로그를 출력할 수 있다.

- maxwell 툴 이용 :

  ```
  ./bin/maxwell --user=’mysql_maxwell_user’' --password=’maxwell_passwordl' --host='127.0.0.1' --producer=stdout
  ```

  [maxwell 깃허브 링크](https://github.com/zendesk/maxwell)위 명령어를 터미널에 작성해서 
  ```json
  // insert into students (age,nam) values (15,’alex’);		// 실행한 sql 쿼리
  
  {"database":"school","table":"students","type":"insert","ts":1472937475,"xid":211209,
  "commit":true,"data":{"age":15,”name”:”alex”}}
  ```
  와 같이 트렌젝션 로그를 출력해보거나
  
- 파이썬의 python-mysql-replication 이용 :
  ```python
  from pymysqlreplication import BinLogStreamReader

  mysql_settings = {'host': '127.0.0.1', 'port': 3306, 'user': mysql_user, 'passwd': 'mysql_password'}

  log_stream = BinLogStreamReader(connection_settings = mysql_settings, server_id=100)

  for binlogevent in log_stream:
    binlogevent.dump()
  
log_stream.close()
  ```
  으로도 트렌젝션 로그 스트림을 출력해볼 수 있다.
  

## Reference

- https://www.kdata.or.kr/info/info_04_view.html?field=&keyword=&type=techreport&page=3&dbnum=189554&mode=detail&type=techreport : 한국데이터산업진흥원 - CDC
- [데이터 캡처 기술이란?](https://medium.com/wedatalab/cdc-데이터-캡처-기술이란-24bb87e8f566) : 기본 개념
- https://specialscene.tistory.com/34 : CDC 구현기법 & 구현방식
- https://hevodata.com/learn/mysql-cdc/#binlog : MySQL CDC 구현방법?

<details>
    <summary>삽질</summary>

    - https://dohoons.com/blog/1722/ : realworld 란
    - https://github.com/gothinkster/realworld : realworld 깃허브 repo

</details>    


  ```

  ```