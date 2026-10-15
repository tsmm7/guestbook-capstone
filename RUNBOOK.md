# RUNBOOK

## Быстрая диагностика
```bash
docker compose ps
docker compose logs --tail=100 app
docker compose logs --tail=100 db
curl -i localhost:8000/health
```

## Откат на предыдущую версию
1. Узнать предыдущий тег: `git tag --sort=-v:refname | head` или раздел Packages на GitHub.
2. Откатить (без «v» в начале):
   ```bash
   APP_TAG=1.0.0 docker compose pull app
   APP_TAG=1.0.0 docker compose up -d app
   ```
3. Проверить: `curl localhost:8000/health`, `curl localhost:8000/messages`.
4. Записать `APP_TAG=1.0.0` в `.env`, чтобы версия не сбросилась при перезапуске.

Откат безопасен, пока схема БД обратно совместима: новые колонки только nullable или с DEFAULT, старые не удаляются и не переименовываются. Данные при откате не теряются (volume `postgres_data`).

## Симптомы и действия
| Симптом | Что делать |
|---|---|
| `app` постоянно перезапускается | `docker compose logs app`; чаще всего неверный `.env` или БД недоступна |
| `app` unhealthy | `docker compose exec app uv run --no-sync python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').read())"` |
| `db` unhealthy | `docker compose logs db`; проверить `POSTGRES_*` в `.env` |
| `pull` отдаёт `denied` / `not found` | проверить `IMAGE_NAME` (строчные буквы) и тег; для приватного пакета: `docker login ghcr.io` |
| Нужен последний рабочий образ | `APP_TAG=latest` или предыдущий тег из Packages |

## Перезапуск
```bash
docker compose restart app
docker compose up -d --force-recreate app
```

## Бэкап БД
```bash
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > backup.sql
```

## Чего не делать
- `docker compose down -v` удаляет volume с данными.
- Не удалять и не переименовывать колонки в одном релизе с кодом, который их использует.
