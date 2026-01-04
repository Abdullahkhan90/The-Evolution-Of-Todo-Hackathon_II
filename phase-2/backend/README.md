# Todo API Backend

A FastAPI-based backend for the Todo application with user authentication and PostgreSQL database integration.

## Features

- User registration and authentication with JWT tokens
- Task management (create, read, update, delete)
- User-specific task isolation
- PostgreSQL database with SQLModel ORM
- Neon PostgreSQL ready configuration

## Requirements

- Python 3.8+
- PostgreSQL database (or Neon PostgreSQL)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the backend root directory with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

For Neon PostgreSQL, your DATABASE_URL would look like:
```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/todo_db?sslmode=require
```

## Running the Application

1. Make sure your PostgreSQL database is running
2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
3. The API will be available at `http://127.0.0.1:8000`
4. API documentation will be available at `http://127.0.0.1:8000/docs`

## API Endpoints

### Authentication
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login and get JWT token

### Tasks (requires authentication)
- `POST /api/{user_id}/` - Create a new task
- `GET /api/{user_id}/` - Get all tasks for a user
- `GET /api/{user_id}/{task_id}` - Get a specific task
- `PUT /api/{user_id}/{task_id}` - Update a specific task
- `DELETE /api/{user_id}/{task_id}` - Delete a specific task

### Other
- `GET /` - Welcome message
- `GET /health` - Health check

## Database Models

### User
- id: UUID (Primary Key)
- email: String (Unique, Indexed)
- password: String (Hashed)
- created_at: DateTime

### Task
- id: UUID (Primary Key)
- title: String
- description: String (Optional)
- completed: Boolean (Default: False)
- priority: String (Optional, high/medium/low)
- tags: String (Optional, comma-separated)
- due_date: DateTime (Optional)
- recurrence: String (Optional, daily/weekly/monthly)
- user_id: UUID (Foreign Key to User)
- created_at: DateTime
- updated_at: DateTime

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- Access control to ensure users can only access their own tasks
- Bearer token authentication required for task endpoints

## Development

To run tests:
```bash
pytest
```

To format code:
```bash
black .
```

To check code style:
```bash
flake8 .
```
