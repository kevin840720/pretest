# -*- encoding: utf-8 -*-
"""
@File    :  service.py
@Time    :  2024/08/16 21:00:39
@Author  :  Kevin Wang
@Desc    :  None
"""

from abc import ABC, abstractmethod
from collections import namedtuple
from typing import (List,
                    Tuple,
                    )
import json
import re

from exchange import ExchangeHandler
from objects import (Address,
                     Order,
                     )

from requests import Response

ValidateResult = namedtuple('ValidateResult', ['status', 'msg'])

class Validator(ABC):
    @abstractmethod
    def validate(self, obj:str) -> ValidateResult:
        raise NotImplementedError

class DummyValidator(Validator):
    def validate(self, obj:str) -> ValidateResult:
        return ValidateResult(200, "")

class NameValidator(Validator):
    def validate(self, name:str) -> ValidateResult:
        if name == "":
            return ValidateResult(400, "Empty name")
        if not re.fullmatch(r"[a-zA-Z\s]+", name):
            return ValidateResult(400, "Name contains non-English characters")
        if not name.istitle():
            return ValidateResult(400, "Name is not capitalized")
        return ValidateResult(200, "")

class PriceValidator(Validator):
    def __init__(self, price_ub:int) -> None:
        super().__init__()
        self._price_ub = price_ub

    def validate(self, price:str) -> ValidateResult:
        if price == "":
            return ValidateResult(400, "Empty price")
        if not price.isdigit():
            return ValidateResult(400, "Price contains non-digits characters")
        if int(price) > self._price_ub:
            return ValidateResult(400, f"Price is over {self._price_ub}")
        return ValidateResult(200, "")

class CurrencyValidator(Validator):
    def __init__(self, currencies:List[str]) -> None:
        super().__init__()
        self.currencies = currencies
    
    def validate(self, currency:str) -> ValidateResult:
        if currency not in self.currencies:
            return ValidateResult(400, "Currency format is wrong")
        return ValidateResult(200, "")


class Transform(ABC):
    @abstractmethod
    def transform(self, obj:str) -> object:
        raise NotImplementedError

class ExchangeTransform(Transform):
    def __init__(self,
                 exchange_handler:ExchangeHandler,
                 ) -> None:
        super().__init__()
        self._exchange_handler = exchange_handler
    
    def transform(self,
                  source:str,
                  target:str,
                  price:int,
                  ) -> int:
        return self._exchange_handler.do_exchange(source,
                                                  target,
                                                  int(price),
                                                  )

class Service:
    def __init__(self,
                 name_validator:Validator,
                 price_validator:Validator,
                 currency_validator:Validator,
                 exchange_transform:ExchangeTransform,
                 ) -> None:
        self._name_validator = name_validator
        self._price_validator = price_validator
        self._currency_validator = currency_validator
        self._exchange_transform = exchange_transform

    def validate(self, obj:dict) -> ValidateResult:
        """Validate input order data field by field.

        Args:
            obj (dict): order data

        Returns:
            ValidateResult: validated result. `status=200` stand for success.
        """
        results = [self._name_validator.validate(obj["name"]),
                   self._price_validator.validate(obj["price"]),
                   self._currency_validator.validate(obj["currency"]),
                   ]
        for result in results:
            if result.status == 400:
                return result
        return result

    def transform(self, obj:dict) -> Order:
        """Transform input order data into self-defined `Order` object.

        Args:
            obj (dict): order data

        Returns:
            Order: transformed order data
        """
        address = Address(obj["address"]["city"],
                          obj["address"]["district"],
                          obj["address"]["street"],
                          )

        price = int(self._exchange_transform.transform(obj["currency"],
                                                       "TWD",
                                                       obj["price"],
                                                       ))
        currency = "TWD"

        order = Order(obj["id"],
                      obj["name"],
                      address,
                      price,
                      currency,
                      )
        return order

    def validate_and_transform(self, obj:dict) -> Tuple[object,int]:
        validation = self.validate(obj)
        if validation.status != 200:
            return validation.msg, validation.status

        transformed = self.transform(obj).to_dict()
        return transformed, 200
