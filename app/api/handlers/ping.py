from fastapi import APIRouter

router = APIRouter()


@router.get("/app")
def ping_app():
    return {"message": "ok"}
