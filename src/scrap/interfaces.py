#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc

from src.items.interfaces import DofusData


class ItemCasting(abc.ABC):
    @abc.abstractmethod
    def to_item(self) -> DofusData:
        pass

