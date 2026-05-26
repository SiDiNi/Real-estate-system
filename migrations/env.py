import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. НАСТРОЙКА ПУТЕЙ И .ENV
# -----------------------------------------------------------------------------

# Добавляем корень проекта в sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Загружаем .env
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# -----------------------------------------------------------------------------
# 2. ИМПОРТ МОДЕЛЕЙ (ОБЯЗАТЕЛЬНО!)
# -----------------------------------------------------------------------------
# Замени эти импорты на свои реальные пути!
# Если Alembic не увидит импорты моделей, миграция будет пустой.

try:
    # Пример: отсюда берется Base.metadata
    from app.database.db import Base

    # Пример: импортируем модели, чтобы они зарегистрировались в Base
    from app.models.models import User, Property, Tenant, Contract, Payment, Request

except ImportError as e:
    print(f"Ошибка импорта моделей: {e}")
    print("Убедись, что пути в migrations/env.py верные!")
    sys.exit(1)

target_metadata = Base.metadata

# -----------------------------------------------------------------------------
# 3. ПОЛУЧЕНИЕ URL
# -----------------------------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ Не найдена переменная DATABASE_URL в файле .env")

# -----------------------------------------------------------------------------
# 4. ФУНКЦИИ MIGRATIONS
# -----------------------------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    # Создаем движок напрямую, не через engine_from_config, чтобы избежать проблем с ключами
    from sqlalchemy import create_engine

    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()