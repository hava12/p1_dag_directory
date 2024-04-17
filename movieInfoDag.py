from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
from azure.storage.filedatalake import DataLakeServiceClient

def fetch_data():
    # REST API URL
    url = "https://api.example.com/data"
    response = requests.get(url)
    data = response.json()
    return data

def save_to_data_lake(data, **kwargs):
    try:
        storage_account_name = 'your_storage_account_name'
        storage_account_key = 'your_storage_account_key'
        file_system_name = 'your_file_system_name'
        file_path = 'data_{date}.json'.format(date=datetime.now().strftime('%Y%m%d'))

        service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net", credential=storage_account_key)
        file_system_client = service_client.get_file_system_client(file_system=file_system_name)
        file_client = file_system_client.get_file_client(file_path)

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
    schedule_interval='0 0 * * *',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    t1 = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data,
        provide_context=True
    )

    t2 = PythonOperator(
        task_id='save_to_data_lake',
        python_callable=save_to_data_lake,
        op_kwargs={'data': '{{ ti.xcom_pull(task_ids="fetch_data") }}'},
    )

    t1 >> t2
