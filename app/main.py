from fastapi import FastAPI
from app.routes import org_routes, admin_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="OrgSphere Backend", version="1.0")

app.include_router(admin_routes.router)
app.include_router(org_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


