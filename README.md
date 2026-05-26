🏠 Real Estate Coursework
Система управления недвижимостью (курсовая работа).

🚀 Быстрый запуск

1. Активируй виртуальное окружение
venv\Scripts\activate

2. Настрой pre-commit
pip install pre-commit black isort flake8
активация в терминале(если нужно):
black .
flake8 .
isort .

3. Установи зависимости
pip install -r requirements.txt

4. Настрой базу данных
Создай БД PostgreSQL (например, real_estate_db)
Проверь подключение в .env или в коде (если хардкод)

5. Запусти сервер
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
Или можно запустить F5 в файле app/main.py
Сервер запустится на: http://127.0.0.1:8001

🗄️ Миграции (Alembic)
# Создать миграцию после изменения моделей
alembic revision --autogenerate -m "Описание изменений"

# Применить миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1

# Проверить текущую версию БД
alembic current