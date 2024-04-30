from airflow import DAG

import airflow.utils.dates
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.configuration import conf

from azure.storage.filedatalake import DataLakeServiceClient
import requests

yesterday = datetime.now() - timedelta(days=1)
yesterday_date_str = yesterday.strftime('%Y%m%d')

def get_real_estate_data_func():
    
    print(conf.get('estate-api', 'api-url'))
    print(conf.get('estate-api', 'api-key'))

    # REST API를 호출하여 데이터를 가져오는 함수
    url = conf.get('estate-api', 'api-url')
    params = {
        'ServiceKey': conf.get('estate-api', 'api-key'),
    }

    response = requests.get(url, params=params)  # requests 라이브러리를 사용해 API 호출

    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)
    
    return response.text  # 데이터 반환

def save_real_estate_data_func(data, **kwargs):
    # Azure Data Lake Storage Gen2에 데이터를 저장하는 함수
    print(data)
    try:
        # Azure 계정 설정 정보
        storage_account_name = conf.get('storage', 'storage-account-name')
        storage_account_key = conf.get('storage', 'storage-account-key')
        file_system_name = conf.get('estate-api', 'container-name')

        # 저장할 파일 경로 설정
        file_path = 'data_{date}.xml'.format(date=yesterday_date_str)

        # Data Lake 서비스 클라이언트 초기화
        service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net", credential=storage_account_key)
        file_system_client = service_client.get_file_system_client(file_system=file_system_name)
        file_client = file_system_client.get_file_client(file_path)
        file_client.upload_data(data, overwrite=True, length=len(data))

        print("Data saved successfully to Azure Data Lake.")
    except Exception as e:
        print(f"An error occurred: {e}")

with DAG(
    dag_id='real_estate_transaction',
    # default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=airflow.utils.dates.days_ago(2),
    tags=['example'],
) as dag:
    
    get_real_estate_data = PythonOperator(
        task_id="get_real_estate_data",
        python_callable=get_real_estate_data_func,
        # op_kwargs: Optional[Dict] = None,
        # op_args: Optional[List] = None,
        # templates_dict: Optional[Dict] = None
        # templates_exts: Optional[List] = None
    )

    save_real_estate_data = PythonOperator(
        task_id="save_real_estate_data",
        python_callable=save_real_estate_data_func,
        op_kwargs={'data': '{{ ti.xcom_pull(task_ids="get_real_estate_data") }}'},  # 이전 태스크에서 데이터 받기
        # op_args: Optional[List] = None,
        # templates_dict: Optional[Dict] = None
        # templates_exts: Optional[List] = None
    )

    get_real_estate_data >> save_real_estate_data
