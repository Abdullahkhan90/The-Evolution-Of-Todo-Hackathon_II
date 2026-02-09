# Phase-3 Troubleshooting Guide

## Common Issues and Solutions

### 1. Old Project Showing Up (404 Errors, Wrong App)

**Problem**: Visiting the frontend URL shows the old project or 404 errors

**Causes**:
- Frontend is still cached with old version
- Vercel is serving old deployment
- Wrong environment variables set

**Solutions**:

#### Option A: Clear Vercel Cache and Redeploy
```bash
# Push to GitHub (or your Git provider)
git add .
git commit -m "Fix: Updated Phase-3 deployment configuration"
git push

# Then redeploy from Vercel Dashboard:
# 1. Go to Project Settings > Advanced
# 2. Click "Clear Build Cache"
# 3. Redeploy from Deployments > Redeploy

# Or redeploy via CLI:
vercel --prod --skip-install
```

#### Option B: Force New Deployment
```bash
# In frontend directory
cd phase-3/frontend

# Ensure env vars are set correctly
echo NEXT_PUBLIC_BACKEND_URL=<your-actual-backend-url> >> .env.local

# Deploy fresh
vercel deploy --prod --force
```

---

### 2. 404 Errors on API Calls

**Problem**: Console shows 404 errors when clicking buttons or logging in

**Error Message**: 
```
GET https://your-frontend.vercel.app/api/... 404
```

**Causes**:
- Backend URL is wrong or incomplete
- Backend is not deployed/running
- Endpoint path mismatch
- Backend crashed due to database error

**Solutions**:

#### Step 1: Verify Backend is Running
```bash
# Test backend health
curl https://your-backend-url.vercel.app/health

# Expected response:
# {"status": "healthy"}

# If error, check Vercel backend logs
```

#### Step 2: Check Correct Backend URL
```bash
# Frontend .env.local should have:
NEXT_PUBLIC_BACKEND_URL=https://your-backend-project.vercel.app

# NOT: 
# - https://hafizabdullah9-phase-3-backend-todo-chatbot.hf.space (old HF URL)
# - http://localhost:8000 (only for local dev)
# - Incomplete URL like just "backend.vercel.app"
```

#### Step 3: Redeploy Frontend with Correct Variables
```bash
cd phase-3/frontend

# Update .env.local
NEXT_PUBLIC_BACKEND_URL=https://your-actual-backend-url.vercel.app
NEXT_PUBLIC_API_URL=https://your-actual-backend-url.vercel.app

# Redeploy
vercel deploy --prod
```

---

### 3. Network Errors / "Cannot Connect to Server"

**Problem**: App shows network error, API calls timeout or fail

**Error Message**:
```
Network error while fetching
Failed to fetch from backend
CORS error
```

**Causes**:
- Backend is down or loading (cold start)
- CORS not properly configured
- Frontend URL not whitelisted on backend
- Database connection failed

**Solutions**:

#### Step 1: Wait for Cold Start
Cold starts on Vercel can take 10-30 seconds
```bash
# Wait and retry
# Or check status page
curl https://your-backend-url.vercel.app/health
```

#### Step 2: Check Backend Logs
In Vercel Dashboard:
1. Go to your backend project
2. Click "Deployments"
3. Click most recent deployment
4. Click "Logs"

**Look for**:
- Database connection errors
- Missing environment variables
- Missing OPENAI_API_KEY

#### Step 3: Fix Environment Variables

Backend needs:
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - Your OpenAI API key
- `FRONTEND_URL` - Your frontend URL for CORS
- `SECRET_KEY` - Random string for JWT

```bash
# In Vercel Dashboard > Backend Project > Settings > Environment Variables:

1. DATABASE_URL=postgresql://... (from Neon)
2. OPENAI_API_KEY=sk-... (from OpenAI)
3. FRONTEND_URL=https://your-frontend.vercel.app
4. SECRET_KEY=your-super-secret-key-at-least-32-chars
5. ENVIRONMENT=production
```

#### Step 4: Redeploy Backend
```bash
cd phase-3/backend
vercel deploy --prod --force
```

---

### 4. Login/Register Not Working

**Problem**: Cannot create account or login

