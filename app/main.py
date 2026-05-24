from contextlib import asynccontextmanager
from pathlib import Path
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.endpoints import contracts, properties, tenants, users
from app.core.exceptions import (
    CustomException,
    custom_exception_handler,
    custom_validator_handler,
)
from app.core.logging_config import logger


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("connection")
    yield
    logger.info("disconnection")


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, custom_validator_handler)

app.include_router(contracts.router, prefix="/api/v1/contracts", tags=["Contracts"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(properties.router, prefix="/api/v1/properties", tags=["Properties"])
app.include_router(tenants.router, prefix="/api/v1/tenants", tags=["Tenants"])

# Настройка статики
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Настройка шаблонов
templates = Jinja2Templates(directory=str(static_dir))


@app.exception_handler(Exception)
async def global_validator(_request: Request, _exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Сервер упал"})


@app.get("/", response_class=Response)
async def read_root():
    """Отдает главную страницу index.html"""
    try:
        index_path = static_dir / "index.html"
        if index_path.exists():
            with open(index_path, "r", encoding="utf-8") as f:
                return Response(content=f.read(), media_type="text/html")
        else:
            return Response(
                content="<h1>ОШИБКА: Файл static/index.html не найден!</h1>",
                media_type="text/html",
                status_code=404
            )
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        return Response(
            content="<h1>Ошибка сервера при загрузке главной страницы</h1>",
            media_type="text/html",
            status_code=500
        )


if __name__ == "__main__":
    uvicorn.run(app, port=8001)