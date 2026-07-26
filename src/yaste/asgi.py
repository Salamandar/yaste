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

import os
from pathlib import Path

import uvicorn

from .app import create_app
from .config import get_config

config_path = Path(os.getenv("YASTE_CONFIG", "config.yml"))
config = get_config(config_path)

app = create_app(config)


def main() -> None:
    uvicorn.run(
        "yaste.asgi:app",
        host=config.server.host,
        port=config.server.port,
        reload=config.misc.testing,
        access_log=config.misc.logging,
    )


if __name__ == "__main__":
    main()
