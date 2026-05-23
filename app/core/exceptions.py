from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.schemas import CustomExceptionModel


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message


async def custom_exception_handler(
    _request: Request, exc: CustomException
) -> JSONResponse:
    error = jsonable_encoder(
        CustomExceptionModel(
            status_code=exc.status_code, detail=exc.detail, message=exc.message
        )
    )
    return JSONResponse(status_code=exc.status_code, content=error)


async def custom_validator_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    list_errors = [
        {"field": error["loc"][-1], "message": error["msg"]} for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"detail": "Ошибка валидации данных", "errors": list_errors},
    )
