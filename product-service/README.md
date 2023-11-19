# Product Service for E-Commerce Wine Store

This service is a part of a microservices-based e-commerce application for a wine store.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- Docker
- AWS CLI configured with access to DynamoDB and S3

### Installing

Clone the repository and install the dependencies:

```bash
git clone [repo-url]
cd [repo-directory]
pip install -r requirements.txt
```

### Running the app

```bash
FLASK_APP=app.py FLASK_ENV=development flask run
```

### Running with Docker

To build and run the app using Docker:

```bash
docker build -t wine-store-product-service .
docker run -p 5000:5000 wine-store-product-service
```

### Running the tests

To run the tests, execute:

```bash
python test_app.py
```

## API Endpoints

- GET /products - List all products
- GET /product/<product_id> - Get a specific product
- POST /product - Add a new product (with image)

