# PreTest

## How to start

### Establish environment

<!-- - For Linux environment, please set `sysctl -w vm.max_map_count=262144` -->

```sh
docker compose -f './docker-compose.yml' up
```

### API

- Order API (POST): `http://0.0.0.0:15000/api/orders`

curl example:

```sh
curl --location 'http://0.0.0.0:15000/api/orders' \
--header 'Content-Type: application/json' \
--data '{"id":"A0000001",
         "name":"Melody Holiday Inn",
         "address":{"city":"taipei-city",
                    "district":"da-an-district",
                    "street":"fuxing-south-road"
                    },
         "price": "1",
         "currency":"TWD"
         }'
```

## 還原開發環境

1. 安裝 Python 3.11
2. 安裝 pipenv (`pip install pipenv`)
3. 還原開發環境 (`pipenv install -d`)
4. 運行測試 (`pipenv run pytest`)
