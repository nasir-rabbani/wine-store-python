# Notification Service

This service is responsible for sending email notifications via AWS SES.

## Getting Started

These instructions will get the service up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- AWS CLI configured with access to SES

### Building the Service

Build the Docker image:

```bash
make build
```

### Running the Service
Run the service using Docker:

```bash
make run
```

## API Endpoint

- POST /send-notification/: Sends an email notification to the specified address.

## Testing
Run the unit tests:

```bash
python test_main.py
```
