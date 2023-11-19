import boto3
import json
import os
from botocore.exceptions import ClientError

# Initialize AWS clients for DynamoDB and SQS
dynamodb = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION"))
sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION"))
order_table = dynamodb.Table("Orders")
order_queue_url = os.getenv("ORDER_QUEUE_URL")


def process_order_message(message):
    order_data = json.loads(message["Body"])
    order_id = order_data["orderId"]

    try:
        # Update the order status in DynamoDB as processed
        response = order_table.update_item(
            Key={"orderId": order_id},
            UpdateExpression="SET orderStatus = :status",
            ExpressionAttributeValues={":status": "Processed"},
            ReturnValues="UPDATED_NEW",
        )
        print(f"Order {order_id} processed successfully.")
    except ClientError as e:
        print(f"Error processing order {order_id}: {e}")


def poll_sqs_queue():
    while True:
        # Polling messages from SQS
        response = sqs.receive_message(
            QueueUrl=order_queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20,  # Long polling
        )

        messages = response.get("Messages", [])
        for message in messages:
            process_order_message(message)
            # Delete message from the queue after processing
            sqs.delete_message(
                QueueUrl=order_queue_url, ReceiptHandle=message["ReceiptHandle"]
            )


if __name__ == "__main__":
    poll_sqs_queue()
