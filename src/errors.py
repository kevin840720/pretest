# -*- encoding: utf-8 -*-
"""
@File    :  errors.py
@Time    :  2024/08/16 06:04:45
@Author  :  Kevin Wang
@Desc    :  None
"""

class NameFormatException(ValueError):
    pass

class NameContainsNonEnglish(NameFormatException):
    pass

class NameIsNotCapitalized(NameFormatException):
    pass


class PriceFormatException(ValueError):
    pass

class PriceExceedTwoThousans(PriceFormatException):
    pass


class CurrencyFormatException(ValueError):
    pass

class IllegalCurrencyType(CurrencyFormatException):
    pass