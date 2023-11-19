# Order Service for E-Commerce Wine Store

This service manages orders for the wine store, including creating orders and retrieving order details. It uses AWS DynamoDB for storage and AWS SQS for order processing.

## Getting Started

These instructions will get the service up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- Docker (for containerized deployment)
- AWS CLI configured (for DynamoDB and SQS access)

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

- POST /orders: Create a new order
- GET /orders/{orderId}: Get details of a specific order
