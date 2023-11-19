# Process Orders Service

This service is responsible for processing orders for the e-commerce wine store. It continuously polls an AWS SQS queue for new orders and processes them.

## Getting Started

These instructions will get the service up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- AWS CLI configured with access to DynamoDB and SQS

### Building the Service

Build the Docker image:

```bash
make build
```

### Running the service

Run the service using Docker:

```bash
make run
```

### Testing

Running unit tests:

```bash
python test_process_orders.py
```
