# PreTest

- 訂單金額 > 2000 是指台幣計價，還是只需要對數字進行檢查

## How to start

<!-- - For Linux environment, please set `sysctl -w vm.max_map_count=262144` -->

```sh
docker compose -f './docker-compose.yml' up
```

Order API: `http://0.0.0.0:15000/api/orders`