import json
import logging
import os

from injector import inject, singleton
from vespa.package import ApplicationPackage, Schema

from src.config import Config
from src.data import SAMPLE_DOCUMENTS
from src.embedding_exporter.exporter import EmbeddingExporter
from src.services import ElasticsearchService, VespaService

logger = logging.getLogger(__name__)


@singleton
class Indexer:
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

    def index_elasticsearch(self):
        index_name = self.config.elasticsearch.index_name
        logger.info(f"Indexing data to Elasticsearch index '{index_name}' (with vectors)...")
        es = self.es_service.get_client()

        try:
            if es.indices.exists(index=index_name):
                es.indices.delete(index=index_name)

            mapping_file = os.path.join(
                self.config.elasticsearch.mappings_path, self.config.elasticsearch.mapping_file
            )
            with open(mapping_file, "r") as f:
                mapping = json.load(f)

            es.indices.create(index=index_name, mappings=mapping)

            for doc in SAMPLE_DOCUMENTS:
                doc_id = str(doc["id"])
                es.index(index=index_name, id=doc_id, document=doc)
                logger.info(f"ES: Indexed doc {doc_id} with vector")

            es.indices.refresh(index=index_name)
        except Exception as e:
            logger.error(f"Elasticsearch indexing failed: {e}")

    def index_vespa(self):
        logger.info("Indexing data to Vespa (with vectors)...")

        schema_file = os.path.join(self.config.vespa.schema_path, self.config.vespa.schema_file)
        try:
            vespa_schema = Schema.from_sd_file(schema_file)
            app_package = ApplicationPackage(name=self.config.app_name, schema=[vespa_schema])

            app = self.vespa_service.deploy_sample_app(app_package)

            for doc in SAMPLE_DOCUMENTS:
                data_id = str(doc["id"])
                app.feed_data_point(schema=vespa_schema.name, data_id=data_id, fields=doc)
                logger.info(f"Vespa: Indexed doc {data_id} with vector")
        except Exception as e:
            logger.error(f"Vespa indexing failed: {e}")

    def run_all(self):
        self.run_embeddings_generation()
        self.index_elasticsearch()
        self.index_vespa()

    def run_embeddings_generation(self):
        logger.info("Generating embeddings for documents...")
        for doc in SAMPLE_DOCUMENTS:
            if "embedding" not in doc:
                doc["embedding"] = self.embedding_exporter.encode(doc["body"])
