## Detailed Request Flow Examples

### 1. Create Organization Flow

```
Client → POST /org/create
    │
    ├─► Route Handler validates input (Pydantic schema)
    │
    ├─► Service Layer:
    │   ├─► Check if organization_name exists in master DB
    │   ├─► Create new collection: org_<organization_name>
    │   ├─► Hash password using bcrypt
    │   ├─► Insert admin document into 'admins' collection
    │   ├─► Insert organization metadata into 'organizations' collection
    │   └─► Return success response with org details
    │
    └─► Response: Organization created with collection name and admin ID
```

### 2. Admin Login Flow

```
Client → POST /admin/login
    │
    ├─► Route Handler validates email and password
    │
    ├─► Service Layer:
    │   ├─► Find admin by email in 'admins' collection
    │   ├─► Verify password using bcrypt
    │   ├─► Find organization linked to this admin
    │   ├─► Generate JWT token containing:
    │   │   - admin_id
    │   │   - email
    │   │   - organization name
    │   │   - expiration time
    │   └─► Return JWT token
    │
    └─► Response: JWT access token for authenticated requests
```

### 3. Update Organization Flow (Protected Route)

```
Client → PUT /org/update (with JWT token in header)
    │
    ├─► Authentication Dependency:
    │   ├─► Extract Bearer token from Authorization header
    │   ├─► Decode JWT token
    │   ├─► Validate token signature and expiration
    │   └─► Extract admin_id from token payload
    │
    ├─► Route Handler validates new organization data
    │
    ├─► Service Layer:
    │   ├─► Find organization by admin_id (ensures admin owns the org)
    │   ├─► Validate new organization_name doesn't exist
    │   ├─► If organization name changed:
    │   │   ├─► Create new collection with new name
    │   │   ├─► Copy all documents from old collection to new
    │   │   └─► Drop old collection
    │   ├─► Hash new password
    │   ├─► Update admin email and password in 'admins' collection
    │   ├─► Update organization metadata in 'organizations' collection
    │   └─► Return success response
    │
    └─► Response: Updated organization details
```

### 4. Delete Organization Flow (Protected Route)

```
Client → DELETE /org/delete?organization_name=... (with JWT token)
    │
    ├─► Authentication Dependency validates JWT and extracts admin_id
    │
    ├─► Route Handler extracts organization_name from query params
    │
    ├─► Service Layer:
    │   ├─► Find organization by name in 'organizations' collection
    │   ├─► Verify admin_id matches (authorization check)
    │   ├─► Drop the organization's dynamic collection
    │   ├─► Delete admin document from 'admins' collection
    │   ├─► Delete organization metadata from 'organizations' collection
    │   └─► Return success message
    │
    └─► Response: Confirmation of deletion
```

### 5. Get Organization Flow

```
Client → GET /org/get?organization_name=...
    │
    ├─► Route Handler extracts organization_name from query params
    │
    ├─► Service Layer:
    │   ├─► Find organization by name in 'organizations' collection
    │   ├─► If not found, return 404 error
    │   └─► Format response (convert ObjectId to string)
    │
    └─► Response: Organization metadata from master database
```

## Multi-Tenant Data Isolation

```
Master Database (orgsphere_master)
    │
    ├─► organizations collection
    │   └─► Stores metadata for all organizations
    │       - Links to admin users
    │       - Contains collection names
    │
    ├─► admins collection
    │   └─► Stores all admin user credentials
    │
    └─► Dynamic Collections (one per organization)
        │
        ├─► org_testorg → Isolated data for "TestOrg"
        ├─► org_company1 → Isolated data for "Company1"
        ├─► org_company2 → Isolated data for "Company2"
        └─► ... (each organization has its own collection)
```

## Security Flow

```
Request with Authorization Header
    │
    ├─► Extract "Bearer <token>" from header
    │
    ├─► Decode JWT token using secret key
    │
    ├─► Validate:
    │   ├─► Token signature is valid
    │   ├─► Token hasn't expired
    │   └─► Token contains required fields (admin_id)
    │
    ├─► If valid:
    │   └─► Extract admin_id and pass to route handler
    │
    └─► If invalid:
        └─► Return 401 Unauthorized error
```

This diagram shows the complete flow from client request through all layers of the application to the database and back to the client response.
