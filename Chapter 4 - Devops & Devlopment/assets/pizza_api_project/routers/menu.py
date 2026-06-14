from fastapi import APIRouter
from models import default_menu

router = APIRouter(prefix="/menu")


@router.get("/")
def get_menu():
    return default_menu
