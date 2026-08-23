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

import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from typing_extensions import TypedDict

from .config import Config
from .paste import Paste


def create_app(config: Config) -> FastAPI:
    logging.basicConfig()
    if config.misc.logging and config.misc.testing:
        logging.getLogger().setLevel(logging.DEBUG)

    logger = logging.getLogger()
    app = FastAPI(debug=config.misc.testing)
    if config.misc.testing:
        app.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            allow_origins=["*"],
        )

    paste = Paste(
        config.storage.path,
        config.storage.compression.enabled,
        config.storage.compression.level,
        config.storage.filters,
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
            key = paste.create(data.decode("utf-8", errors="replace"))
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
