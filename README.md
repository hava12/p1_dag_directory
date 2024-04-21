# Project Overview
Apache Airflow Test Project

Project는 영화진흥위원회의 오픈 API를 이용해 진행합니다. (아래 링크 참고)
- https://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do

# Prerequisites
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

# 진행 상황
movieInfo_dag.py 파일 실행 테스트 진행 중 
- DataLake 에 용량이 110Byte밖에 전송되지 않는 점 확인 필요
