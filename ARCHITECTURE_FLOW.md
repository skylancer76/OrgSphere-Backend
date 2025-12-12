# OrgSphere Backend - Architecture Flow Diagram

## High-Level Architecture Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT/FRONTEND                           │
│                    (API Requests/Responses)                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI APPLICATION                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    CORS Middleware                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             │                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Route Handlers                         │   │
│  │  ┌──────────────┐              ┌──────────────┐          │   │
│  │  │ Admin Routes │              │  Org Routes  │          │   │
│  │  │ /admin/login │              │ /org/create  │          │   │
│  │  │              │              │ /org/get     │          │   │
│  │  │              │              │ /org/update  │          │   │
│  │  │              │              │ /org/delete  │          │   │
│  │  └──────┬───────┘              └──────┬───────┘          │   │
│  └─────────┼──────────────────────────────┼──────────────────┘   │
│            │                              │                      │
│  ┌─────────▼──────────────────────────────▼──────────────────┐   │
│  │              Authentication Dependency                    │   │
│  │         (JWT Token Validation for Protected Routes)      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             │                                     │
│  ┌─────────────────────────▼─────────────────────────────────┐   │
│  │                    Service Layer                           │   │
│  │  ┌──────────────────┐        ┌──────────────────┐         │   │
│  │  │  Admin Service   │        │  Org Service     │         │   │
│  │  │  - Login         │        │  - Create        │         │   │
│  │  │  - Auth          │        │  - Get           │         │   │
│  │  │                  │        │  - Update         │         │   │
│  │  │                  │        │  - Delete        │         │   │
│  │  └────────┬─────────┘        └────────┬─────────┘         │   │
│  └───────────┼───────────────────────────┼───────────────────┘   │
│              │                           │                        │
│  ┌───────────▼───────────────────────────▼───────────────────┐   │
│  │                    Utility Layer                           │   │
│  │  ┌──────────────┐        ┌──────────────┐                  │   │
│  │  │   Hashing    │        │  JWT Handler │                  │   │
│  │  │  - bcrypt    │        │  - Create    │                  │   │
│  │  │  - Verify    │        │  - Decode    │                  │   │
│  │  └──────────────┘        └──────────────┘                  │   │
│  └────────────────────────────────────────────────────────────┘   │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE CONNECTION LAYER                     │
│              (MongoDB Client - Master Database)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MONGODB DATABASE                              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              MASTER DATABASE (orgsphere_master)           │  │
│  │                                                            │  │
│  │  ┌──────────────────┐  ┌──────────────────┐              │  │
│  │  │  organizations   │  │     admins       │              │  │
│  │  │  Collection      │  │   Collection    │              │  │
│  │  │                  │  │                  │              │  │
│  │  │  - org_name      │  │  - email         │              │  │
│  │  │  - collection    │  │  - password     │              │  │
│  │  │    _name         │  │    (hashed)     │              │  │
│  │  │  - admin_id      │  │  - role          │              │  │
│  │  │  - created_at    │  │  - created_at    │              │  │
│  │  └──────────────────┘  └──────────────────┘              │  │
│  │                                                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │     DYNAMIC ORGANIZATION COLLECTIONS               │  │  │
│  │  │     (Created per organization)                      │  │  │
│  │  │                                                    │  │  │
│  │  │  org_testorg                                      │  │  │
│  │  │  org_company1                                     │  │  │
│  │  │  org_company2                                     │  │  │
│  │  │  ... (one per organization)                       │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow Examples

### 1. Create Organization Flow

```
Client Request
    │
    ▼
POST /org/create
    │
    ▼
Route Handler (org_routes.py)
    │
    ▼
Service Layer (org_service.py)
    │
    ├─► Validate organization_name doesn't exist
    │
    ├─► Create dynamic collection (org_<name>)
    │
    ├─► Hash password (bcrypt)
    │
    ├─► Create admin document in 'admins' collection
    │
    ├─► Create organization metadata in 'organizations' collection
    │
    └─► Return success response
```

### 2. Admin Login Flow

