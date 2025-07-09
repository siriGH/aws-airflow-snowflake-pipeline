Real-Time Data Pipeline: AWS S3 → Lambda → Airflow → Snowflake

This project showcases a real-time data ingestion pipeline that I built from scratch to explore how cloud-native services can work together to move and transform data seamlessly. From generating data to seeing it land in Snowflake. Everything here is automated, monitored, and orchestrated using some of the most widely used tools in the data world.

Use Case: 
This pipeline simulates real-time user activity data (such as user ID, name, and email), which is uploaded to an S3 bucket, triggers Lambda, calls a webhook to Apache Airflow, and finally loads the data into Snowflake.

It demonstrates how to:
Automate ingestion of semi-structured data (JSON).
Use event-driven Lambda for orchestration.
Run Airflow workflows using webhooks.
Use Snowflake's COPY INTO for data loading.

🧱 Tools & Technologies:

Python → Generate synthetic JSON data         
AWS S3 → Store data files                      
AWS Lambda → Trigger Airflow on file upload        
AWS CloudWatch → Monitor Lambda logs and events     
Apache Airflow (Docker) → Orchestrate ETL workflow   
Snowflake → Target data warehouse                 
Ngrok → Expose local Airflow to Lambda        
Git & GitHub → Version control & portfolio sharing 

📁 Project Structure:

aws-airflow-snowflake-pipeline/
├── dags/                      
│   └── s3_to_snowflake_dag.py
├── lambda/                   
│   └── lambda_function.py
├── python_generator/        
│   └── generate_data.py
├── airflow-docker/          
│   ├── docker-compose.yaml
│   └── requirements.txt
├── screenshots/              
│   ├── EveryStep_ScreeShorts.png
├── README.md


Step-by-Step Workflow:

Step 1: Generate Synthetic JSON Data using Python
A Python script (generate_data.py) creates simple user records like

These files are uploaded to a pre-configured AWS S3 bucket.

Step 2:  AWS S3 Triggers Lambda on File Upload
S3 is configured with an event notification.
When a .json file is uploaded, it triggers a Lambda function.
Lambda sends a POST request to Airflow's webhook endpoint (using Ngrok).

Step 3: Monitor Execution Using AWS CloudWatch
All Lambda invocations are logged automatically in CloudWatch.
This helped me validate loads and debug errors.

Step 4: Airflow Orchestrating the Data Load into Snowflake
I used Apache Airflow as the central orchestration tool for triggering and managing the Snowflake data load.

Airflow Setup with Docker
I used Docker Compose to spin up an Airflow environment on my local machine. This included the web server, scheduler, and metadata database.
Here's a quick look at the components defined in airflow-docker/docker-compose.yaml:
Airflow Webserver (UI at localhost:8080)
Scheduler to run DAGs
Volume mapping for local DAGs
Installed Snowflake provider using requirements.txt
I used Apache Airflow (running via Docker) to define the DAG (s3_to_snowflake_dag.py).
The DAG uses SnowflakeOperator to load the JSON into Snowflake.
Since I wanted to trigger this DAG automatically when new data lands in S3, I used AWS Lambda to send a webhook request to Airflow’s REST API via Ngrok: ngrok http 8080.
This allowed full automation: new file → Lambda → Airflow → Snowflake.


Step 5:  Snowflake: Data is Loaded & Verified
Before loading data, I prepared the Snowflake environment with the following components:
Storage Integration: I created a secure STORAGE INTEGRATION object (S3_INT) in Snowflake to allow access to the external S3 bucket.
Stage: An external stage named S3_JSON_STAGE was created, pointing to the S3 bucket with proper IAM role mapping.
Schema & Table: Inside my database (DATA_PIPELINE_DB), I created a USERS schema and a USER_DATA table to receive the incoming records.
Once the Airflow DAG ran successfully, I validated the data using:
SELECT * FROM DATA_PIPELINE_DB.USERS.USER_DATA;


About Me:
I’m Sirisha Karusala. I enjoy working in data engineering and cloud-based solutions on projects that bring together automation, scalability, and real-time data processing. This pipeline was a hands-on opportunity to apply my knowledge of AWS services, orchestration with Apache Airflow, and data warehousing in Snowflake. 
Please feel free to connect or reach out to me on LinkedIn at https://www.linkedin.com/in/sirishakarusal




# aws-airflow-snowflake-pipeline
End-to-end real-time data pipeline using AWS S3, Lambda, CloudWatch, Airflow(Docker), and Snowflake
