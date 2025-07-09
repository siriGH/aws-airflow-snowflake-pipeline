import json
import uuid
import boto3
from faker import Faker

fake = Faker()

def generate_user():
    return {
        "id": str(uuid.uuid4()),
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "created_at": fake.iso8601()
    }

# Generate file name
filename = f"user_data_{uuid.uuid4()}.json"
local_path = f"./{filename}"

# Step 1: Create NDJSON file locally
with open(local_path, "w") as f:
    for _ in range(10):  # adjust number of records as needed
        json.dump(generate_user(), f)
        f.write("\n")

print(f"✅ NDJSON file created: {local_path}")

# Step 2: Upload to S3
bucket_name = "data-pipeline-sk"  # ✅ Replace with your bucket
s3_key = filename

s3 = boto3.client("s3")

try:
    s3.upload_file(local_path, bucket_name, s3_key)
    print(f"✅ File uploaded to S3: s3://{bucket_name}/{s3_key}")
except Exception as e:
    print(f"❌ Failed to upload: {e}")
