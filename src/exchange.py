# -*- encoding: utf-8 -*-
"""
@File    :  exchange.py
@Time    :  2024/08/18 08:33:40
@Author  :  Kevin Wang
@Desc    :  None
"""

from collections import defaultdict

from errors import (ExchangeAlreadyExists,
                    ExchangeDoNotExists,
                    )
from objects import Exchange


class ExchangeHandler:
    def __init__(self) -> None:
        self._table = defaultdict(dict)
    
    def register(self,
                 source:str,
                 target:str,
                 rate:float,
                 overwrite=False,
                 ):
        if (target in self._table[source]) and (not overwrite):
            raise ExchangeAlreadyExists
        self._table[source][target] = Exchange(source, target, rate)

    def do_exchange(self,
                    source:str,
                    target:str,
                    price:float,
                    ) -> float:
        if source == target:
            return price
        if target not in self._table[source]:
            raise ExchangeDoNotExists(f"Exchange rate: {source} -> {target} has not been registered yet.")
        return self._table[source][target] * price
