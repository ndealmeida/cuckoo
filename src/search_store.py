import logging
from enum import Enum
from typing import Any, Dict, List

from injector import inject, singleton

from src.config import Config
from src.embedding_exporter.exporter import EmbeddingExporter
from src.services import ElasticsearchService, VespaService

logger = logging.getLogger(__name__)


class SearchSource(str, Enum):
    ELASTICSEARCH = "ELASTICSEARCH"
    VESPA = "VESPA"


class SearchType(str, Enum):
    LEXICAL = "LEXICAL"
    SEMANTIC = "SEMANTIC"


@singleton
class SearchStore:
    @inject
    def __init__(
        self,
        config: Config,
        es_service: ElasticsearchService,
        vespa_service: VespaService,
        embedding_exporter: EmbeddingExporter,
    ):
        self.config = config
        self.es_service = es_service
        self.vespa_service = vespa_service
        self.embedding_exporter = embedding_exporter

    def search(
        self, query: str, source: SearchSource, search_type: SearchType
    ) -> List[Dict[str, Any]]:
        if source == SearchSource.ELASTICSEARCH:
            return self._search_elasticsearch(query, search_type)
        return self._search_vespa(query, search_type)

    def _search_elasticsearch(
        self, query_text: str, search_type: SearchType
    ) -> List[Dict[str, Any]]:
        es = self.es_service.get_client()
        index_name = self.config.elasticsearch.index_name

        if search_type == SearchType.LEXICAL:
            query = {"match": {"body": query_text}}
            res = es.search(index=index_name, query=query)
        else:
            query_vector = self.embedding_exporter.encode(query_text)
            knn = {"field": "embedding", "query_vector": query_vector, "k": 3, "num_candidates": 10}
            res = es.search(index=index_name, knn=knn)

        return [
            {"score": hit["_score"], "title": hit["_source"]["title"]}
            for hit in res["hits"]["hits"]
        ]

    def _search_vespa(self, query_text: str, search_type: SearchType) -> List[Dict[str, Any]]:
        app = self.vespa_service.get_app()
        if search_type == SearchType.LEXICAL:
            query_body = {
                "yql": "select * from sources * where userQuery();",
                "query": query_text,
                "type": "any",  # Behave like Elasticsearch (OR)
                "ranking": "default",  # Use Vespa's built-in BM25
            }
        else:
            query_vector = self.embedding_exporter.encode(query_text)
            query_body = {
                "yql": """
                    select *
                    from sources * 
                    where {targetHits:3}nearestNeighbor(embedding, q_vector);
                """,
                "input.query(q_vector)": query_vector,
                "ranking": "semantic",  # Use our custom closeness rank profile
            }
        res = app.query(body=query_body)
        return [{"score": hit["relevance"], "title": hit["fields"]["title"]} for hit in res.hits]
