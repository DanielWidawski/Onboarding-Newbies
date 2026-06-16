from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Request, Response

from exceptions.exceptions import ValidationError
from exceptions.handler import validation_error_handler

exception_handler_mapping: dict[
    int | type[Exception],
    Callable[[Request, Any], Coroutine[Any, Any, Response]],
] = {}

exception_handler_mapping[ValidationError] = validation_error_handler
