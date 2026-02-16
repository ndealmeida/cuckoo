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
    index_name: str
    mappings_path: str
    mapping_file: str


@dataclass
class VespaConfig:
    host: str
    port: int
    config_port: int
    schema_path: str
    schema_file: str


@dataclass
class EmbeddingConfig:
    model_name: str
    cache_folder: str


@singleton
@dataclass
class Config:
    app_name: str
    database: DatabaseConfig
    elasticsearch: ElasticsearchConfig
    vespa: VespaConfig
    embedding: EmbeddingConfig

    def __init__(self):
        self.app_name = settings.app_name
        self.database = DatabaseConfig(**settings.database)
        self.elasticsearch = ElasticsearchConfig(**settings.elasticsearch)
        self.vespa = VespaConfig(**settings.vespa)
        self.embedding = EmbeddingConfig(**settings.embedding)
