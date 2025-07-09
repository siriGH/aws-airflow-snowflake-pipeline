import json
import urllib3

# Replace with your ngrok public Airflow URL
AIRFLOW_API_URL = "https://3b95e438c3de.ngrok-free.app/api/v1/dags/s3_to_snowflake_dag/dagRuns"
AIRFLOW_USERNAME = "admin"
AIRFLOW_PASSWORD = "admin"

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    # Extract S3 file info (optional, for logging)
    s3_info = event['Records'][0]['s3']
    bucket = s3_info['bucket']['name']
    key = s3_info['object']['key']
    print(f"File uploaded: s3://{bucket}/{key}")

    # Prepare payload to trigger DAG
    payload = {
        "conf": {
            "s3_bucket": bucket,
            "s3_key": key
        }
    }

    http = urllib3.PoolManager()
    headers = urllib3.make_headers(basic_auth=f"{AIRFLOW_USERNAME}:{AIRFLOW_PASSWORD}")
    headers["Content-Type"] = "application/json"

    response = http.request(
        "POST",
        AIRFLOW_API_URL,
        body=json.dumps(payload),
        headers=headers
    )

    print("Airflow response status:", response.status)
    print("Airflow response body:", response.data.decode())
    return {
        'statusCode': response.status,
        'body': response.data.decode()
    }
