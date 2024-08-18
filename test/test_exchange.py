# -*- encoding: utf-8 -*-
"""
@File    :  test_exchange.py
@Time    :  2024/08/18 09:18:31
@Author  :  Kevin Wang
@Desc    :  None
"""

import math

import pytest

from errors import (ExchangeAlreadyExists,
                    ExchangeDoNotExists,
                    )
from exchange import ExchangeHandler
from objects import Exchange


class TestExchangeHandler:
    def test_register(self):
        exchange_handler = ExchangeHandler()
        exchange_handler.register("USD", "TWD", 31)
        assert "USD" in exchange_handler._table
        assert "TWD" in exchange_handler._table["USD"]
        assert Exchange('USD', 'TWD', 31) == exchange_handler._table["USD"]["TWD"]

    def test_register_conflict(self):
        exchange_handler = ExchangeHandler()
        exchange_handler.register("USD", "TWD", 31)
        with pytest.raises(ExchangeAlreadyExists):
            exchange_handler.register("USD", "TWD", 999)

    def test_register_overwrite(self):
        exchange_handler = ExchangeHandler()
        exchange_handler.register("USD", "TWD", 31)
        exchange_handler.register("USD", "TWD", 999, overwrite=True)
        assert Exchange('USD', 'TWD', 999) == exchange_handler._table["USD"]["TWD"]

    def test_do_exchange(self):
        exchange_handler = ExchangeHandler()
        exchange_handler.register("USD", "TWD", 31)
        assert math.isclose(exchange_handler.do_exchange("USD", "TWD", 10),
                            310,
                            )

    def test_do_exchange_on_unknown_rate(self):
        exchange_handler = ExchangeHandler()
        with pytest.raises(ExchangeDoNotExists):
            exchange_handler.do_exchange("USD", "TWD", 10)
