# User Service for E-Commerce Wine Store

This service manages user-related operations for the wine store.

## Getting Started

These instructions will get the service up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- Docker (for containerized deployment)
- AWS CLI configured (for DynamoDB access)

### Installation

Install the necessary Python packages:

```bash
make install
```

### Running the Service
Run the service locally:

```bash
make run
```

### Running with Docker
Build and run the service using Docker:

```bash
make docker-run
```

### Testing
Run the unit tests:

```bash
make test
```

## API Endpoints

- POST /users: Register a new user
- GET /user/{userId}: Get details of a specific user
- PUT /user/{userId}: Update details of a specific user

