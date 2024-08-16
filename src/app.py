# -*- encoding: utf-8 -*-
"""
@File    :  app.py
@Time    :  2024/08/16 05:44:36
@Author  :  Kevin Wang
@Desc    :  None
"""

from flask import Flask, Response
from utils import FieldChecker, TypeChecker, InputFormatCheck

NECESSARY_FIELDS = {
    "id": str,
    "name": str,
    "address": {
        "city": str,
        "district": str,
        "road": str,
    },
    "price": str,
    "currency": str
}

input_checker = InputFormatCheck([FieldChecker(NECESSARY_FIELDS),
                                  TypeChecker(NECESSARY_FIELDS),
                                  ])


app = Flask(__name__)

@app.route("/api/orders")
def make_order(obj:dict):
    check_flag = input_checker(obj)

    if check_flag == False:
        return Response(f"Wrong input format",
                        status=400,
                        )
    
    return "A"

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=15000,
            )
