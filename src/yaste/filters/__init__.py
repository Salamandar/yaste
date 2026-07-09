#!/usr/bin/env python3

import importlib
import pkgutil
import sys
from abc import ABC, abstractmethod
from collections.abc import Iterator
from types import ModuleType

CURRENT_MODULE = sys.modules[__name__]


class FilterType(ABC):
    @abstractmethod
    def fill(self, file: str) -> None:
        pass

    @abstractmethod
    def acceptable(self) -> bool:
        pass

    @abstractmethod
    def filtered(self) -> str:
        pass


def discover_filters() -> dict[str, type[FilterType]]:
    def iter_namespace(ns_pkg: ModuleType) -> Iterator[pkgutil.ModuleInfo]:
        # Specifying the second argument (prefix) to iter_modules makes the
        # returned name an absolute name instead of a relative one. This allows
        # import_module to work without having to do additional modification to
        # the name.
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

    plugins: dict[str, type[FilterType]] = {}
    for _, name, _ in iter_namespace(CURRENT_MODULE):
        module = importlib.import_module(name)
        if "Filter" not in module.__dict__ or not issubclass(module.Filter, FilterType):
            raise RuntimeError(f"invalid yaste filter {name}")
        plugins[name] = module.Filter

    return plugins


def get_filters(filter_names: list[str]) -> dict[str, type[FilterType]]:
    all_filters = discover_filters()
    filters = {}
    for name in filter_names:
        if not (the_filter := all_filters.get(name)):
            raise RuntimeError(f"Could not find yaste filter {name}")

        filters[name] = the_filter
    return filters
