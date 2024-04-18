from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
from azure.storage.filedatalake import DataLakeServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_data():
    # REST API를 호출하여 데이터를 가져오는 함수
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
    params = {
    'key1': 'value1',
    'key2': 'value2'
    }
    response = requests.get(url)  # requests 라이브러리를 사용해 API 호출
    data = response.json()  # 응답을 JSON으로 변환
    return data  # 데이터 반환

def save_to_data_lake(data, **kwargs):
    # Azure Data Lake Storage Gen2에 데이터를 저장하는 함수
    try:
        # Azure 계정 설정 정보
        storage_account_name = os.getenv('storage-account-name')
        storage_account_key = os.getenv('storage-account-key')
        file_system_name = os.getenv('storage-account-container-name')
        # 저장할 파일 경로 설정
        file_path = 'data_{date}.json'.format(date=datetime.now().strftime('%Y%m%d'))

        # Data Lake 서비스 클라이언트 초기화
        service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net", credential=storage_account_key)
        file_system_client = service_client.get_file_system_client(file_system=file_system_name)
        file_client = file_system_client.get_file_client(file_path)

        # 파일 생성 및 데이터 추가
        file_client.create_file()
        file_client.append_data(data, 0, len(data))
        file_client.flush_data(len(data))
        
        print("Data saved successfully to Azure Data Lake.")
    except Exception as e:
        print(f"An error occurred: {e}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'api_to_azure_datalake',
    default_args=default_args,
    description='Fetch data from API and store in Azure Data Lake',
    schedule_interval='0 0 * * *',  # 매일 자정에 실행
    start_date=datetime(2023, 1, 1),  # DAG 시작 날짜
    catchup=False,  # 과거 누락된 실행을 캐치업하지 않음
    tags=['example'],  # DAG 분류를 위한 태그
) as dag:

    t1 = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data,  # 데이터 페칭 함수 연결
        provide_context=True
    )

    t2 = PythonOperator(
        task_id='save_to_data_lake',
        python_callable=save_to_data_lake,  # 데이터 저장 함수 연결
        op_kwargs={'data': '{{ ti.xcom_pull(task_ids="fetch_data") }}'},  # 이전 태스크에서 데이터 받기
    )

    # t1 >> t2  # t1 태스크 후 t2 태스크 실행
    t1