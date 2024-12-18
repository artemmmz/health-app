from typing import Any, List

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import (
    AlreadyExistsError,
    InvalidAuthCodeError,
    InvalidAuthSchemeError,
    InvalidLoginError,
    InvalidTokenError,
    NoResultError,
    UnauthorizedError,
    ForbiddenError,
    InvalidTokenTypeError,
)


def get_error_response(
    status_code: int, error_messages: List[Any]
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code, content={"detail": error_messages}
    )


# Custom Errors
async def already_exists_error_handler(
    _: Request, exc: AlreadyExistsError | Exception  #
):
    if isinstance(exc.model, str):
        name = exc.model
    elif exc.model is None:
        name = ''
    else:
        name = exc.model.__name__
    return get_error_response(409, [f"{name} already exists"])


async def forbidden_error_handler(_: Request, __: ForbiddenError | Exception):
    return get_error_response(403, ['Forbidden'])


async def invalid_auth_code_error_handler(
    _: Request, __: InvalidAuthCodeError | Exception
):
    return get_error_response(400, ["Invalid authentication code"])


async def invalid_auth_scheme_error_handler(
    _: Request, __: InvalidAuthSchemeError | Exception
):
    return get_error_response(400, ["Invalid authentication scheme"])


async def invalid_login_error_handler(
    _: Request, __: InvalidLoginError | Exception
):
    return get_error_response(400, ["Username or password incorrect"])


async def invalid_token_error_handler(
    _: Request, __: InvalidTokenError | Exception
):
    return get_error_response(400, ["Token is invalid or expired"])


async def invalid_token_type_error_handler(
    _: Request, exc: InvalidTokenTypeError | Exception
):
    return get_error_response(
        400,
        [f"Invalid token type. Found {exc.found}, expected {exc.expected}"],
    )


async def no_result_error_handler(_: Request, exc: NoResultError | Exception):
    if isinstance(exc.model, str):
        name = exc.model
    elif exc.model is None:
        name = ''
    else:
        name = exc.model.__name__
    return get_error_response(400, [f"{name} not found"])


async def unauthorized_error_handler(
    _: Request, __: UnauthorizedError | Exception
):
    return get_error_response(401, ["Unauthorized"])


# Other errors
async def other_error_handler(_: Request, __: Exception):
    return get_error_response(500, ["Internal Server Error"])


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(AlreadyExistsError, already_exists_error_handler)
    app.add_exception_handler(ForbiddenError, forbidden_error_handler)
    app.add_exception_handler(
        InvalidAuthCodeError, invalid_auth_code_error_handler
    )
    app.add_exception_handler(
        InvalidAuthSchemeError, invalid_auth_scheme_error_handler
    )
    app.add_exception_handler(InvalidLoginError, invalid_login_error_handler)
    app.add_exception_handler(InvalidTokenError, invalid_token_error_handler)
    app.add_exception_handler(
        InvalidTokenTypeError, invalid_token_type_error_handler
    )
    app.add_exception_handler(NoResultError, no_result_error_handler)
    app.add_exception_handler(UnauthorizedError, unauthorized_error_handler)
    app.add_exception_handler(Exception, other_error_handler)
