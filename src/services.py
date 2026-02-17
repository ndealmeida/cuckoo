import logging
from typing import Optional

import docker
from elasticsearch import Elasticsearch
from injector import inject, singleton
from vespa.application import Vespa
from vespa.deployment import VespaDocker

from src.config import Config

logger = logging.getLogger(__name__)
logging.getLogger("httpr").setLevel(logging.ERROR)


@singleton
class ElasticsearchService:
    @inject
    def __init__(self, config: Config):
        self.config = config.elasticsearch
        self.client: Optional[Elasticsearch] = None

    def get_client(self) -> Elasticsearch:
        if self.client is None:
            self.client = Elasticsearch(f"http://{self.config.host}:{self.config.port}")
        return self.client

    def test_connection(self) -> bool:
        try:
            return self.get_client().ping()
        except Exception:
            return False


@singleton
class VespaService:
    @inject
    def __init__(self, config: Config):
        self.config = config.vespa
        self.app_name = config.app_name
        self.app: Optional[Vespa] = None

    def get_app(self) -> Vespa:
        if self.app is None:
            self.app = Vespa(url=f"http://{self.config.host}", port=self.config.port)
        return self.app

    def test_connection(self) -> bool:
        try:
            import httpx

            response = httpx.get(f"http://{self.config.host}:{self.config.port}", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def deploy_from_disk(self) -> Vespa:
        client = docker.from_env()
        container = client.containers.get("vespa")
        vespa_docker = VespaDocker(
            container=container, port=self.config.port, cfgsrv_port=self.config.config_port
        )
        self.app = vespa_docker.deploy_from_disk(
            application_name=self.app_name, application_root=self.config.schema_path
        )
        return self.app
