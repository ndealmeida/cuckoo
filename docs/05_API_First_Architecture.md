# 05 - API-First Architecture

We transitioned from a script-based execution model to a service-oriented architecture using **FastAPI**.

## 🚀 Why an API?
1.  **Production Readiness:** In a real-world scenario, your search engine isn't triggered by a local script; it's part of a backend ecosystem.
2.  **Decoupling:** The "Search Logic" is now separated from the "Interface." You can call the same logic from a CLI, a web frontend, or another microservice.
3.  **State Management:** By running as a server, we can maintain persistent connections to Elasticsearch and Vespa, improving performance.

## 🛠 Endpoints

### 1. `POST /index`
- **Action:** Clears existing indices and re-indexes all sample documents.
- **Transformations:** Generates embeddings for all documents before pushing to the engines.
- **Nature:** Synchronous (waits for both engines to finish).

### 2. `POST /search`
- **Action:** Routes queries to the specified engine and search type.
- **Parameters:**
    - `query`: The text string.
    - `source`: `elasticsearch` or `vespa`.
    - `type`: `LEXICAL` (BM25 keyword) or `SEMANTIC` (Vector similarity).
