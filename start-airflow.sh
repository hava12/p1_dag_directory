export AIRFLOW_HOME=~/airflow_workspace/

airflow db init
airflow webserver -p 8080
airflow scheduler