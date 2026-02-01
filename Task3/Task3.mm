graph LR
    Client -->|HTTP Request| ShopAPI
    ShopAPI -->|W3C Context| MES_API
    MES_API -->|W3C Context| DB[(Postgres)]
    
    subgraph "Observability Plane"
    ShopAPI -.->|OTLP gRPC| JaegerCollector
    MES_API -.->|OTLP gRPC| JaegerCollector
    JaegerCollector --> JaegerUI
    end
