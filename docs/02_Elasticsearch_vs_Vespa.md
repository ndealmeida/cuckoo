# 02 - Elasticsearch vs. Vespa: Conceptual Comparison

While both can search text and vectors, they are built with very different philosophies.

## 1. Elasticsearch: The Analytics Powerhouse
Elasticsearch is built on **Apache Lucene**.
- **Mental Model:** A JSON Document Store. You send data, it "indexes" it, and you search it.
- **Strengths:** "Time to first search" is minutes. Incredible for logs (ELK stack) and general-purpose search.
- **Schema:** Flexible. It can guess your schema (Dynamic Mapping), which makes it great for rapid prototyping.

## 2. Vespa: The Serving Engine
Vespa was built by Yahoo for high-volume, complex ranking (like News feeds and Ad targeting).
- **Mental Model:** A distributed computation engine that happens to store data.
- **Strengths:** Designed for **Real-time AI**. You can run complex math (Tensors) inside the engine itself.
- **Schema:** Strict. You must define a `.sd` (Schema Definition) file. It feels more like a database than a search index.

## 3. Key Concept Mapping

| Concept | Elasticsearch | Vespa |
| :--- | :--- | :--- |
| **Data Unit** | Document | Document |
| **Collection** | Index | Schema / Content Cluster |
| **Ranking** | Script Score / Rank Feature | Rank Profile (First-phase / Second-phase) |
| **Vector Field** | `dense_vector` | `tensor<float>(x[dim])` |
| **Query Language**| Query DSL (JSON) | YQL (SQL-like) |
| **Scaling** | Shards & Replicas | Content Nodes & Groups |
