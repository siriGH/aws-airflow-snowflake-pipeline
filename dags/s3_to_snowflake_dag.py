from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'depends_on_past': False,
}

with DAG(
    dag_id='s3_to_snowflake_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['snowflake', 'json', 's3'],
) as dag:

    load_data_into_snowflake = SnowflakeOperator(
        task_id='load_from_s3_to_snowflake',
        sql="""
            COPY INTO USER_DATA (ID, NAME, EMAIL)
            FROM (
                SELECT
                    $1:id::STRING AS ID,
                    $1:name::STRING AS NAME,
                    $1:email::STRING AS EMAIL
                FROM @S3_JSON_STAGE
            )
            FILE_FORMAT = (FORMAT_NAME = 'JSON_FORMAT')
            PATTERN = '.*'
            ON_ERROR = CONTINUE;
        """,
        snowflake_conn_id='snowflake_default',
        warehouse='COMPUTE_WH',
        database='DATA_PIPELINE_DB',
        schema='USERS',
        role='ACCOUNTADMIN',
        do_xcom_push=True,
    )
