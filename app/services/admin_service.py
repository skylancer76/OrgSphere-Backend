from app.database.connection import get_master_db
from app.utils.hashing import verify_password
from app.utils.jwt_handler import create_access_token
from fastapi import HTTPException, status
from bson import ObjectId
from typing import Dict, Any

def admin_login(email: str, password: str) -> Dict[str, Any]:
    db = get_master_db()
    admin = db["admins"].find_one({"email": email.lower().strip()})
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid email or password.")

    if not verify_password(password, admin["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid email or password.")

    # find organization linked to this admin (if any)
    org = db["organizations"].find_one({"admin_id": admin["_id"]})
    org_identifier = None
    if org:
        org_identifier = org["organization_name"]

    # Build token payload
    payload = {
        "admin_id": str(admin["_id"]),
        "email": admin["email"],
        "organization": org_identifier
    }
    token = create_access_token(payload)
    return {"access_token": token, "token_type": "bearer"}
