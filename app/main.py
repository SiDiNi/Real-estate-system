from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
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

app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(properties.router, prefix="/api/v1/properties", tags=["Properties"])
app.include_router(tenants.router, prefix="/api/v1/tenants", tags=["Tenants"])
app.include_router(contracts.router, prefix="/api/v1/contracts", tags=["Contracts"])

app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)

templates = Jinja2Templates(directory="app/static")


@app.exception_handler(Exception)
async def global_validator(_request: Request, _exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Сервер упал"})


if __name__ == "__main__":
    uvicorn.run(app, port=8001)
