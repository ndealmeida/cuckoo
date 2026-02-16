import logging

from injector import inject, singleton
from vespa.package import ApplicationPackage, Document, Field, Schema

from src.data import SAMPLE_DOCUMENTS
from src.embedding_exporter.exporter import EmbeddingExporter
from src.services import ElasticsearchService, VespaService

logger = logging.getLogger(__name__)


@singleton
class Indexer:
    @inject
    def __init__(
        self,
        es_service: ElasticsearchService,
        vespa_service: VespaService,
        embedding_exporter: EmbeddingExporter,
    ):
        self.es_service = es_service
        self.vespa_service = vespa_service
        self.embedding_exporter = embedding_exporter

    def index_elasticsearch(self):
        logger.info("Indexing data to Elasticsearch...")
        es = self.es_service.get_client()
        index_name = "test_index"

        try:
            if es.indices.exists(index=index_name):
                es.indices.delete(index=index_name)

            # Simple schema for now
            es.indices.create(index=index_name)

            for doc in SAMPLE_DOCUMENTS:
                doc_id = str(doc["id"])
                # Here we could add transformations (like embeddings)
                es.index(index=index_name, id=doc_id, document=doc)
                logger.info(f"ES: Indexed doc {doc_id}")

            es.indices.refresh(index=index_name)
        except Exception as e:
            logger.error(f"Elasticsearch indexing failed: {e}")

    def index_vespa(self):
        logger.info("Indexing data to Vespa...")

        # Define schema
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
                app.feed_data_point(schema="doc", data_id=data_id, fields=doc)
                logger.info(f"Vespa: Indexed doc {data_id}")
        except Exception as e:
            logger.error(f"Vespa indexing failed: {e}")

    def run_all(self):
        self.index_elasticsearch()
        self.index_vespa()
