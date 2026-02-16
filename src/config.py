from dataclasses import dataclass

from dynaconf import Dynaconf
from injector import singleton

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.yaml", ".secrets.yaml"],
    merge_enabled=True,
)


@dataclass
class DatabaseConfig:
    host: str
    port: int
    user: str


@dataclass
class ElasticsearchConfig:
    host: str
    port: int


@dataclass
class VespaConfig:
    host: str
    port: int
    config_url: str


@dataclass
class EmbeddingConfig:
    model_name: str


@singleton
@dataclass
class Config:
    database: DatabaseConfig
    elasticsearch: ElasticsearchConfig
    vespa: VespaConfig
    embedding: EmbeddingConfig

    def __init__(self):
        self.database = DatabaseConfig(**settings.database)
        self.elasticsearch = ElasticsearchConfig(**settings.elasticsearch)
        self.vespa = VespaConfig(**settings.vespa)
        self.embedding = EmbeddingConfig(**settings.embedding)
