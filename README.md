# This is a repository for Moscow Travel Hack 2024 ECom solution of Amazing Digital MISIS team


## Архитектура решения
- [Сайт](https://amazing-digital-misis.ru/) решения
- Сваггер [документация](https://amazing-digital-misis.ru:8000/docs)

#### Диаграмма решения
![arch](docs/arch.svg)<br>
Все компаненты контейнерезированы:
- `nginx` - Reverse-proxy, роутинг, SSL
- `frontend` - React SPA приложение для фронтенда
- `backend` - Python backend, использует `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic` и `gigachain`
- `redis` - Key-value СУБД
- `postgres` - Реляционая СУБД с расширением pg-vector

#### Запуск решения
##### В докере
C ssl
```sh
docker compose up # С SSL
```
Без ssl
```sh
docker compose -f docker-compose-nossl.yaml up
```
Локально
```sh
make frontend-install

make backend-install

make infra-run

make frontend-run # В отдельном терминале

make backend-run # В отдельном терминале
```
