# -*- encoding: utf-8 -*-
"""
@File    :  objects.py
@Time    :  2024/08/16 05:50:52
@Author  :  Kevin Wang
@Desc    :  None
"""

from dataclasses import dataclass, field
from typing import Literal

@dataclass
class StructureCheck:
    errors:list=field(default_factory=list)

    def __post_init__(self):
        assert isinstance(self.errors, list), ValueError("attribute `errors`: list is required")

    @property
    def status(self):
        return True if len(self.errors) == 0 else False

    def merge(self, obj):
        self.errors += obj.errors

@dataclass
class Address:
    city:str
    district:str
    street:str

    def to_dict(self):
        return {"city": self.city,
                "district": self.district,
                "street": self.street,
                }

@dataclass
class Order:
    id:str
    name:str
    address:Address
    price:int
    currency:str

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "address": self.address.to_dict(),
                "price": self.price,
                "currency": self.currency,
                }
