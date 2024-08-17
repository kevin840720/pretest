# -*- encoding: utf-8 -*-
"""
@File    :  test_service.py
@Time    :  2024/08/16 22:37:09
@Author  :  Kevin Wang
@Desc    :  None
"""

from copy import deepcopy
import json
import pytest

from src.service import (CurrencyValidator,
                         DummyValidator,
                         ExchangeTransform,
                         NameValidator,
                         PriceValidator,
                         Service,
                         ValidateResult,
                         )

dummy_validator = DummyValidator()
name_validator = NameValidator()
price_validator = PriceValidator(price_ub=2000)
currency_validator = CurrencyValidator(["TWD", "USD"])

class TestDummyValidator:
    @pytest.mark.parametrize('obj,expected',
        [("", ValidateResult(200, "")),
         ])
    def test_validate(self, obj:str, expected:ValidateResult):
        validated_obj = dummy_validator.validate(obj)
        assert validated_obj == expected

class TestNameValidator:
    @pytest.mark.parametrize('obj,expected',
        [("Mickey", ValidateResult(200, "")),
         ("Mickey Mouse Hotel", ValidateResult(200, "")),
         ("Mickey mouse Hotel", ValidateResult(400, "Name is not capitalized")),
         ("", ValidateResult(400, "Empty name")),
         ("Mickey001Hotel", ValidateResult(400, "Name contains non-English characters")),
         ("Mickey 001Hotel", ValidateResult(400, "Name contains non-English characters")),
         ])
    def test_validate(self, obj:str, expected:ValidateResult):
        validated_obj = name_validator.validate(obj)
        assert validated_obj == expected

class TestPriceValidator:
    @pytest.mark.parametrize('obj,expected',
        [("1000", ValidateResult(200, "")),
         ("", ValidateResult(400, "Empty price")),
         ("10NTD", ValidateResult(400, "Price contains non-digits characters")),
         ("9999", ValidateResult(400, "Price is over 2000")),
         ])
    def test_validate(self, obj:str, expected:ValidateResult):
        validated_obj = price_validator.validate(obj)
        assert validated_obj == expected

class TestCurrencyValidator:
    @pytest.mark.parametrize('obj,expected',
        [("TWD", ValidateResult(200, "")),
         ("USD", ValidateResult(200, "")),
         ("JPN", ValidateResult(400, "Currency format is wrong")),
         (["TWD", "USD"], ValidateResult(400, "Currency format is wrong")),
         ])
    def test_validate(self, obj:str, expected:ValidateResult):
        validated_obj = currency_validator.validate(obj)
        assert validated_obj == expected


usd_to_twd_exchange = ExchangeTransform(frm_country="USD",
                                        to_country="TWD",
                                        exchange_rate=31,
                                        )

class TestExchangeTransform:
    @pytest.mark.parametrize('price,exchange_transform,expected',
        [(10, usd_to_twd_exchange, 310),
         ])
    def test_transform(self,
                       price:int,
                       exchange_transform:ExchangeTransform,
                       expected:int,
                       ):
        assert expected == exchange_transform.transform(price)
        assert "USD" == exchange_transform.frm_country
        assert "TWD" == exchange_transform.to_country


service_class = Service(NameValidator(),
                        PriceValidator(price_ub=2000),
                        CurrencyValidator(["TWD", "USD"]),
                        ExchangeTransform(frm_country="USD",
                                          to_country="TWD",
                                          exchange_rate=31,
                                          ),
                        )

class TestService:
    def test_validate_and_transform_success(self):
        obj = {"id":"A0000001",
               "name":"Melody Holiday Inn",
               "address":{"city":"taipei-city",
                          "district":"da-an-district",
                          "street":"fuxing-south-road",
                          },
               "price":"1025",
               "currency":"TWD",
               }
        resp_data, resp_status = service_class.validate_and_transform(obj)

        text = deepcopy(obj)
        text["price"] = 1025

        assert resp_status == 200
        assert resp_data == text

    def test_validate_and_transform_exchange_success(self):
        obj = {"id":"A0000001",
               "name":"Melody Holiday Inn",
               "address":{"city":"taipei-city",
                          "district":"da-an-district",
                          "street":"fuxing-south-road",
                          },
               "price":"10",
               "currency":"USD",
               }
        resp_data, resp_status = service_class.validate_and_transform(obj)

        text = deepcopy(obj)
        text["price"] = 310
        text["currency"] = "TWD"
        assert resp_status == 200
        assert resp_data == text

    def test_validate_and_transform_name_non_english(self):
        obj = {"id":"A0000001",
               "name":"美樂蒂 Holiday Inn",
               "address":{"city":"taipei-city",
                          "district":"da-an-district",
                          "street":"fuxing-south-road",
                          },
               "price":"1025",
               "currency":"TWD",
               }
        resp_data, resp_status = service_class.validate_and_transform(obj)

        assert resp_status == 400
        assert resp_data == "Name contains non-English characters"

    def test_validate_and_transform_name_not_capital(self):
        obj = {"id":"A0000001",
               "name":"Melody holiday Inn",
               "address":{"city":"taipei-city",
                          "district":"da-an-district",
                          "street":"fuxing-south-road",
                          },
               "price":"1025",
               "currency":"TWD",
               }
        resp_data, resp_status = service_class.validate_and_transform(obj)

        assert resp_status == 400
        assert resp_data == "Name is not capitalized"

    def test_validate_and_transform_name_not_capital(self):
        obj = {"id":"A0000001",
               "name":"Melody Holiday Inn",
               "address":{"city":"taipei-city",
                          "district":"da-an-district",
                          "street":"fuxing-south-road",
                          },
               "price":"9999",
               "currency":"TWD",
               }
        resp_data, resp_status = service_class.validate_and_transform(obj)

        assert resp_status == 400
        assert resp_data == "Price is over 2000"

    def test_validate_and_transform_wrong_currency(self):
        obj = {"id":"A0000001",
               "name":"Melody Holiday Inn",
               "address":{"city":"taipei-city",
                          "district":"da-an-district",
                          "street":"fuxing-south-road",
                          },
               "price":"1025",
               "currency":"JPY",
               }
        resp_data, resp_status = service_class.validate_and_transform(obj)

        assert resp_status == 400
        assert resp_data == "Currency format is wrong"
