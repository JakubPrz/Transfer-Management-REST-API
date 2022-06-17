from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from . import models
from .database import engine
from .exceptions.handlers import validation_exception_handler
from .routers.transfers import router


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Transfer Management REST API Application")
app.include_router(router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
