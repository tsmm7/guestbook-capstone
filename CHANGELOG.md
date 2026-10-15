# Changelog

Формат: [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), версии по [SemVer](https://semver.org/lang/ru/).

## [1.1.0] - YYYY-MM-DD
### Added
- Эндпоинт `GET /version`.
- Колонка `messages.created_at` (nullable, `DEFAULT now()`), добавляется при старте через `ADD COLUMN IF NOT EXISTS`.

## [1.0.0] - YYYY-MM-DD
### Added
- Гостевая книга: `GET/POST /messages`, `GET /health`.
- Docker, compose с PostgreSQL, CI (Ruff + pytest), публикация образа в ghcr.io.
