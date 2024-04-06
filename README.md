# This is a repository for Moscow Travel Hack 2024 ECom solution of Amazing Digital MISIS team


## Архитектура решения
- [Сайт](https://amazing-digital-misis.ru/) решения
- Сваггер [документация](https://amazing-digital-misis.ru:8000/docs)

#### Диаграмма решения
![arch](docs/arch.svg)
Все компаненты контейнерезированы:
- nginx - reverse-proxy
- frontend
- backend
- redis
- postgresql

#### Запуск решения
```bash
# Установить docker
docker compose up # С SSL

# docker compose -f docker-compose-nossl.yaml up # Без ssl
```