```
Client Request
    │
    ▼
POST /admin/login
    │
    ▼
Route Handler (admin_routes.py)
    │
    ▼
Service Layer (admin_service.py)
    │
    ├─► Find admin by email in 'admins' collection
    │
    ├─► Verify password (bcrypt)
    │
    ├─► Find organization linked to admin
    │
    ├─► Generate JWT token (contains admin_id, email, organization)
    │
    └─► Return JWT token
```

### 3. Update Organization Flow (Protected)

```
Client Request (with JWT token)
    │
    ▼
PUT /org/update
    │
    ▼
Authentication Dependency (auth.py)
    │
    ├─► Extract JWT token from header
    │
    ├─► Decode and validate token
    │
    └─► Extract admin_id from token
    │
    ▼
Route Handler (org_routes.py)
    │
    ▼
Service Layer (org_service.py)
    │
    ├─► Find organization by admin_id
    │
    ├─► Validate new organization_name doesn't exist
    │
    ├─► If name changed:
    │   ├─► Create new collection
    │   ├─► Migrate data from old collection
    │   └─► Drop old collection
    │
    ├─► Update admin email/password
    │
    ├─► Update organization metadata
    │
    └─► Return success response
```

### 4. Delete Organization Flow (Protected)

```
Client Request (with JWT token)
    │
    ▼
DELETE /org/delete?organization_name=...
    │
    ▼
Authentication Dependency (auth.py)
    │
    ├─► Validate JWT token
    │
    └─► Extract admin_id
    │
    ▼
Route Handler (org_routes.py)
    │
    ▼
Service Layer (org_service.py)
    │
    ├─► Find organization by name
    │
    ├─► Verify admin_id matches (authorization)
    │
    ├─► Drop organization's collection
    │
    ├─► Delete admin document
    │
    ├─► Delete organization metadata
    │
    └─► Return success response
```

## Data Flow Diagram

```
┌─────────────┐
│   Request   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Pydantic       │
│  Schema         │──► Input Validation
│  Validation     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Service        │──► Business Logic
│  Layer          │    - Data Processing
└──────┬──────────┘    - Validation Rules
       │
       ▼
┌─────────────────┐
│  Database       │──► MongoDB Operations
│  Operations     │    - CRUD Operations
└──────┬──────────┘    - Collection Management
       │
       ▼
┌─────────────────┐
│  Response       │──► JSON Response
│  Formation      │    - Success/Error
└─────────────────┘
```

## Component Interactions

```
┌──────────────┐         ┌──────────────┐
│   Routes     │────────►│  Services    │
│  (HTTP)      │         │  (Business)  │
└──────┬───────┘         └──────┬───────┘
       │                        │
       │                        ▼
       │              ┌──────────────┐
       │              │   Utils      │
       │              │  (Hashing,   │
       │              │   JWT)       │
       │              └──────┬───────┘
       │                     │
       ▼                     ▼
┌──────────────┐    ┌──────────────┐
│ Dependencies │    │  Database    │
│  (Auth)      │    │  Connection  │
└──────────────┘    └──────────────┘
```

## Multi-Tenant Architecture Flow

```
Organization A
    │
    ├─► Master DB: organizations collection
    │   └─► Metadata: org_a, collection_name: org_a
    │
    └─► Dynamic Collection: org_a
        └─► Organization-specific data

Organization B
    │
    ├─► Master DB: organizations collection
    │   └─► Metadata: org_b, collection_name: org_b
    │
    └─► Dynamic Collection: org_b
        └─► Organization-specific data

Organization C
    │
    ├─► Master DB: organizations collection
    │   └─► Metadata: org_c, collection_name: org_c
    │
    └─► Dynamic Collection: org_c
        └─► Organization-specific data
```

## Security Flow

```
Request with Token
    │
    ▼
Extract Bearer Token
    │
    ▼
Decode JWT Token
    │
    ├─► Valid? ──► Extract admin_id, organization
    │   │
    │   └─► Continue to route handler
    │
    └─► Invalid? ──► Return 401 Unauthorized
```

This flow diagram can be used to create a visual flowchart using tools like:
- Draw.io
- Lucidchart
- Mermaid (if supported)
- Any flowchart creation tool
