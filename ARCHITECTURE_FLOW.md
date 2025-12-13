Create a system architecture diagram in a clean, hand-drawn style with colored shapes and numbered arrows showing the interconnected components of a FastAPI backend application. The diagram should have two parts:

**PART 1 - General System Interaction:**

Show four main components arranged horizontally from left to right:

1. **Client/Frontend** - Represent as a green-outlined rectangle on the far left, labeled "CLIENT/FRONTEND"

2. **FastAPI Application** - Represent as a tall, narrow, orange-outlined vertical rectangle in the center, with "FASTAPI APP" written vertically

3. **Service Layer** - Represent as a red-outlined rectangle to the right of FastAPI, labeled "SERVICE LAYER"

4. **MongoDB Database** - Represent as a purple-filled cylinder on the far right, labeled "MONGODB"

**Request Flow (Red Arrows, left to right):**
- Arrow "1" (solid red): From CLIENT/FRONTEND to FASTAPI APP, labeled "HTTP Request"
- Arrow "2" (solid red): From FASTAPI APP to SERVICE LAYER, labeled "Process Request"
- Arrow "2'" (dashed red): From SERVICE LAYER to MONGODB, labeled "Database Query"

**Response Flow (Green Arrows, right to left):**
- Arrow "2''" (dashed green): From MONGODB back to SERVICE LAYER, labeled "Return Data"
- Arrow "3" (solid green): From SERVICE LAYER back to FASTAPI APP, labeled "Return Result"
- Arrow "4" (solid green): From FASTAPI APP back to CLIENT/FRONTEND, labeled "JSON Response"

**PART 2 - Specific Use Case: Create Organization Flow**

Below the first diagram, create an identical layout with the same four components, but with specific action labels on the arrows:

**Request Flow (Red Arrows):**
- Arrow "1": CLIENT/FRONTEND → FASTAPI APP, labeled "POST /org/create {name, email, password}"
- Arrow "2": FASTAPI APP → SERVICE LAYER, labeled "create_organization()"
- Arrow "2'": SERVICE LAYER → MONGODB, labeled "Check if org exists, create collection, insert admin & org data"

**Response Flow (Green Arrows):**
- Arrow "2''": MONGODB → SERVICE LAYER, labeled "Return success confirmation"
- Arrow "3": SERVICE LAYER → FASTAPI APP, labeled "Return org metadata"
- Arrow "4": FASTAPI APP → CLIENT/FRONTEND, labeled "201 Created {organization details}"

**Visual Style Requirements:**
- Clean, minimalist, hand-drawn aesthetic
- Use solid lines for application layer communication
- Use dashed lines for database interactions
- Number all arrows clearly (1, 2, 2', 2'', 3, 4)
- Color code: Green for Frontend, Orange for FastAPI, Red for Service Layer, Purple for Database
- Red arrows for requests, Green arrows for responses
- Add a title above Part 2: "Create Organization Flow - OrgSphere Backend"

Make sure the diagram clearly shows the bidirectional communication flow and the separation between application layers and database interactions.


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
