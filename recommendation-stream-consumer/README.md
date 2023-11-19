# Recommendation Stream Consumer

This service is responsible for consuming data from an AWS Kinesis stream and processing it for recommendation purposes.

## Getting Started

These instructions will get the service up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- AWS CLI configured with access to Kinesis

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

## Testing
Run the unit tests:

```bash
python test_main.py
```
