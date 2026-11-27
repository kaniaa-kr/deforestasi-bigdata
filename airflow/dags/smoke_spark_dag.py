from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    "smoke_spark",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["smoke"],
) as dag:
    s3 = BashOperator(task_id="smoke_s3",
                      bash_command="python /opt/airflow/src/spark_jobs/smoke_test_s3.py")
    jdbc = BashOperator(task_id="smoke_jdbc",
                        bash_command="python /opt/airflow/src/spark_jobs/smoke_test_jdbc.py")
    s3 >> jdbc
