from typing import Any, Optional

from pydantic import BaseModel


class BadRequest(BaseModel):
    """
    Used in `validation_exception_handler` to define a custom response body
    when path operation throws a `RequestValidationError`.
    """
    detail: Optional[list] = []
    body: Optional[Any] = None
