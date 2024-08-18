# -*- encoding: utf-8 -*-
"""
@File    :  test_app.py
@Time    :  2024/08/17 17:33:46
@Author  :  Kevin Wang
@Desc    :  None
"""

from copy import deepcopy
import json

import pytest

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_make_order_success(client):
    obj = {"id":"A0000001",
           "name":"Melody Holiday Inn",
           "address":{"city":"taipei-city",
                      "district":"da-an-district",
                      "street":"fuxing-south-road",
                      },
           "price":"1025",
           "currency":"TWD",
           }
    response = client.post("/api/orders",
                           data=json.dumps(obj),
                           content_type="application/json",
                           )

    text = deepcopy(obj)
    text["price"] = 1025

    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')) == text

def test_validate_and_transform_exchange_success(client):
    obj = {"id":"A0000001",
           "name":"Melody Holiday Inn",
           "address":{"city":"taipei-city",
                      "district":"da-an-district",
                      "street":"fuxing-south-road",
                      },
           "price":"10",
           "currency":"USD",
           }
    response = client.post("/api/orders",
                           data=json.dumps(obj),
                           content_type="application/json",
                           )

    text = deepcopy(obj)
    text["price"] = 310
    text["currency"] = "TWD"

    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')) == text

def test_make_order_violate_name_non_english(client):
    obj = {"id":"A0000001",
           "name":"美樂蒂 Holiday Inn",
           "address":{"city":"taipei-city",
                      "district":"da-an-district",
                      "street":"fuxing-south-road",
                      },
           "price":"1025",
           "currency":"TWD",
           }
    response = client.post("/api/orders",
                           data=json.dumps(obj),
                           content_type="application/json",
                           )

    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Name contains non-English characters"

def test_make_order_price_over_2000_boundary(client):
    obj = {"id":"A0000001",
           "name":"Melody Holiday Inn",
           "address":{"city":"taipei-city",
                      "district":"da-an-district",
                      "street":"fuxing-south-road",
                      },
           "price":"2000",
           "currency":"TWD",
           }
    response = client.post("/api/orders",
                           data=json.dumps(obj),
                           content_type="application/json",
                           )

    text = deepcopy(obj)
    text["price"] = 2000

    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')) == text


def test_make_order_price_over_2000(client):
    obj = {"id":"A0000001",
           "name":"Melody Holiday Inn",
           "address":{"city":"taipei-city",
                      "district":"da-an-district",
                      "street":"fuxing-south-road",
                      },
           "price":"2001",
           "currency":"TWD",
           }
    response = client.post("/api/orders",
                           data=json.dumps(obj),
                           content_type="application/json",
                           )

    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Price is over 2000"

def test_make_order_violate_name_not_capital(client):
    obj = {"id":"A0000001",
           "name":"Melody holiday Inn",
           "address":{"city":"taipei-city",
                      "district":"da-an-district",
                      "street":"fuxing-south-road",
                      },
           "price":"1025",
           "currency":"TWD",
           }
    response = client.post("/api/orders",
                           data=json.dumps(obj),
                           content_type="application/json",
                           )

    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Name is not capitalized"

def test_make_order_wrong_currency(client):
    obj = {"id":"A0000001",
           "name":"Melody Holiday Inn",
           "address":{"city":"taipei-city",
                      "district":"da-an-district",
                      "street":"fuxing-south-road",
                      },
           "price":"1025",
           "currency":"JPY",
           }
    response = client.post("/api/orders",
                           data=json.dumps(obj),
                           content_type="application/json",
                           )

    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Currency format is wrong"
