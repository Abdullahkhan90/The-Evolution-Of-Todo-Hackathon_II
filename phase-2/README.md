# Phase II: Full-Stack Todo Application

This phase implements a complete full-stack todo application with a Next.js frontend and FastAPI backend.

## Overview

Phase II consists of two main components:
1. **Backend**: FastAPI + SQLModel + PostgreSQL with JWT authentication
2. **Frontend**: Next.js 16+ App Router with TypeScript and Tailwind CSS

## Backend Features

- User registration and authentication with JWT tokens
- Task management (create, read, update, delete)
- PostgreSQL database with SQLModel ORM
- Neon PostgreSQL ready configuration
- Secure password hashing
- User-specific task isolation

## Frontend Features

- User authentication (login/signup)
- Task management dashboard
- Responsive UI with Tailwind CSS
- JWT token handling for API authentication
- Clean and modern interface

## Tech Stack

### Backend
- FastAPI
- SQLModel
- PostgreSQL/Neon
- JWT Authentication
- Python 3.8+

### Frontend
- Next.js 16+ with App Router
- TypeScript
- Tailwind CSS
- Axios for API calls

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory: `cd phase-2/backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with the required environment variables
6. Run the application: `uvicorn app.main:app --reload`

### Frontend Setup
1. Navigate to the frontend directory: `cd phase-2/frontend`
2. Install dependencies: `npm install`
3. Create a `.env.local` file with your API URL
4. Run the development server: `npm run dev`

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Endpoints (Backend)

### Authentication
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Authenticate user and get JWT token

### Task Management (requires authentication)
- `POST /api/{user_id}/` - Create a new task
- `GET /api/{user_id}/` - Get all tasks for a user
- `GET /api/{user_id}/{task_id}` - Get a specific task
- `PUT /api/{user_id}/{task_id}` - Update a specific task
- `DELETE /api/{user_id}/{task_id}` - Delete a specific task

## Frontend Pages

- `/` - Home (redirects to login/dashboard)
- `/login` - User login page
- `/signup` - User registration page
- `/dashboard` - Task management dashboard

## Project Structure

```
phase-2/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py       # Main application
│   │   ├── core/         # Authentication utilities
│   │   ├── database/     # Database setup
│   │   ├── models/       # SQLModel models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── routers/      # API routes
│   ├── requirements.txt
│   ├── .env
│   ├── README.md
│   └── test_api.py
└── frontend/             # Next.js frontend
    ├── app/
    │   ├── login/page.tsx
    │   ├── signup/page.tsx
    │   ├── dashboard/page.tsx
    │   └── page.tsx
    ├── components/       # React components
    ├── lib/             # Utilities and services
    ├── types/           # TypeScript definitions
    ├── public/
    ├── package.json
    ├── next.config.js
    ├── .env.local
    └── README.md
```