from fastapi import APIRouter

from app.core.standard_profile import STANDARD_PROFILE

router = APIRouter(tags=["standards"])


@router.get("/standards/main-groups")
def get_main_groups():
    return STANDARD_PROFILE["main_groups"]
