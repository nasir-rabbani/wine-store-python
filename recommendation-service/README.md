# Recommendation Service

This service provides product recommendations by querying a Redshift database.

## Getting Started

These instructions will get the service up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Access to an AWS Redshift database

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

### Testing
Run the unit tests:

```bash
python test_main.py
```

## API Endpoints

- GET /recommendations/{user_id}: Fetch product recommendations for a specific user.
