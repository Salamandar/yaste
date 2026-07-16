#!/usr/bin/env python3

from typing import override

from . import FilterType


class Filter(FilterType):
    @override
    def fill(self, file: str) -> None:
        self.data = file

    @override
    def acceptable(self) -> bool:
        return True

    @override
    def filtered(self) -> str:
        return self.data
