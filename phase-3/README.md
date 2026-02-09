# Phase III: Todo AI Chatbot

This phase implements an AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture.

##    Features

### AI Chatbot
- Natural language processing for task management
- Integration with OpenAI API for intelligent responses
- MCP tools for task operations (add, list, complete, delete, update)
- State management with conversation history stored in database

### Backend Features
- FastAPI backend with proper authentication
- SQLModel ORM with PostgreSQL database
- MCP server exposing task operations as tools
- Stateless chat endpoint with conversation persistence
- User isolation for data security

### Frontend Features
- Chat interface with real-time messaging
- Conversation history display
- Natural language command support
- Integration with backend API

## Tech Stack

### Backend
- Python 3.13+
- FastAPI
- SQLModel
- PostgreSQL/Neon
- OpenAI API
- MCP Protocol
- JWT Authentication

### Frontend
- Next.js 14+ with App Router
- TypeScript
- Tailwind CSS
- OpenAI API client

- Deployed on Vercel - fixed env var cache

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory: `cd phase-3/backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with the required environment variables
6. Run the application: `uvicorn app.main:app --reload`

### Frontend Setup
1. Navigate to the frontend directory: `cd phase-3/frontend`
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
OPENAI_API_KEY=your-openai-api-key
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

### Chat Endpoint
- `POST /api/chat/conversation` - Send message to AI assistant

## Natural Language Commands

The AI assistant understands these commands:

| User Says | Agent Action |
|----------|--------------|
| "Add a task to buy groceries" | Call add_task with title "Buy groceries" |
| "Show me all my tasks" | Call list_tasks with status "all" |
| "What's pending?" | Call list_tasks with status "pending" |
| "Mark task 3 as complete" | Call complete_task with task_id 3 |
| "Delete the meeting task" | Call list_tasks first, then delete_task |
| "Change task 1 to 'Call mom tonight'" | Call update_task with new title |
| "I need to remember to pay bills" | Call add_task with title "Pay bills" |
| "What have I completed?" | Call list_tasks with status "completed" |

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

### Conversation
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to User)
- created_at: DateTime
- updated_at: DateTime

### Message
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to User)
- conversation_id: UUID (Foreign Key to Conversation)
- role: String (user/assistant)
- content: String
- created_at: DateTime

## Architecture

The application follows a stateless architecture where conversation history is persisted to the database, allowing the server to handle requests without maintaining in-memory state.

```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              FastAPI Server                   │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │    Neon DB      │
│  Chat Interface │────▶│  │         Chat Endpoint                  │  │     │  (PostgreSQL)   │
│  (Frontend)     │     │  │  POST /api/chat                        │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │  - tasks        │
│                 │     │                  │                           │     │  - conversations│
│                 │     │                  ▼                           │     │  - messages     │
│                 │     │  ┌────────────────────────────────────────┐  │     │                 │
│                 │◀────│  │      OpenAI API Integration          │  │     │                 │
│                 │     │  │      (Natural Language Processing)   │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  ▼                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │────▶│                 │
│                 │     │  │         MCP Tools Server               │  │     │                 │
│                 │     │  │  (Task Operations)                     │  │◀────│                 │
│                 │     │  └────────────────────────────────────────┘  │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

## MCP Tools Specification

The server exposes these MCP tools for the AI agent:

### add_task
- Purpose: Create a new task
- Parameters: user_id (string, required), title (string, required), description (string, optional)
- Returns: task_id, status, title

### list_tasks
- Purpose: Retrieve tasks from the list
- Parameters: user_id (string, required), status (string, optional: "all", "pending", "completed")
- Returns: Array of task objects

### complete_task
- Purpose: Mark a task as complete
- Parameters: user_id (string, required), task_id (string, required)
- Returns: task_id, status, title

### delete_task
- Purpose: Remove a task from the list
- Parameters: user_id (string, required), task_id (string, required)
- Returns: task_id, status, title

### update_task
- Purpose: Modify task title or description
- Parameters: user_id (string, required), task_id (string, required), title (string, optional), description (string, optional)
- Returns: task_id, status, title

## Development

To run tests:
```bash
cd phase-3/backend
python -m pytest
```

To format code:
```bash
black .
```

To check code style:
```bash
flake8 .
```

## Deployment

### Quick Start - Production Deployment

See `DEPLOYMENT_GUIDE.md` for step-by-step instructions on deploying to production.

**TL;DR - Deploy in 5 minutes:**

1. **Backend**:
   - Deploy to Vercel/Railway with your `DATABASE_URL` and `OPENAI_API_KEY`
   - Note the backend URL

2. **Frontend**:
   - Add env vars: `NEXT_PUBLIC_BACKEND_URL=<your-backend-url>`
   - Deploy to Vercel

3. **Verify**: Visit your frontend URL and test login/chat

### Local Development

Quick setup script available:
```bash
# Windows
phase-3\setup-local.bat

# Then in two terminals:

# Terminal 1 - Backend
cd phase-3\backend
venv\Scripts\activate
python main.py

# Terminal 2 - Frontend
cd phase-3\frontend
npm run dev
```

Visit `http://localhost:3000`

### Verification
Run the configuration checker:
```bash
python phase-3/verify-setup.py
```
