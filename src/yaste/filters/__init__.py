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
        the_filter = all_filters.get(name, all_filters.get(f"yaste.filters.{name}"))
        if the_filter is None:
            raise RuntimeError(f"Could not find yaste filter {name}")

        filters[name] = the_filter
    return filters