**Causes**:
- Backend not receiving requests (see issue #2 and #3)
- Database not connected
- Password validation failing (too weak)
- User already exists

**Solutions**:

#### Check Backend Logs
```bash
curl -X POST https://your-backend-url.vercel.app/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#","name":"Test"}'
```

Look at response - it will indicate the actual error.

#### Verify Password Requirements
Password should have:
- At least 8 characters
- Mix of uppercase and lowercase
- At least one number
- At least one special character (!@#$%^&*)

#### Check Database Connection
```bash
# In backend logs, look for:
# "failed to connect to database"
# "connection refused"

# If DATABASE_URL is wrong, it will fail on startup
```

---

### 5. Chat Not Responding / No AI Answers

**Problem**: Chat interface doesn't respond, or AI doesn't answer questions

**Causes**:
- OPENAI_API_KEY is invalid
- OpenAI API quota exceeded
- MCP tools not loading

**Solutions**:

#### Verify OpenAI API Key
```bash
# Test OpenAI API key:
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-..." \
  -H "Content-Type: application/json"

# Should return list of models
```

#### Check OpenAI Billing
- Visit https://platform.openai.com/account/billing/overview
- Ensure you have credits or valid payment method

#### Check Backend Logs for MCP Errors
In Vercel > Backend > Deployments > Logs:
```
Look for:
- "MCP server started"
- "Failed to initialize tools"
- "OpenAI error"
```

---

### 6. "Too Many Requests" or Rate Limit Errors

**Problem**: Getting 429 Too Many Requests error

**Causes**:
- OpenAI API rate limit exceeded
- Backend overloaded
- Multiple requests sent simultaneously

**Solutions**:
- Wait 30-60 seconds before retrying
- Upgrade OpenAI API plan at https://platform.openai.com/account/billing/overview
- Use exponential backoff in retry logic

---

### 7. Database Connection Errors

**Problem**: Backend logs show "could not connect to database"

**Solutions**:

#### Check DATABASE_URL Format
```
# Correct format:
postgresql://user:password@host:5432/dbname

# If using Neon:
postgresql://user:password@host.neon.tech:5432/dbname?sslmode=require
```

#### Verify Neon Database
1. Visit https://console.neon.tech
2. Check database status (should be "Active")
3. Copy connection string (includes password)
4. Paste in Vercel environment variables
5. Test connection:
```bash
# Using psql (if installed)
psql "postgresql://user:password@host:5432/dbname"
```

#### IP Whitelisting
If using Neon with IP restrictions:
1. Go to Project Settings > Network > IP Whitelist
2. Add `0.0.0.0/0` (allows all - less secure) OR
3. Add Vercel IP ranges (see Vercel docs)

---

### 8. Vercel Deployment Keeps Failing

**Problem**: Vercel shows red "Failed" status on deployment

**Causes**:
- Missing required environment variables
- Python version too old
- Dependency installation fails

**Solutions**:

#### Check Vercel Build Logs
1. Go to Deployments > Recent Failed Build
2. Scroll down to see full error message

#### For Backend Python Issues
Create `vercel.json` in backend root:
```json
{
  "builds": [
    { "src": "main.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "main.py" }
  ],
  "env": {
    "PYTHON_VERSION": "3.11"
  }
}
```

#### For Frontend Build Issues
Ensure `package.json` has build script:
```json
{
  "scripts": {
    "build": "next build",
    "start": "next start"
  }
}
```

---

## Debugging Commands

### Test Frontend Connection
```bash
# Check if frontend can reach backend
curl -X GET https://your-backend-url.vercel.app/health
```

### Test API Endpoints
```bash
# Register
curl -X POST https://your-backend-url.vercel.app/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#","name":"Test"}'

# Login
curl -X POST https://your-backend-url.vercel.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#"}'
```

### Browser Console Debugging
Press `F12` in browser, then:
```javascript
// Check environment
console.log(process.env.NEXT_PUBLIC_BACKEND_URL)

// Check stored token
localStorage.getItem('token')

// Check API calls (in Network tab)
// Look for 404s, 500s, CORS errors
```

---

## Still Having Issues?

Check these files for configuration:
1. `phase-3/frontend/.env.local` - Frontend config
2. `phase-3/frontend/.env.production` - Production config hint
3. `phase-3/backend/.env.production` - Backend config template
4. `phase-3/frontend/next.config.js` - API rewrites (must have your backend URL)
5. `phase-3/backend/app/main.py` - CORS configuration

Run verification script:
```bash
python phase-3/verify-setup.py
```

Check deployment guide:
```bash
Open phase-3/DEPLOYMENT_GUIDE.md
```
