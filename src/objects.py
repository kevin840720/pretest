# -*- encoding: utf-8 -*-
"""
@File    :  objects.py
@Time    :  2024/08/16 05:50:52
@Author  :  Kevin Wang
@Desc    :  None
"""

from dataclasses import dataclass

@dataclass
class Exchange:
    source:str
    target:str
    rate:float

    def __mul__(self, price:int|float):
        return self.rate * price

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
