from pydantic import BaseModel, EmailStr, Field

class CreateOrgRequest(BaseModel):
    organization_name: str = Field(..., min_length=2, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=6)
