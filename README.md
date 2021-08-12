## GB-Backend-docker
밥브리타임 RESTful API Back-end Server 구현하기 😉

#### Back-end : Django + MySQL + Docker
- [x] MySQL DB와의 연동 (Board, Article, and Comments)
- [x] 일부 버그 Fix (실행 안되던 문제)
  - MySQL 8.x 버전대라서, Password 을 암호 관련 인증하는 방식을 변경함
  - 오탈자 👉 비밀번호가 잘못 적혀있는 부분을 수정
  - `django-cors-headers` 패키지가 설치되지 않았던 부분 수정
- [ ] RESTful API Endpoint 설계 (미완)
- [ ] Front-end와의 동기화 (미완)
- [ ] 나머지 Rule 및 Filter Setting (미완)
- [ ] ELK Stack과 Log 연동 (미완)

### 사용 방법
```sh
$ git clone https://github.com/VYWL/GB-Backend-docker
$ # .env 파일을 최상단, 그리고 Django 내부에 설정.
$ sudo docker-compose up --build
```


### 기타사항
- 문제 있을시 연락.
