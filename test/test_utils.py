# -*- encoding: utf-8 -*-
"""
@File    :  test_utils.py
@Time    :  2024/08/16 20:46:28
@Author  :  Kevin Wang
@Desc    :  None
"""

import pytest

from utils import (FieldChecker,
                   InputFormatCheck,
                   TypeChecker,
                   )

input_format = {
    "A": str,
    "B": int,
    "C": {"a": bool,
          "b": None,
          }
}
field_checker = FieldChecker(input_format)
type_checker = TypeChecker(input_format)
input_checker = InputFormatCheck([field_checker, type_checker])

class TestFieldChecker:
    @pytest.mark.parametrize('obj,expected',
        [({"A":"","B":10,"C":{"a":True,"b":None}}, True),
         ({"A":"","B":10,"C":{"a":True,"b":None}, "D":""}, True),
         ({"B":10,"C":{"a":True,"b":None}}, False),
         ({"Z":"","B":10,"C":{"a":True,"b":None}}, False),
         ({"A":10,"B":10,"C":{"a":1000,"b":None}}, True),  # FieldChecker 不檢驗型別
         ({"A":10,"B":10,"C":1000}, True),                 # FieldChecker 不檢驗型別
         ({"A":"","B":10,"C":{"b":None}}, False),
         ])
    def test_check(self, obj:dict, expected:bool):
        check_obj = field_checker.check(obj)
        assert check_obj == expected

class TestTypeChecker:
    @pytest.mark.parametrize('obj,expected',
        [({"A":"","B":10,"C":{"a":True,"b":None}}, True),
         ({"A":"","B":10,"C":{"a":True,"b":None}, "D":""}, True),
         ({"A":10,"B":10,"C":{"a":True,"b":None}}, False),
         ({"A":"","B":10,"C":{"a":True,"b":""}}, False),
         ({"A":10,"B":10,"C":1000}, False),
         ])
    def test_check(self, obj:dict, expected:bool):
        check_obj = type_checker.check(obj)
        assert check_obj == expected

class TestInputFormatCheck:
    @pytest.mark.parametrize('obj,expected',
        [({"A":"","B":10,"C":{"a":True,"b":None}}, True),
         ({"A":"","B":10,"C":{"a":True,"b":None}, "D":""}, True),
         ({"B":10,"C":{"a":True,"b":None}}, False),
         ({"Z":"","B":10,"C":{"a":True,"b":None}}, False),
         ({"A":10,"B":10,"C":{"a":True,"b":None}}, False),
         ({"A":"","B":10,"C":{"a":1000,"b":None}}, False),
         ({"A":10,"B":10,"C":1000}, False),
         ({"A":"","B":10,"C":{"b":None}}, False),
         ])
    def test_check(self, obj:dict, expected:bool):
        check_obj = input_checker.check(obj)
        assert check_obj == expected