from airflow import DAG

import airflow.utils.dates
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.configuration import conf

yesterday = datetime.now() - timedelta(days=1)
yesterday_date_str = yesterday.strftime('%Y%m%d')

def get_weather_data():
    
    print(conf.get('estate-api', 'api-url'))
    print(conf.get('estate-api', 'api-key'))

    # REST API를 호출하여 데이터를 가져오는 함수
    url = conf.get('estate-api', 'api-url')
    params = {
    'key': conf.get('estate-api', 'api-key'),
    'targetDt': yesterday_date_str
    }

    response = requests.get(url, params=params)  # requests 라이브러리를 사용해 API 호출

    print("Status Code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)
    data = response.json()  # 응답을 JSON으로 변환
    
    return data  # 데이터 반환


with DAG(
    'real_estate_transation',
    # default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=airflow.utils.dates.days_ago(2),
    tags=['example'],
) as dag:
    
    get_weather_data = PythonOperator(
        task_id="get_weather_data",
        python_callable=get_weather_data,
        # op_kwargs: Optional[Dict] = None,
        # op_args: Optional[List] = None,
        # templates_dict: Optional[Dict] = None
        # templates_exts: Optional[List] = None
    )

    save_weather_data = PythonOperator(
        task_id="save_weather_data",
        python_callable=lambda: print('Hi from python operator'),
        # op_kwargs: Optional[Dict] = None,
        # op_args: Optional[List] = None,
        # templates_dict: Optional[Dict] = None
        # templates_exts: Optional[List] = None
    )

    get_weather_data >> save_weather_data
