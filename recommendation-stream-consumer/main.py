import boto3
import json
import os
from botocore.exceptions import ClientError

# Initialize Kinesis client
kinesis_client = boto3.client("kinesis", region_name=os.getenv("AWS_REGION"))
kinesis_stream_name = os.getenv("KINESIS_STREAM_NAME")


def process_stream_data(record):
    # Implement logic to process and use this data
    # This could involve updating recommendation data in Redshift
    print("Processing record:", record)


def poll_kinesis_stream():
    try:
        response = kinesis_client.describe_stream(StreamName=kinesis_stream_name)
        shard_id = response["StreamDescription"]["Shards"][0]["ShardId"]
        shard_iterator = kinesis_client.get_shard_iterator(
            StreamName=kinesis_stream_name, ShardId=shard_id, ShardIteratorType="LATEST"
        )["ShardIterator"]

        while True:
            out = kinesis_client.get_records(ShardIterator=shard_iterator, Limit=100)
            for record in out["Records"]:
                process_stream_data(json.loads(record["Data"]))
            shard_iterator = out["NextShardIterator"]
            # Sleep or timeout as needed
    except ClientError as e:
        print(f"Error polling Kinesis stream: {e}")


if __name__ == "__main__":
    poll_kinesis_stream()
