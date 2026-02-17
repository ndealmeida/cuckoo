# Cuckoo 🐦‍⬛

Cuckoo is my playground for exploring the intersection of **Search Engineering** and **AI Engineering**.

## 🚀 Roadmap
- [x] Basic Search Infrastructure (Docker, Healthchecks)
- [x] Dependency Injection & Service Architecture
- [x] Keyword Search Comparison (Elasticsearch vs. Vespa)
- [x] Semantic Search (Vector Search)
- [ ] Hybrid Search (BM25 + Dense Vectors)
- [ ] Custom Ranking with ML Models

## 🛠 Tech Stack
- **Language:** Python 3.14+
- **Orchestration:** Docker Compose
- **Engines:** Elasticsearch 8.18, Vespa 8.64, Postgres 18
- **Management:** `uv` for lightning-fast dependency management
- **Frameworks:** `injector` (DI), `pyvespa`, `elasticsearch-py`, `sentence-transformers` (SBERT)

## 🏃 Getting Started

1. Initialize search infrastructure (requirement: 4GB+ of memory)

```bash
docker compose up -d
```

2. Deploy Vespa mappings (see more [here](docs/04_Vespa_Schemas_vs_ES_Mappings.md))

```bash
uv run deploy-vespa
```

3. Run Cuckoo:

```bash
uv run cuckoo
```

## API

1. Trigger `POST /index` to run indexation (currently it reads from mock data in data.py)
2. Search with `GET /search` endpoint
