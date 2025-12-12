from app.database.connection import get_master_db
from app.utils.hashing import hash_password
from pymongo.errors import CollectionInvalid
from bson import ObjectId
from datetime import datetime
from typing import Dict, Any
from fastapi import HTTPException, status

def _safe_collection_name(org_name: str) -> str:
    name = org_name.strip().lower().replace(" ", "_")
    return f"org_{name}"

def create_organization(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates an organization:
    - Validates if org exists in master DB
    - Creates a tenant collection for the org
    - Creates an admin user document in master DB (admins collection)
    - Stores metadata in organizations collection
    """
    db = get_master_db()
    org_raw = payload["organization_name"]
    admin_email = payload["email"].lower().strip()
    password = payload["password"]

    org_key = org_raw.strip().lower()
    collection_name = _safe_collection_name(org_raw)

    # 1. Check existing org by normalized name
    existing = db["organizations"].find_one({"organization_name": org_key})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="An organization with that name already exists.")

    # 2. Create tenant collection (if you want initial schema/seed, do it here)
    try:
        db.create_collection(collection_name)
    except CollectionInvalid:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to allocate storage for the new organization. Try again.")

    # 3. Create admin user in master admins collection
    hashed_pw = hash_password(password)
    admin_doc = {
        "email": admin_email,
        "password": hashed_pw,
        "role": "admin",
        "created_at": datetime.utcnow()
    }
    insert_result = db["admins"].insert_one(admin_doc)
    admin_id = insert_result.inserted_id

    # 4. Create organization metadata record
    org_metadata = {
        "organization_name": org_key,
        "display_name": org_raw.strip(),
        "collection_name": collection_name,
        "admin_id": admin_id,
        "created_at": datetime.utcnow()
    }
    db["organizations"].insert_one(org_metadata)

    # return a safe response
    return {
        "message": "Organization created successfully.",
        "organization": {
            "organization_name": org_key,
            "display_name": org_raw.strip(),
            "collection_name": collection_name,
            "admin_id": str(admin_id)
        }
    }

def get_organization(org_name: str) -> Dict[str, Any]:
    db = get_master_db()
    org_key = org_name.strip().lower()
    org = db["organizations"].find_one({"organization_name": org_key})
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Organization not found.")
    org["admin_id"] = str(org["admin_id"])
    org["_id"] = str(org["_id"])
    org.pop("_id", None)
    return org

def delete_organization(org_name: str, requesting_admin_id: str) -> Dict[str, Any]:
    db = get_master_db()
    org_key = org_name.strip().lower()
    org = db["organizations"].find_one({"organization_name": org_key})
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Organization not found.")
    if str(org["admin_id"]) != str(requesting_admin_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to delete this organization.")

    collection_name = org["collection_name"]
    db.drop_collection(collection_name)
    db["admins"].delete_one({"_id": org["admin_id"]})
    db["organizations"].delete_one({"_id": org["_id"]})

    return {"message": "Organization and related resources removed successfully."}
