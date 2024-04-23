from airflow import DAG

import airflow.utils.dates
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

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
        python_callable=lambda: print('Hi from python operator'),
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