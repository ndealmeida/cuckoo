import logging
from injector import Injector, inject
from vespa.package import ApplicationPackage, Document, Field, Schema
from src.services import ElasticsearchService, VespaService
from src.data import SAMPLE_DOCUMENTS

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class SearchComparison:
    @inject
    def __init__(self, es_service: ElasticsearchService, vespa_service: VespaService):
        self.es_service = es_service
        self.vespa_service = vespa_service

    def run_elasticsearch_test(self):
        logger.info("--- Testing Elasticsearch ---")
        if not self.es_service.test_connection():
            logger.error("Elasticsearch is not responding!")
            return

        es = self.es_service.get_client()
        index_name = "test_index"
        
        try:
            if es.indices.exists(index=index_name):
                es.indices.delete(index=index_name)
            es.indices.create(index=index_name)

            for doc in SAMPLE_DOCUMENTS:
                doc_id = str(doc["id"])
                res = es.index(index=index_name, id=doc_id, document=doc)
                logger.info(f"Indexed doc {doc_id}: {res['result']}")

            es.indices.refresh(index=index_name)

            query = {"match": {"body": "engineering"}}
            res = es.search(index=index_name, query=query)
            logger.info(f"Search results found: {res['hits']['total']['value']}")
            for hit in res["hits"]["hits"]:
                logger.info(f" - {hit['_source']['title']}")
        except Exception as e:
            logger.error(f"Elasticsearch operation failed: {e}")

    def run_vespa_test(self):
        logger.info("--- Testing Vespa ---")
        
        app_package = ApplicationPackage(
            name="testapp",
            schema=[
                Schema(
                    name="doc",
                    document=Document(
                        fields=[
                            Field(name="id", type="int", indexing=["summary"]),
                            Field(name="title", type="string", indexing=["index", "summary"]),
                            Field(name="body", type="string", indexing=["index", "summary"]),
                        ]
                    ),
                )
            ],
        )

        try:
            app = self.vespa_service.deploy_sample_app(app_package)
            
            for doc in SAMPLE_DOCUMENTS:
                data_id = str(doc["id"])
                res = app.feed_data_point(schema="doc", data_id=data_id, fields=doc)
                logger.info(f"Indexed doc {data_id} status: {res.status_code}")

            query_body = {"yql": 'select * from sources * where body contains "engineering";'}
            res = app.query(body=query_body)
            logger.info(f"Search results found: {len(res.hits)}")
            for hit in res.hits:
                logger.info(f" - {hit['fields']['title']}")
        except Exception as e:
            logger.error(f"Vespa operation failed: {e}")

def main():
    container = Injector()
    comparison = container.get(SearchComparison)
    comparison.run_elasticsearch_test()
    comparison.run_vespa_test()

if __name__ == "__main__":
    main()
