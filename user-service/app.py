from flask import Flask, request, jsonify
import psycopg2
import os
import jsonschema
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import bcrypt
import boto3
from botocore.exceptions import ClientError
import json

app = Flask(__name__)

# PostgreSQL Database Configuration
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", "5432")

# Establishing a connection to the database
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cur = conn.cursor()

user_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string", "format": "email"},
    },
    "required": ["username", "password", "email"],
}

# AWS Kinesis Configuration
kinesis_client = boto3.client("kinesis", region_name=os.getenv("AWS_REGION"))
kinesis_stream_name = os.getenv("KINESIS_STREAM_NAME")


def send_user_event_to_kinesis(event_type, user_data):
    try:
        payload = {"event_type": event_type, "user_data": user_data}
        kinesis_client.put_record(
            StreamName=kinesis_stream_name,
            Data=json.dumps(payload),
            PartitionKey=user_data["username"],
        )
    except ClientError as e:
        print(f"Error sending event to Kinesis: {e}")


@app.route("/users", methods=["POST"])
def register_user():
    user_info = request.json
    try:
        validate(instance=user_info, schema=user_schema)

        # Hash the password
        hashed_password = bcrypt.hashpw(
            user_info["password"].encode("utf-8"), bcrypt.gensalt()
        )
        user_info["password"] = hashed_password.decode("utf-8")

        cur.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            (user_info["username"], user_info["password"], user_info["email"]),
        )
        conn.commit()
        send_user_event_to_kinesis('user_registered', user_info)
        return jsonify({"message": "User registered successfully"}), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        cur.execute("SELECT * FROM users WHERE username = %s", (user_id,))
        user = cur.fetchone()
        if user:
            return jsonify({"username": user[0], "email": user[2]})
        else:
            return jsonify({"message": "User not found"}), 404
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500


@app.route("/user/<user_id>", methods=["PUT"])
def update_user(user_id):
    user_info = request.json
    try:
        cur.execute(
            "UPDATE users SET email = %s WHERE username = %s",
            (user_info["email"], user_id),
        )
        conn.commit()
        send_user_event_to_kinesis('user_updated', {'username': user_id, **user_info})
        return jsonify({"message": "User updated successfully"}), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500


def initialize_db():
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL
        );
    """
    )
    conn.commit()


if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)
