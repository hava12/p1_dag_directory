import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG(
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@hourly"
)

# bash operator를 이용하여 데이터 가져오기
# get_data=BashOperator(
#     task_id="get_data",
#     bash_command=(
#         "curl -o /tmp/wikipageview.gz "
#         "https://dumps.wikimedia.org/other/pageviews/"
#         "{{ execution_date.year }}/"
#         "{{ execution_date.year }}-"
#         "{{ '{:02}'.format(execution_date.month) }}-"
#         "pageviews-{{ execution_date.year }}"
#         "{{ '{:02}'.format(execution_date.month) }}"  
#         "{{ '{:02}'.format(execution_date.day) }}-"  
#         "{{ '{:02}'.format(execution_date.hour) }}0000.gz"           
#     ),
#     dag=dag
# )

# Python Operator를 이용하여 데이터 가져오기
def _fetch_pageviews(pagenames) :
    result = dict.fromkeys(pagenames, 0)
    with open(F"/tmp/wikipageviews", "r") as f:
        for line in f:
            domain_code, page_title, view_counts, _=line.split(" ")
            if domain_code == "en" and page_title in pagenames:
                result[page_title]=view_counts
    print(result)
    # Prints e.g. "{'Facebook': '778', 'Apple':'20', 'Google': '451', 'Amazon': '9', 'Microsoft':'119'}"

fetch_pageviews = PythonOperator(
    task_id="fetch_pageviews",
    python_callable=lambda: _fetch_pageviews,
    op_kwargs = {
        "pagenames": {
            "Google",
            "Amazon",
            "Apple",
            "Microsoft",
            "Facebook"
        }
    },
    # op_args: Optional[List] = None,
    # templates_dict: Optional[Dict] = None
    # templates_exts: Optional[List] = None
    dag = dag
)