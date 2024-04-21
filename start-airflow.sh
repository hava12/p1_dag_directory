#!/bin/bash
source ~/.bashrc

# airflow db init
airflow webserver -p 8080
airflow scheduler