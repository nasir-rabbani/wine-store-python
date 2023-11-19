from flask import Flask, request, jsonify
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json
import os

app = Flask(__name__)

# Initialize DynamoDB, SQS, and kinesis clients
dynamodb = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION"))
sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION"))
order_table = dynamodb.Table("Orders")
order_queue_url = os.getenv("ORDER_QUEUE_URL")
kinesis_client = boto3.client("kinesis", region_name=os.getenv("AWS_REGION"))
kinesis_stream_name = os.getenv("KINESIS_STREAM_NAME")

order_schema = {
    "type": "object",
    "properties": {
        "orderId": {"type": "string"},
        "items": {"type": "array", "items": {"type": "string"}},
        "total": {"type": "number"},
    },
    "required": ["orderId", "items", "total"],
}


def send_order_event_to_kinesis(order_data):
    try:
        payload = {"event_type": "order_created", "order_data": order_data}
        kinesis_client.put_record(
            StreamName=kinesis_stream_name,
            Data=json.dumps(payload),
            PartitionKey=order_data["orderId"],
        )
    except ClientError as e:
        print(f"Error sending order event to Kinesis: {e}")


@app.route("/orders", methods=["POST"])
def create_order():
    order_data = request.json
    try:
        validate(order_data, order_schema)
        order_table.put_item(Item=order_data)
        # Send message to SQS Queue
        sqs.send_message(QueueUrl=order_queue_url, MessageBody=json.dumps(order_data))
        # Send event to Kinesis Stream
        send_order_event_to_kinesis(order_data)
        return jsonify({"message": "Order created successfully"}), 201
    except ClientError as e:
        return jsonify({"error": str(e)}), 500
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    try:
        response = order_table.get_item(Key={"orderId": order_id})
        if "Item" in response:
            return jsonify(response["Item"])
        else:
            return jsonify({"message": "Order not found"}), 404
    except ClientError as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
