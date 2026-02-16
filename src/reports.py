import logging

from injector import inject, singleton

from src.config import Config
from src.embedding_exporter.exporter import EmbeddingExporter
from src.services import ElasticsearchService, VespaService

logger = logging.getLogger(__name__)


@singleton
class SearchReporter:
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

    def report_elasticsearch(self, query_text: str):
        logger.info(f"ES Keyword Report: '{query_text}'")
        es = self.es_service.get_client()
        query = {"match": {"body": query_text}}
        try:
            res = es.search(index=self.config.elasticsearch.index_name, query=query)
            for hit in res["hits"]["hits"]:
                logger.info(f" - [Score: {hit['_score']:.4f}] {hit['_source']['title']}")
        except Exception as e:
            logger.error(f"ES Search failed: {e}")

    def report_elasticsearch_semantic(self, query_text: str):
        logger.info(f"ES Semantic Report: '{query_text}'")
        es = self.es_service.get_client()
        query_vector = self.embedding_exporter.encode(query_text)
        knn = {
            "field": "embedding",
            "query_vector": query_vector,
            "k": 3,
            "num_candidates": 10,
        }
        try:
            res = es.search(index=self.config.elasticsearch.index_name, knn=knn)
            for hit in res["hits"]["hits"]:
                logger.info(f" - [Score: {hit['_score']:.4f}] {hit['_source']['title']}")
        except Exception as e:
            logger.error(f"ES Semantic Search failed: {e}")

    def report_vespa(self, query_text: str):
        logger.info(f"Vespa Keyword Report: '{query_text}'")
        app = self.vespa_service.get_app()
        query_body = {"yql": f'select * from sources * where body contains "{query_text}";'}
        try:
            res = app.query(body=query_body)
            for hit in res.hits:
                logger.info(f" - [Score: {hit['relevance']:.4f}] {hit['fields']['title']}")
        except Exception as e:
            logger.error(f"Vespa Search failed: {e}")

    def report_vespa_semantic(self, query_text: str):
        logger.info(f"Vespa Semantic Report: '{query_text}'")
        app = self.vespa_service.get_app()
        query_vector = self.embedding_exporter.encode(query_text)
        query_body = {
            "yql": """
                select * from sources * where {targetHits:3}nearestNeighbor(embedding, q_vector);
            """,
            "input.query(q_vector)": query_vector,
        }
        try:
            res = app.query(body=query_body)
            for hit in res.hits:
                logger.info(f" - [Score: {hit['relevance']:.4f}] {hit['fields']['title']}")
        except Exception as e:
            logger.error(f"Vespa Semantic Search failed: {e}")

    def run_comparison(self, query_text: str):
        logger.info("=== SEARCH COMPARISON REPORT ===")
        logger.info(f"Query: '{query_text}'")
        logger.info("-" * 30)
        self.report_elasticsearch(query_text)
        self.report_elasticsearch_semantic(query_text)
        logger.info("-" * 30)
        self.report_vespa(query_text)
        self.report_vespa_semantic(query_text)
        logger.info("-" * 30)
