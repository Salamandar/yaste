#!/usr/bin/env python3

import logging
from typing import TypedDict

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse

from .config import Config
from .paste import Paste


def create_app(config: Config) -> FastAPI:
    logger = logging.getLogger()
    app = FastAPI(debug=config.misc.testing)
    paste = Paste(
        config.storage.path,
        config.storage.compression.enabled,
        config.storage.compression.level,
    )

    if config.frontend is not None:
        app.frontend("/", directory=config.frontend.path)

    class CreatePasteResponse(TypedDict):
        key: str
        url: str
        raw: str

    @app.post("/create", status_code=201)
    @app.post("/documents", status_code=201)  # Compatibility with hastebin
    async def paste_post(fastapi_req: Request) -> CreatePasteResponse:
        data = await fastapi_req.body()
        logger.debug("Getting new paste of size %s", len(data))
        try:
            key = paste.create(data)
        except FileExistsError:
            raise HTTPException(status_code=409, detail="Data already exists") from None

        return {
            "key": key,
            "url": f"{config.server.public_host}/{key}",
            "raw": f"{config.server.public_host}/raw/{key}",
        }

    @app.get("/raw/{key}")
    async def paste_get(key: str) -> PlainTextResponse:
        path = paste.search(key)
        if path is None:
            raise HTTPException(status_code=404, detail="Item does not exist") from None
        return PlainTextResponse(paste.read(path))

    return app
