from fastapi import APIRouter, Depends
from app.schemas.org_schemas import CreateOrgRequest
from app.services.org_service import create_organization, get_organization, delete_organization
from app.dependencies.auth import get_current_admin
from fastapi import HTTPException, status

router = APIRouter(tags=["Organization"])

@router.post("/org/create", status_code=status.HTTP_201_CREATED)
def api_create_org(payload: CreateOrgRequest):
    """
    Create an organization and a tenant collection. Returns basic metadata.
    """
    result = create_organization(payload.dict())
    return result

@router.get("/org/get")
def api_get_org(organization_name: str):
    """
    Get organization metadata by name.
    """
    return get_organization(organization_name)

@router.delete("/org/delete")
def api_delete_org(organization_name: str, current_admin = Depends(get_current_admin)):
    """
    Delete organization. Only the admin who is stored as the organization's admin can delete.
    current_admin is taken from JWT token.
    """
    # current_admin is the payload returned by get_current_admin
    requesting_admin_id = current_admin.get("admin_id")
    return delete_organization(organization_name, requesting_admin_id)
