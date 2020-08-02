# Harmohy Hub Server

Сервер для Harmohy Hub 

# Деплой

Собираем Docker-образ:

```sh
docker build -t harmony-hub-server .
```

Запуск:

```sh
docker run -d \
--name harmony-sever \
--restart always \
-p 32670:32670 \
-e HUB_IP='192.168.1.65' \
harmony-hub-server
```



