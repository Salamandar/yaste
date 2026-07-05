#!/usr/bin/env python3

import tomllib
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, ValidationError, model_validator


class CustomModel(BaseModel):
    model_config = ConfigDict(
        validate_default=True,
        extra="forbid",
    )


class Server(CustomModel):
    host: str = "127.0.0.1"
    port: int = 8004

    public_host: str | None = None

    @model_validator(mode="after")
    def set_public_host(self) -> "Server":
        if self.public_host is None:
            scheme = "http" if self.port != 443 else "https"
            portstr = f":{self.port}" if self.port not in [80, 443] else ""
            self.public_host = f"{scheme}://{self.host}{portstr}"
        return self


class StorageCompression(CustomModel):
    enabled: bool = False
    level: int = 4


class Storage(CustomModel):
    path: Path
    compression: StorageCompression


class Misc(CustomModel):
    testing: bool = False
    logging: bool = True


class Config(CustomModel):
    server: Server
    storage: Storage
    misc: Misc


def get_config(path: Path) -> Config:
    try:
        if path.name.endswith((".yaml", ".yml")):
            data = yaml.safe_load(path.open("r"))
        elif path.name.endswith(".toml"):
            data = tomllib.load(path.open("rb"))
        else:
            raise RuntimeError(f"Could not determine format of config {path}")
        config = Config(**data)
    except FileNotFoundError:
        raise RuntimeError(f"Config file {path} not found!") from None
    except yaml.YAMLError as err:
        msg = f"Config file {path} has invalid YAML syntax:\n{err}"
        raise RuntimeError(msg) from None
    except tomllib.TOMLDecodeError as err:
        msg = f"Config file {path} has invalid TOML syntax:\n{err}"
        raise RuntimeError(msg) from None
    except ValidationError as err:
        raise RuntimeError(f"Invalid config file {path}:\n{err}") from None
    else:
        return config
