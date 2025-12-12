# OrgSphere Backend

A multi-tenant organization management backend service built with FastAPI and MongoDB.

## Features

- **Multi-tenant Architecture**: Each organization has its own isolated MongoDB collection
- **Organization Management**: Create, read, update, and delete organizations
- **Admin Authentication**: JWT-based authentication for admin users
- **Dynamic Collection Creation**: Automatically creates collections for new organizations
- **Secure Password Hashing**: Uses bcrypt for password security

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Python Version**: 3.8+

## Project Structure

```
OrgSphere Backend/
├── app/
│   ├── config/          # Configuration settings
│   ├── database/        # MongoDB connection
│   ├── dependencies/    # FastAPI dependencies (auth)
│   ├── routes/          # API route handlers
│   ├── schemas/         # Pydantic models
│   ├── services/        # Business logic
│   └── utils/           # Utility functions (hashing, JWT)
├── venv/                # Virtual environment
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Prerequisites

- Python 3.8 or higher
- MongoDB (running locally or remote)
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "OrgSphere Backend"
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   MONGO_URI=mongodb://localhost:27017
   MASTER_DB_NAME=orgsphere_master
   JWT_SECRET_KEY=your_secret_key_here_change_in_production
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

5. **Start MongoDB**
   
   Make sure MongoDB is running on your system:
   ```bash
   # On macOS with Homebrew
   brew services start mongodb-community
   
   # Or run MongoDB manually
   mongod
   ```

## Running the Application

1. **Activate the virtual environment** (if not already activated)
   ```bash
   source venv/bin/activate
   ```

2. **Start the FastAPI server**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   The `--reload` flag enables auto-reload on code changes (useful for development).

3. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive API Docs: `http://localhost:8000/docs`
   - Alternative API Docs: `http://localhost:8000/redoc`

## API Endpoints

### Organization Endpoints

#### 1. Create Organization
- **POST** `/org/create`
- **Body**:
  ```json
  {
    "organization_name": "MyOrg",
    "email": "admin@myorg.com",
    "password": "securepassword123"
  }
  ```
- **Response**: Organization metadata with collection name and admin ID

#### 2. Get Organization
- **GET** `/org/get?organization_name=MyOrg`
- **Response**: Organization details from master database

#### 3. Update Organization
- **PUT** `/org/update`
- **Headers**: `Authorization: Bearer <token>`
- **Body**:
  ```json
  {
    "organization_name": "UpdatedOrgName",
    "email": "newadmin@myorg.com",
    "password": "newpassword123"
  }
  ```
- **Note**: Only the admin who owns the organization can update it. If organization name changes, the collection is migrated automatically.

#### 4. Delete Organization
- **DELETE** `/org/delete?organization_name=MyOrg`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Success message
- **Note**: Only the admin who owns the organization can delete it. This also deletes the organization's collection and admin user.

### Admin Endpoints

#### 5. Admin Login
- **POST** `/admin/login`
- **Body**:
  ```json
  {
    "email": "admin@myorg.com",
    "password": "securepassword123"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
- **JWT Token Contains**: Admin ID, email, and organization identifier

## Testing

A test script is provided to verify all endpoints:

```bash
python3 test_api.py
```

Make sure the server is running before executing the test script.

## Database Structure

### Master Database (`orgsphere_master`)

#### Collections:

1. **organizations**
   - `organization_name` (string, unique)
   - `display_name` (string)
   - `collection_name` (string) - The dynamic collection for this org
   - `admin_id` (ObjectId) - Reference to admin user
   - `created_at` (datetime)
   - `updated_at` (datetime, optional)

2. **admins**
   - `email` (string, unique)
   - `password` (string, hashed with bcrypt)
   - `role` (string) - Always "admin"
   - `created_at` (datetime)

3. **org_<organization_name>** (Dynamic collections)
   - Created automatically for each organization
   - Can store organization-specific data

## Security Features

- **Password Hashing**: All passwords are hashed using bcrypt before storage
- **JWT Authentication**: Secure token-based authentication
- **Authorization**: Admins can only modify/delete their own organizations
- **Input Validation**: Pydantic models validate all input data

## Development Notes

- The project follows a clean, modular structure with separation of concerns
- Services contain business logic, routes handle HTTP requests/responses
- Dependencies are used for authentication and database connections
- Error handling is implemented with appropriate HTTP status codes

## License

This project is created for assignment purposes.
