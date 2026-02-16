# Cuckoo 🐦‍⬛

Cuckoo is my playground for exploring the intersection of **Search Engineering** and **AI Engineering**.

## 🚀 Roadmap
- [x] Basic Search Infrastructure (Docker, Healthchecks)
- [x] Dependency Injection & Service Architecture
- [x] Keyword Search Comparison (Elasticsearch vs. Vespa)
- [ ] **Semantic Search (Vector Search)** - *In Progress*
- [ ] Hybrid Search (BM25 + Dense Vectors)
- [ ] Custom Ranking with ML Models

## 🛠 Tech Stack
- **Language:** Python 3.14+
- **Orchestration:** Docker Compose
- **Engines:** Elasticsearch 8.18, Vespa 8.64, Postgres 18
- **Management:** `uv` for lightning-fast dependency management
- **Frameworks:** `injector` (DI), `pyvespa`, `elasticsearch-py`, `sentence-transformers` (SBERT)

## 🏃 Getting Started

Note: please provide at least 4Gb for containers to work properly.

1. **Spin up the engines:**
   ```bash
   docker compose up -d
   ```

2. **Run the comparison:**
   ```bash
   uv run cuckoo
   ```
