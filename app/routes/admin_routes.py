from fastapi import APIRouter
from app.schemas.admin_schemas import AdminLoginRequest, TokenResponse
from app.services.admin_service import admin_login

router = APIRouter(tags=["Admin"])

@router.post("/admin/login", response_model=TokenResponse)
def api_admin_login(payload: AdminLoginRequest):
    return admin_login(payload.email, payload.password)
