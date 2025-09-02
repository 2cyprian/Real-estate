Erd Diagram
erDiagram

    %% -------------------------------------
    %% User Service (SQL - PostgreSQL)
    %% - For transactional, relational user data
    %% -------------------------------------
    Users {
        UUID id PK "Primary Key"
        varchar email UK "Unique"
        varchar hashed_password
        varchar first_name
        varchar last_name
        boolean is_agent
        timestamp created_at
        timestamp updated_at
    }

    Agents {
        UUID id PK "Primary Key"
        UUID user_id FK "Foreign Key to Users.id"
        varchar agency_name
        varchar license_number UK "Unique"
        text bio
        varchar profile_image_url
    }

    SavedSearches {
        UUID id PK "Primary Key"
        UUID user_id FK "Foreign Key to Users.id"
        jsonb search_criteria "Flexible JSON for search params"
        timestamp created_at
    }

    Users ||--o{ SavedSearches : "saves"
    Users ||--|| Agents : "is an"


    %% -------------------------------------
    %% Property Service (SQL - PostgreSQL)
    %% - For structured, transactional property data
    %% -------------------------------------
    Properties {
        UUID id PK "Primary Key"
        UUID agent_id "Refers to Agents.id in User Service"
        varchar status "ENUM: For Sale, For Rent, Sold"
        varchar property_type "ENUM: House, Apartment, Land"
        varchar address
        varchar city
        varchar province
        decimal price "For precise monetary value"
        decimal bedrooms
        decimal bathrooms
        text description
        geography location "PostGIS for location queries"
        timestamp listed_at
        timestamp updated_at
    }

    PropertyImages {
        UUID id PK "Primary Key"
        UUID property_id FK "Foreign Key to Properties.id"
        varchar image_url
        int order_index "To sort images"
    }

    Amenities {
        UUID id PK "Primary Key"
        varchar name UK "Unique, e.g., 'Swimming Pool'"
        varchar icon_url
    }

    PropertyAmenities {
        UUID property_id FK "Foreign Key to Properties.id"
        UUID amenity_id FK "Foreign Key to Amenities.id"
    }

    Properties ||--o{ PropertyImages : "has"
    Properties }o--o{ Amenities : "features"


    %% ----------------------------------------------------
    %% Content & Analytics Service (NoSQL - MongoDB)
    %% - For flexible, document-based, high-volume data
    %% - Relationships are conceptual/application-level
    %% ----------------------------------------------------
    Articles_Collection {
        ObjectId _id PK "Primary Key"
        string title
        string slug UK "URL-friendly version of title"
        string content
        string category "'market_news', 'buying_advice'"
        UUID author_id "Refers to Users.id in User Service"
        array tags "e.g., ['investment', 'gauteng']"
        timestamp published_at
    }

    PropertyViews_Collection {
        ObjectId _id PK "Primary Key"
        UUID property_id "Refers to Properties.id"
        UUID user_id "Refers to Users.id (optional)"
        timestamp viewed_at
        string ip_address
        string user_agent
    }

    MarketTrends_Collection {
        ObjectId _id PK "Primary Key"
        string region "e.g., 'Gauteng'"
        int year
        int month
        object average_price "e.g., { all: 1.2M, house: 1.5M }"
        int sales_count
    }

   FlowChart
   flowchart LR
    %% -----------------------------
    %% SQL Services (Postgres)
    %% -----------------------------
    subgraph SQL["User & Property Services (Postgres)"]
        U[Users]
        AG[Agents]
        SS[SavedSearches]
        P[Properties]
        PI[PropertyImages]
        AM[Amenities]
        PA[PropertyAmenities]
    end

    %% -----------------------------
    %% NoSQL Services (MongoDB)
    %% -----------------------------
    subgraph NoSQL["Content & Analytics (MongoDB)"]
        A[Articles Collection]
        PV[PropertyViews Collection]
        MT[MarketTrends Collection]
    end

    %% -----------------------------
    %% SQL Relationships
    %% -----------------------------
    U -->|is an| AG
    U -->|saves| SS
    AG -->|lists| P
    P -->|has| PI
    P -->|features| PA
    PA --> AM

    %% -----------------------------
    %% SQL ↔ NoSQL Conceptual Links
    %% -----------------------------
    U -->|writes| A
    U -->|generates| PV
    P -->|viewed in| PV

Architecture

graph LR
    subgraph Browser["User's Browser"]
        U(User) --> R[React Web App]
    end

    subgraph Edge["The Edge (Cloudflare / AWS CloudFront)"]
        R -- HTTPS Requests --> CDN[CDN]
        CDN -- Cached Assets --> R
        CDN -- API Calls --> WAF[Web Application Firewall]
        WAF --> LB[Load Balancer / API Gateway]
    end

    subgraph Backend["Backend Infrastructure (Kubernetes in AWS/GCP/Azure)"]
        LB --> SS[Search Service]
        LB --> PS[Property Service]
        LB --> US[User Service]
        LB --> CS[Content Service]

        subgraph Data["Data & Search Layer"]
            SS -- Queries --> ES[Elasticsearch Cluster]
            PS -- Reads/Writes --> PG_P[PostgreSQL - Properties DB]
            US -- Reads/Writes --> PG_U[PostgreSQL - Users DB]
            CS -- Reads/Writes --> MDB[MongoDB - Content DB]
            PS -- Stores Images --> S3[Cloud Object Storage S3]
        end

        subgraph Async["Asynchronous Processing"]
            PS -- Publishes Events --> MQ[Message Queue - RabbitMQ/Kafka]
            US -- Publishes Events --> MQ
            
            W_Idx[Indexing Worker] -- Consumes --> MQ
            W_Img[Image Worker] -- Consumes --> MQ
            W_Notif[Notification Worker] -- Consumes --> MQ

            W_Idx -- Writes to --> ES
            W_Img -- Reads/Writes --> S3
            W_Notif -- Sends Emails/Alerts --> ExtSvc[External Services -SendGrid, Twilio]
        end
    end

    %% Styles
    style U fill:#f9f,stroke:#333,stroke-width:2px
    style R fill:#9cf,stroke:#333,stroke-width:2px
    style ES fill:#f96,stroke:#333,stroke-width:2px
    style SS fill:#9f9,stroke:#333,stroke-width:2px
