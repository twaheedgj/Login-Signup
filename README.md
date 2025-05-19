# FullStack Authentication API

A secure and robust authentication API built with FastAPI, SQLModel, and JWT.

## Features

- User registration and authentication
- JWT-based authentication
- Password hashing with bcrypt
- Email validation
- Strong password requirements
- User profile management
- Protected routes

## Tech Stack

- FastAPI
- SQLModel
- PostgreSQL
- JWT Authentication
- Pydantic
- Python 3.8+

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd FullStack
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
```

5. Run the application:
```bash
uvicorn Backend.main:app --reload
```

## API Endpoints

### Authentication
- `POST /auth/signup` - Register a new user
- `POST /auth/token` - Login and get access token
- `GET /auth/me` - Get current user info

### User Management
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}/profile` - Update user profile
- `PUT /users/{user_id}/password` - Update user password
- `DELETE /users/{user_id}` - Delete user

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- Email format validation
- Strong password requirements:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one number
  - At least one special character

## License

MIT 