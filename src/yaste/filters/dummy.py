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
