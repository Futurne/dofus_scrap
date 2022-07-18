#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc


class DofusData(abc.ABC):
    @abc.abstractmethod
    def to_dict(self) -> dict:
        pass

class Bonus(DofusData):
    pass

class Condition(DofusData):
    pass

class Dommage(DofusData):
    pass

