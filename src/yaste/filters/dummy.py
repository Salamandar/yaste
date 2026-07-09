#!/usr/bin/env python3

from . import FilterType


class Filter(FilterType):
    def fill(self, file: str) -> None:
        self.data = file

    def acceptable(self) -> bool:
        return True

    def filtered(self) -> str:
        return self.data
