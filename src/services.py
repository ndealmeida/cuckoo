import logging
from typing import Optional

import docker
from elasticsearch import Elasticsearch
from injector import inject, singleton
from vespa.application import Vespa
from vespa.deployment import VespaDocker
from vespa.package import ApplicationPackage

from src.config import Config

logger = logging.getLogger(__name__)
# Silence the httpr library warning about CA bundles
logging.getLogger("httpr").setLevel(logging.ERROR)


@singleton
class ElasticsearchService:
    @inject
    def __init__(self, config: Config):
        self.host = config.elasticsearch.host
        self.port = config.elasticsearch.port
        self.client: Optional[Elasticsearch] = None

    def get_client(self) -> Elasticsearch:
        if self.client is None:
            self.client = Elasticsearch(f"http:{self.host}:{self.port}")
        return self.client

    def test_connection(self) -> bool:
        try:
            return self.get_client().ping()
        except Exception as e:
            logger.error(f"Elasticsearch ping failed: {e}")
            return False


@singleton
class VespaService:
    @inject
    def __init__(self, config: Config):
        self.host = config.vespa.host
        self.port = config.vespa.port
        self.config_url = config.vespa.config_url
        self.app: Optional[Vespa] = None

    def deploy_sample_app(self, app_package: ApplicationPackage) -> Vespa:
        client = docker.from_env()
        try:
            container = client.containers.get("vespa")
            vespa_docker = VespaDocker(container=container)
            self.app = vespa_docker.deploy(application_package=app_package)
            return self.app
        except Exception as e:
            logger.error(f"Vespa deployment failed: {e}")
            raise e

    def get_app(self) -> Vespa:
        if self.app is None:
            self.app = Vespa(url=f"http:{self.host}:{self.port}")
        return self.app
