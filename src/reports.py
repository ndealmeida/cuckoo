import logging

from injector import inject, singleton

from src.services import ElasticsearchService, VespaService

logger = logging.getLogger(__name__)


@singleton
class SearchReporter:
    @inject
    def __init__(self, es_service: ElasticsearchService, vespa_service: VespaService):
        self.es_service = es_service
        self.vespa_service = vespa_service

    def report_elasticsearch(self, query_text: str):
        logger.info(f"ES Report for query: '{query_text}'")
        es = self.es_service.get_client()
        query = {"match": {"body": query_text}}
        try:
            res = es.search(index="test_index", query=query)
            for hit in res["hits"]["hits"]:
                logger.info(f" - [Score: {hit['_score']:.4f}] {hit['_source']['title']}")
        except Exception as e:
            logger.error(f"ES Search failed: {e}")

    def report_vespa(self, query_text: str):
        logger.info(f"Vespa Report for query: '{query_text}'")
        app = self.vespa_service.get_app()
        query_body = {"yql": f'select * from sources * where body contains "{query_text}";'}
        try:
            res = app.query(body=query_body)
            for hit in res.hits:
                logger.info(f" - [Score: {hit['relevance']:.4f}] {hit['fields']['title']}")
        except Exception as e:
            logger.error(f"Vespa Search failed: {e}")

    def run_comparison(self, query_text: str):
        logger.info("=== SEARCH COMPARISON REPORT ===")
        self.report_elasticsearch(query_text)
        self.report_vespa(query_text)
