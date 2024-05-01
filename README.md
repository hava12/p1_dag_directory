# Project Overview
Apache Airflow Test Project

해당 프로젝트를 통해 부동산 관련 네이버 뉴스의 부정 혹은 긍정 의견에 따른 아파트 매매 실거래 추이 변화를 분석하고자 합니다.

<!-- Project는 영화진흥위원회의 오픈 API를 이용해 진행합니다. (아래 링크 참고) -->
<!-- - https://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do -->

#### [API 정보] 

- 아파트매매 실거래 상세 자료
https://www.data.go.kr/data/15057511/openapi.do

- 네이버 뉴스 API
https://developers.naver.com/docs/serviceapi/search/news/news.md


# Prerequisites
- HDFS/Hive Server (Linux - Standalone) - 생성 전
- Spark Server (Linux - Standalone) - 생성 전
- Linux Ubuntu Server
    - Docker Community Edition
    - Docker compose v1.29.1 이상
- VSCode   

# Airflow 구성 요소
- Airflow Webserver
    - Airflow의 웹 인터페이스를 제공
- Airflow Scheduler
    - Airflow의 스케줄러 컨테이너. 작업의 실행 타이밍을 결정하고 새로운 작업 인스턴스를 트리거
- Airflow Worker
    - 작업을 실행하는 주체. 실제로 사용자가 정의한 태스크 실행
- Airflow Redis
    - 메시지 브로커 역할. 작업 메시지를 임시 저장하고 Worker간 작업 분배
- Airflow Flower
    - CeleryExecutor와 사용되는 경우 Celery클러스터를 모니터링하는 웹 기반 툴
- PostgreSQL or MySQL
    - Airflow의 메타데이터를 저장하는 데이터베이스

# 명령어 설명

- Backfill 기능 : my_dag_id는 DAG의 ID, -s는 시작 날짜, -e는 종료 날짜를 지정합니다.  
예시)  
```airflow dags backfill -s 2020-01-01 -e 2020-01-07 my_dag_id```

# 진행 상황
- 부동산 실거래 정보 API 호출 후 DataLake 적재 테스트 완료