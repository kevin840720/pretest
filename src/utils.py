# -*- encoding: utf-8 -*-
"""
@File    :  utils.py
@Time    :  2024/08/16 05:51:05
@Author  :  Kevin Wang
@Desc    :  None
"""
from abc import ABC
from typing import (List,
                    Union,
                    )

class Checker(ABC):
    def check(self, obj:dict) -> bool:
        raise NotImplementedError

class FieldChecker(Checker):
    def __init__(self,
                 structure:dict,
                 ) -> None:
        self._structure = structure

        self._obj:Union[None,dict] = None
        self._standard:Union[None,dict] = None
        self._errors:List[str] = []

    def clean(self):
        self._obj = None
        self._standard = None
        self._errors = []

    def _check_recursive(self,
                         obj:dict,
                         standard:dict,
                         prefix="",
                         ) -> List[str]:
        errors = []
        for key in standard.keys():
            if key not in obj:
                errors.append(f"Missing field: {(prefix + '.' + key) if prefix else key}")
            elif (isinstance(standard[key], dict) 
                and isinstance(obj[key], dict)
                ):
                errors += self._check_recursive(obj[key], standard[key], key)
        return errors

    def check(self, obj:dict) -> bool:
        self.clean()
        errors = self._check_recursive(obj,
                                       self._structure,
                                       prefix="",
                                       )
        print(errors)
        if len(errors) > 0:
            return False
        return True
    
    @property
    def errors(self):
        return self._errors

class TypeChecker(Checker):
    def __init__(self,
                 structure:dict,
                 ) -> None:
        self._structure = structure

        self._obj:Union[None,dict] = None
        self._standard:Union[None,dict] = None
        self._errors:List[str] = []

    def clean(self):
        self._obj = None
        self._standard = None
        self._errors = []

    def _check_recursive(self,
                         obj:dict,
                         standard:dict,
                         prefix="",
                         ) -> List[str]:
        errors = []
        for key in standard.keys():
            if standard[key] == None:  # None 不能放在 isinstance arg2
                if obj[key] != None:
                    errors.append(f"Inconsistent type: {(prefix + '.' + key) if prefix else key}")
            elif isinstance(standard[key], dict):
                if isinstance(obj[key], dict):
                    errors += self._check_recursive(obj[key], standard[key], key)
                else:
                    errors.append(f"Inconsistent type: {(prefix + '.' + key) if prefix else key}")
            elif not isinstance(obj[key], standard[key]):
                errors.append(f"Inconsistent type: {(prefix + '.' + key) if prefix else key}")
        return errors

    def check(self, obj:dict) -> bool:
        self.clean()
        errors = self._check_recursive(obj,
                                       self._structure,
                                       prefix="",
                                       )
        if len(errors) > 0:
            return False
        return True
    
    @property
    def errors(self):
        return self._errors

class InputFormatCheck:
    def __init__(self, checkers:List[Checker]) -> None:
        self._checkers = checkers

    @property
    def checkers(self):
        return self._checkers

    def check(self, obj:dict) -> bool:
        for checker in self.checkers:
            if checker.check(obj) is False:
                return False
        return True
