# Secure File Sharing API

A secure file sharing application built with FastAPI, featuring role-based access control and file encryption.

## Features

- 🔐 **User Authentication**: JWT-based authentication system
- 👥 **Role-Based Access Control**: Two user roles - Ops (Admin) and Client
- 🔒 **Secure File Storage**: Encrypted file storage system
- 📁 **File Management**: Upload, download, and manage files
- 📧 **Email Notifications**: For important account activities

## Tech Stack

- **Backend**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Bcrypt
- **File Storage**: Local file system with encryption

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/CodesavvySiddharth/Siddharth_2200290100162.git
   cd Siddharth_2200290100162
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python create_ops.py
   ```

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative API Docs**: `http://localhost:8000/redoc`

## Usage

### Authentication
1. Register a new user (if not already registered)
2. Login to get an access token
3. Use the token in the `Authorization` header for protected routes

### Available Endpoints

#### Ops User (Admin)
- `POST /ops/register` - Register a new ops user
- `POST /ops/login` - Login for ops users
- `GET /ops/files` - List all files (admin only)
- `DELETE /ops/files/{file_id}` - Delete a file (admin only)

#### Client User
- `POST /client/register` - Register a new client user
- `POST /client/login` - Login for client users
- `POST /client/upload` - Upload a file
- `GET /client/files` - List user's files
- `GET /client/files/{file_id}` - Download a file

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application setup
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic models
│   ├── auth.py           # Authentication utilities
│   ├── database.py       # Database connection
│   ├── encryption.py     # File encryption
│   └── email_utils.py    # Email notifications
├── routers/
│   ├── ops.py           # Ops user endpoints
│   └── client.py        # Client user endpoints
├── files/               # Uploaded files storage
├── requirements.txt     # Project dependencies
└── create_ops.py       # Script to create initial admin user
```

## Security Notes

- Always use HTTPS in production
- Store sensitive information in environment variables
- Regularly rotate encryption keys
- Keep dependencies updated

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Siddharth (CodesavvySiddharth)

---

*This project was developed as part of an academic/learning exercise.*
