## Todo Frontend

A Next.js frontend application for the Todo application with user authentication and task management.

## Features

- User authentication (login/signup)
- Task management (create, read, update, delete)
- JWT token handling for API authentication
- Responsive UI with Tailwind CSS
- Clean and modern interface

## Tech Stack

- Next.js 16+ with App Router
- TypeScript
- Tailwind CSS
- Axios for API calls

## Environment Variables

Create a `.env.local` file in the root of the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd phase-2/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. Create the environment file with your API URL:
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

## Running the Application

1. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

2. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── login/page.tsx      # Login page
│   ├── signup/page.tsx     # Signup page
│   ├── dashboard/page.tsx  # Dashboard with task list
│   └── page.tsx           # Home page (redirects to login/dashboard)
├── components/            # Reusable React components
│   ├── TaskList.tsx       # List of tasks
│   ├── TaskItem.tsx       # Individual task item
│   └── TaskForm.tsx       # Form for creating/updating tasks
├── lib/                   # Utility functions and services
│   ├── api.ts             # API client with JWT handling
│   └── auth.ts            # Authentication service
├── types/                 # TypeScript type definitions
│   └── task.ts            # Task type definitions
├── public/                # Static assets
└── package.json           # Dependencies and scripts
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8000` by default.
All API calls automatically include the JWT token in the Authorization header.

## Authentication Flow

1. Users register or login via the auth forms
2. JWT token is received from the backend and stored in localStorage
3. All subsequent API calls include the token in the Authorization header
4. On logout, the token is removed from localStorage

## Pages

- `/` - Redirects to login if not authenticated, otherwise to dashboard
- `/login` - User login page
- `/signup` - User registration page
- `/dashboard` - Task management dashboard

## Components

- `TaskList` - Displays all tasks in a list format
- `TaskItem` - Individual task with edit/delete options
- `TaskForm` - Form for creating and updating tasks
