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
    password: str


@singleton
@dataclass
class Config:
    database: DatabaseConfig

    def __init__(self):
        self.database = DatabaseConfig(**settings.database)
