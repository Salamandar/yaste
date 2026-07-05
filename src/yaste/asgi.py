#!/usr/bin/env python3

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
