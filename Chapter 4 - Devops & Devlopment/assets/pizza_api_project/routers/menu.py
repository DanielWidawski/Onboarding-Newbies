from typing import Any

from fastapi import APIRouter

from models import default_menu

router = APIRouter(prefix="/menu")


@router.get("/")
def get_menu() -> dict[str, Any]:
    return default_menu.model_dump()
