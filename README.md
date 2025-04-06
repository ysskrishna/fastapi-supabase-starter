# FastAPI Supabase Starter

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.1-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.30-blue.svg)](https://www.sqlalchemy.org/)
[![Supabase](https://img.shields.io/badge/Supabase-Platform-orange.svg)](https://supabase.com/)
[![python-jose](https://img.shields.io/badge/python--jose-3.5.0-yellow.svg)](https://python-jose.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A starter template for building secure and scalable FastAPI applications with Supabase authentication integration. This template provides a solid foundation for modern web applications, combining the power of FastAPI's high-performance framework with Supabase's robust authentication system.

## Use Cases

This starter template is perfect for:
- Building secure backend APIs
- Creating user authentication systems
- Developing full-stack applications
- Learning FastAPI and Supabase integration
- Prototyping new projects quickly

## Features

- FastAPI backend with SQLAlchemy ORM
- Secure Supabase JWT authentication integration
  - Automatic token validation and parsing
  - Protected route handling
- User management endpoints
- CORS middleware enabled
- SQLite database (can be easily switched to other databases)
- Swagger UI for API documentation

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Supabase account and project

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-supabase-starter
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
Create a `.env` file in the project root with the following variables:
```env
SUPABASE_PROJECT_ID=your_project_id
SUPABASE_JWT_SECRET=your_jwt_secret
DATABASE_URL=your_database_url
```

## Supabase Setup

1. Create a Supabase project at https://supabase.com
2. Get your project credentials:
   - Project ID: Found in Project Settings > General
   - JWT Secret: Found in Project Settings > API > JWT Settings
3. Add these credentials to your `.env` file

## JWT Authentication

This project uses Supabase's JWT authentication with the following features:

- HS256 symmetric encryption
- Automatic JWT validation and parsing
- User session management
- Protected route handling

### Getting a JWT Token

1. Using Supabase Client:
```javascript
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password'
})
// JWT token will be in data.session.access_token
```

2. Using REST API:
```bash
curl -X POST 'https://[YOUR_PROJECT_ID].supabase.co/auth/v1/token?grant_type=password' \
-H "apikey: [YOUR_ANON_KEY]" \
-H "Content-Type: application/json" \
-d '{"email":"user@example.com","password":"password"}'
```

### Using JWT in API Requests

Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Project Structure

```
fastapi-supabase-starter/
├── core/               # Core utilities and configurations
│   ├── config.py      # Environment configuration
│   ├── dbutils.py     # Database utilities
│   └── jwtutils.py    # JWT authentication utilities
├── models/            # SQLAlchemy models
├── routers/           # API route handlers
├── main.py           # Application entry point
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## API Endpoints

### User Management

- `POST /user/create` - Create user in database, using supabase jwt payload (requires Supabase JWT)
- `GET /user/me` - Retrieves user details from database (requires Supabase JWT)

## Running the Application

Start the development server:

```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Documentation

Swagger UI documentation is available at: `http://localhost:8000/docs`

## Security Best Practices

- Never expose your JWT_SECRET in client-side code
- Keep your JWT_SECRET secure and rotate it periodically
- Use HTTPS for all API requests
- Set appropriate token expiration times
- Validate all claims in the JWT payload

## References

### Supabase Documentation
- [Supabase Authentication Overview](https://supabase.com/docs/guides/auth)
- [JWT Authentication Guide](https://supabase.com/docs/guides/auth/jwt)
- [Security Best Practices](https://supabase.com/docs/guides/auth/managing-user-data)
- [API Reference](https://supabase.com/docs/reference/api/introduction)

### JWT Resources
- [JWT.io](https://jwt.io/) - Learn about JSON Web Tokens
- [JWT Best Practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.