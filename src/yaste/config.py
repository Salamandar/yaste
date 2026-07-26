#!/usr/bin/env python3
# Yaste
# Copyright (C) 2026  Yaste contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
    filters: list[str] = []


class Frontend(CustomModel):
    path: Path = Path(__file__).parent.parent.parent / "frontend" / "dist"


class Misc(CustomModel):
    testing: bool = False
    logging: bool = True


class Config(CustomModel):
    server: Server
    storage: Storage
    frontend: Frontend | None = None
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
