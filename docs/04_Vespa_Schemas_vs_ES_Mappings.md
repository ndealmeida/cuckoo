# 04 - Configuration Management: API vs. Deployment

This document outlines the fundamental difference in how Elasticsearch and Vespa manage their data structures and search logic.

## 1. Elasticsearch: API-Driven
Elasticsearch utilizes a dynamic, RESTful approach to configuration.
- **Mechanism:** Mappings are updated via HTTP requests (e.g., `PUT /index/_mapping`).
- **Lifecycle:** Configuration changes are applied directly to the active index.
- **Data Model:** Supports dynamic mapping, where the engine infers types from incoming JSON documents if a field is not predefined.

## 2. Vespa: Deployment-Driven
Vespa utilizes a "Schema-as-Code" approach where configurations are bundled into an Application Package.
- **Mechanism:** Schemas (`.sd` files) are part of an application package that must be uploaded to a Config Server.
- **Lifecycle:** The Config Server validates the package and distributes it across the cluster. This ensures that every node in the system is synchronized with the same version of the schema and ranking logic.
- **Data Model:** Requires explicit schema definitions. All fields and tensor dimensions must be declared before data can be indexed.

## 3. Core Distinction
- **Elasticsearch** is optimized for **flexibility**: Changes can be made to individual indices via the API without affecting the broader system state.
- **Vespa** is optimized for **consistency**: The deployment model ensures that complex ranking expressions and schemas are validated and atomically updated across the entire distributed system.
