from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse


def validation_exception_handler(request: Request,
                                 exc: RequestValidationError) -> JSONResponse:
    """
    Creates a JSON response with details of the exception. This is to override
    a default 422 HTTP error with 400 HTTP status code and custom response body
    when path operation throws a `RequestValidationError`.
    :param request: An HTTP request.
    :param exc: The `RequestValidationError thrown by a path operation.
    :return: An instance of a JSONResponse object with custom response body and
        HTTP 400 status code.
    """
    body = {"detail": exc.errors(), "body": exc.body}
    return JSONResponse(content=jsonable_encoder(body),
                        status_code=status.HTTP_400_BAD_REQUEST)
