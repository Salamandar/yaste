#!/usr/bin/env python3

import hashlib
from pathlib import Path

import zstandard

from .filters import get_filters


def key_of_data(data: str) -> str:
    m = hashlib.blake2b(digest_size=16)
    m.update(data.encode("utf-8"))
    return m.hexdigest()


class Paste:
    def __init__(self, path: Path, compress: bool, compress_level: int, filters: list[str]) -> None:
        self._path = path
        self._compress = compress
        self._compress_level = compress_level
        self.filters = get_filters(filters)

    def search(self, key: str) -> Path | None:
        if (path := self._path / f"{key}.zst").exists():
            return path
        if (path := self._path / f"{key}.txt").exists():
            return path
        return None

    def exists(self, key: str) -> bool:
        return self.search(key) is not None

    def read(self, path: Path) -> str:
        if path.name.endswith(".zst"):
            data = zstandard.decompress(path.read_bytes()).decode("utf-8")
        else:
            data = path.read_text()
        return data

    def apply_filters(self, data: str) -> str:
        for name, filtertype in self.filters.items():
            filterimpl = filtertype()
            filterimpl.fill(data)
            if not filterimpl.acceptable():
                raise RuntimeError(f"Filter {name} decided data is inacceptable")
            data = filterimpl.filtered()
        return data

    def create(self, data: str) -> str:
        data = self.apply_filters(data)

        key = key_of_data(data)
        if self.exists(key):
            raise FileExistsError(f"File with hash {key} already exists")

        if self._compress:
            file = self._path / f"{key}.zst"
            file.write_bytes(zstandard.compress(data.encode("utf-8"), level=self._compress_level))
        else:
            file = self._path / f"{key}.txt"
            file.write_text(data)

        return key
