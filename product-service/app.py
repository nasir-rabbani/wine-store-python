from flask import Flask, request, jsonify
import boto3
import os
import uuid
from werkzeug.utils import secure_filename
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import json

app = Flask(__name__)

# Load environment variables
aws_region = os.getenv("AWS_REGION")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")
kinesis_stream_name = os.getenv("KINESIS_STREAM_NAME")

# Initialize DynamoDB and S3 clients
dynamodb = boto3.resource("dynamodb", region_name=aws_region)
s3 = boto3.client("s3", region_name=aws_region)
table = dynamodb.Table("Products")
kinesis_client = boto3.client("kinesis", region_name=aws_region)


def send_product_event_to_kinesis(event_type, product_data):
    try:
        payload = {"event_type": event_type, "product_data": product_data}
        kinesis_client.put_record(
            StreamName=kinesis_stream_name,
            Data=json.dumps(payload),
            PartitionKey=product_data["productId"],
        )
    except ClientError as e:
        print(f"Error sending event to Kinesis: {e}")


def upload_file_to_s3(file, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = file.filename

    try:
        s3.upload_fileobj(file, bucket, object_name)
        return True
    except ClientError as e:
        print(e)
        return False


@app.route("/product", methods=["POST"])
def add_product():
    # Check if a valid image file was uploaded
    if "image" not in request.files:
        return jsonify({"error": "No image part"}), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    image_key = str(uuid.uuid4()) + "-" + filename
    success = upload_file_to_s3(file, s3_bucket_name, image_key)

    if not success:
        return jsonify({"error": "Failed to upload image"}), 500

    image_url = f"https://{s3_bucket_name}.s3.{aws_region}.amazonaws.com/{image_key}"

    data = request.form
    product_id = data["productId"]
    name = data["name"]
    price = data["price"]
    description = data["description"]

    product_info = {
        "productId": product_id,
        "name": name,
        "price": price,
        "description": description,
        "image_url": image_url,
    }

    try:
        response = table.put_item(Item=product_info)
        send_product_event_to_kinesis("product_added", product_info)
        return jsonify(response), 201
    except ClientError as e:
        return jsonify(error=str(e)), 500


@app.route("/products", methods=["GET"])
def list_products():
    try:
        response = table.scan()
        return jsonify(response.get("Items", []))
    except ClientError as e:
        return jsonify(error=str(e)), 500


@app.route("/product/<product_id>", methods=["GET"])
def get_product(product_id):
    try:
        response = table.query(KeyConditionExpression=Key("productId").eq(product_id))
        items = response.get("Items", [])
        return jsonify(items[0]) if items else ("", 404)
    except ClientError as e:
        return jsonify(error=str(e)), 500


# ... [Rest of the code]
