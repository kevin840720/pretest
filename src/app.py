# -*- encoding: utf-8 -*-
"""
@File    :  app.py
@Time    :  2024/08/16 05:44:36
@Author  :  Kevin Wang
@Desc    :  None
"""

from flask import (Flask,
                   request,
                   )
from service import (CurrencyValidator,
                     ExchangeTransform,
                     NameValidator,
                     PriceValidator,
                     Service,
                     )
from utils import (FieldChecker,
                   InputFormatCheck,
                   TypeChecker,
                   )

NECESSARY_FIELDS = {
    "id": str,
    "name": str,
    "address": {
        "city": str,
        "district": str,
        "street": str,
    },
    "price": str,
    "currency": str
}

input_checker = InputFormatCheck([FieldChecker(NECESSARY_FIELDS),
                                  TypeChecker(NECESSARY_FIELDS),
                                  ])
service_class = Service(NameValidator(),
                        PriceValidator(price_ub=2000),
                        CurrencyValidator(["TWD", "USD"]),
                        ExchangeTransform(frm_country="USD",
                                          to_country="TWD",
                                          exchange_rate=31,
                                          ),
                        )

app = Flask(__name__)

@app.post("/api/orders")
def make_order():
    obj = request.get_json()
    check_flag = input_checker.check(obj)

    if check_flag == False:
        return "Wrong input format", 400

    result, status = service_class.validate_and_transform(obj)
    return result, status

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=15000,
            )
