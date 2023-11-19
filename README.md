# Wine Store

## Architecture

```mermaid
graph TD
    UI["User Interface<br>(Web Application)"]
    APIG[API Gateway]

    UI --> APIG

    subgraph Microservices
    PS["Product Service<br>(DynamoDB)"]
    US["User Service<br>(RDS/Aurora)"]
    OS["Order Service<br>(DynamoDB)"]
    RS["Recommendation Service<br>(Redshift)"]
    NS["Notification Service<br>(SES)"]
    RSC["Recommendation Stream Consumer"]
    end

    subgraph Data_Storage
    S3["S3<br>Wine Images"]
    RDS["RDS/Aurora<br>User Data"]
    DDB["DynamoDB<br>Order Data"]
    Redshift["Redshift<br>Analytics Data"]
    end

    subgraph Messaging_and_Streaming
    SQS[SQS<br>Message Queue]
    Kinesis[Kinesis<br>Data Stream]
    end

    subgraph Security
    KMS["KMS<br>Encryption Keys"]
    end

    APIG -->|Data/API Requests| PS
    APIG -->|Data/API Requests| US
    APIG -->|Data/API Requests| OS
    APIG -->|Data/API Requests| RS
    APIG -->|Data/API Requests| NS

    PS -->|Image Storage| S3
    US -->|User Data Storage| RDS
    OS -->|Order Data Storage| DDB
    RS -->|Analytics Data Storage| Redshift

    US -->|Event Streaming| Kinesis
    PS -->|Event Streaming| Kinesis
    OS -->|Event Streaming| Kinesis
    Kinesis -->|Data Feed| RSC
    RSC -->|Process and Update| RS

    OS -->|Order Queue| SQS
    SQS -->|Order Processing| OS

    PS -->|Key Management| KMS
    US -->|Key Management| KMS
    OS -->|Key Management| KMS
    RS -->|Key Management| KMS
    NS -->|Key Management| KMS
    RSC -->|Key Management| KMS

    subgraph AWS
    UI
    APIG
    Microservices
    Data_Storage
    Messaging_and_Streaming
    Security
    end
```

1. User Interface (UI) Layer

- *Frontend*: A web-based UI where users can browse and purchase wines. This can be hosted on AWS Amplify or S3 with CloudFront for content delivery.

2. Application Layer (Microservices)

- *Product Service*: Manages wine inventory. Uses DynamoDB for storing product details.
- *User Service*: Manages user accounts and profiles. Uses RDS/Aurora for relational data storage.
- *Order Service*: Handles order creation and management. Uses DynamoDB for order data and places orders into an SQS queue.
- *Process Order Service*: Processes orders from the SQS queue. It updates order statuses and handles business logic related to order fulfillment.
- *Recommendation Service*: Provides personalized wine recommendations. Uses machine learning models, potentially leveraging SageMaker, and stores data in Redshift for analysis.
- - *Recommendation Stream Consumer*: Consumes data from the Kinesis data stream and updates the recommendation service with new data.
- *Notification Service*: Sends email notifications (order confirmations, promotions) using SES.

1. Data Storage Layer

- *S3:* Stores static assets like images of wine bottles, digital assets, etc.
- *RDS/Aurora*: Used for relational data that requires complex queries, like user data.
- *DynamoDB*: For high-speed, flexible NoSQL storage, like product catalog and orders.
- *Redshift*: For data warehousing and analytics.

4. Integration and Messaging

- *SQS*: For decoupling microservices, handling message queues for asynchronous processing (e.g., order processing, inventory updates).
- *Kinesis*: For real-time data streaming and analytics, useful for user activity tracking, real-time inventory updates, etc.

5. Security and Encryption

- *KMS*: For managing encryption keys used in the application, ensuring data security across services.

6. Additional Considerations

- *API Gateway*: To manage and route requests to the appropriate microservices.
- *Lambda*: For serverless computing needs, such as running small functions triggered by events (e.g., image processing upon upload to S3).
- *CloudWatch*: For monitoring and logging.
Elasticsearch Service: For advanced search capabilities across the product catalog.
