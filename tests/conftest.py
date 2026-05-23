# tests/conftest.py
import pytest
import sys
from pathlib import Path
from httpx import AsyncClient, ASGITransport

# Добавляем корень проекта в пути, чтобы видеть 'app'
sys.path.append(str(Path(__file__).parent.parent))

from app.main import app

@pytest.fixture(scope="function")
async def client():
    """Простой клиент без манипуляций с БД. Тесты будут ходить в твою реальную базу."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac