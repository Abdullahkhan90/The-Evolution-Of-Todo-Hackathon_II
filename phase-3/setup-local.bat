@echo off
REM Quick setup script for Phase-3 local development

echo ========================================
echo Phase-3 Local Development Setup
echo ========================================

REM Check if we're in the right directory
if not exist "phase-3" (
    echo Error: Please run this script from the root TODO directory
    exit /b 1
)

echo.
echo [1/4] Setting up Backend...
cd phase-3\backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -r requirements.txt -q

echo Creating .env file...
if not exist ".env" (
    (
        echo DATABASE_URL=sqlite:///./db.sqlite
        echo SECRET_KEY=your-super-secret-key-change-in-production
        echo ALGORITHM=HS256
        echo ACCESS_TOKEN_EXPIRE_MINUTES=30
        echo OPENAI_API_KEY=sk-test-key
        echo ENVIRONMENT=development
        echo DEBUG=true
        echo RELOAD=true
        echo PORT=8000
        echo HOST=127.0.0.1
    ) > .env
    echo .env file created
) else (
    echo .env file already exists
)

cd ..

echo.
echo [2/4] Setting up Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install -q
)

echo Creating .env.local file...
if not exist ".env.local" (
    (
        echo NEXT_PUBLIC_API_URL=http://localhost:8000
        echo NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
    ) > .env.local
    echo .env.local file created
) else (
    echo .env.local file already exists
)

cd ..\..

echo.
echo [3/4] Verifying setup...
echo Checking Python...
python --version

echo Checking Node...
node --version
npm --version

echo.
echo [4/4] Setup Complete!
echo.
echo ========================================
echo To start development:
echo ========================================
echo.
echo Terminal 1 - Start Backend:
echo   cd phase-3\backend
echo   venv\Scripts\activate
echo   python main.py
echo.
echo Terminal 2 - Start Frontend:
echo   cd phase-3\frontend
echo   npm run dev
echo.
echo Then visit: http://localhost:3000
echo.
echo ========================================
