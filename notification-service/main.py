from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import boto3
from botocore.exceptions import ClientError
import os

app = FastAPI()


class NotificationRequest(BaseModel):
    email: EmailStr
    subject: str
    message: str


# Initialize SES client
ses_client = boto3.client("ses", region_name=os.getenv("AWS_REGION"))


@app.post("/send-notification/")
async def send_notification(notification: NotificationRequest):
    try:
        response = ses_client.send_email(
            Source=os.getenv("EMAIL_FROM"),
            Destination={"ToAddresses": [notification.email]},
            Message={
                "Subject": {"Data": notification.subject},
                "Body": {"Text": {"Data": notification.message}},
            },
        )
        return {"message": "Notification sent", "response": response}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
