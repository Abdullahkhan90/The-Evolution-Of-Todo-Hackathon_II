# Phase-3 Deployment Guide

## Overview
Phase-3 consists of two separate applications that communicate via REST API:
- **Frontend**: Next.js 14 application (deployed on Vercel)
- **Backend**: FastAPI application (deployed on Vercel, Railway, Render, or similar)

## Complete Deployment Steps

### Step 1: Deploy Backend First

#### Option A: Deploy Backend on Vercel

1. **Prepare the backend**:
   ```bash
   cd phase-3/backend
   ```

2. **Create `vercel.json`** in the backend root:
   ```json
   {
     "buildCommand": "pip install -r requirements.txt",
     "outputDirectory": ".",
     "serverlessFunctionRegion": "iad1",
     "env": {
       "PYTHON_VERSION": "3.13"
     }
   }
   ```

3. **Deploy to Vercel**:
   ```bash
   vercel deploy --prod
   ```

4. **Note the backend URL**: It will look like `https://phase-3-backend-xx.vercel.app`

5. **Set environment variables in Vercel Dashboard**:
   - Go to Settings > Environment Variables
   - Add: `DATABASE_URL` (your Neon PostgreSQL connection string)
   - Add: `OPENAI_API_KEY` (your OpenAI API key)
   - Add: `SECRET_KEY` (generate a strong key)
   - Add: `FRONTEND_URL` (your frontend URL after deployment)
   - Add: `ENVIRONMENT=production`

#### Option B: Deploy Backend on Railway/Render
Use their web dashboards and set the same environment variables.

### Step 2: Get Backend URL
After backend deployment, you'll have a URL like:
- `https://phase-3-backend-xx.vercel.app`

### Step 3: Deploy Frontend

1. **Set frontend environment for production**:
   Create `.env.local` in `phase-3/frontend`:
   ```env
   NEXT_PUBLIC_BACKEND_URL=https://phase-3-backend-xx.vercel.app
   NEXT_PUBLIC_API_URL=https://phase-3-backend-xx.vercel.app
   ```

2. **Deploy to Vercel**:
   ```bash
   cd phase-3/frontend
   vercel deploy --prod
   ```

3. **Set environment variables in Vercel Dashboard for frontend**:
   - Go to Settings > Environment Variables
   - Add: `NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.vercel.app`
   - Add: `NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app`

### Step 4: Verify Deployment

### 4A: Test Backend Health
```bash
curl https://phase-3-backend-xx.vercel.app/health
# Expected response: {"status": "healthy"}
```

### 4B: Test Authentication
```bash
curl -X POST https://phase-3-backend-xx.vercel.app/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass","name":"Test User"}'
```

### 4C: Test Frontend Connection
- Visit your frontend URL
- Try to register or login
- Check browser console for any network errors

### 4D: Check Logs

**Backend Logs** (Vercel):
- Go to Vercel Dashboard > Project > Deployments > Recent > Logs

**Frontend Logs** (Vercel):
- Go to Vercel Dashboard > Project > Deployments > Recent > Logs

## Troubleshooting 404 and Network Errors

### Problem: 404 Errors on API Calls
**Causes**:
1. Backend URL is wrong in frontend `.env`
2. Backend is not deployed or crashed
3. Endpoint paths don't match

**Solution**:
1. Verify backend URL: `curl https://your-backend-url/health`
2. Check Vercel backend logs
3. Verify API endpoints match in `backend/app/main.py`

### Problem: CORS Errors
**Causes**:
1. Frontend URL not in `FRONTEND_URL` env variable
2. CORS middleware not configured correctly

**Solution**:
1. Add `FRONTEND_URL=https://your-frontend-url.vercel.app` to backend env vars
2. Restart backend deployment
3. Verify logs show correct CORS origins

### Problem: Network Errors/"Cannot reach backend"
**Causes**:
1. Backend is still starting up (cold start)
2. Database connection failed
3. Environment variables missing

**Solution**:
1. Wait 30 seconds and retry
2. Check backend logs for database errors
3. Verify all required env vars are set

## Environment Variables Checklist

### Backend (phase-3/backend)
- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `OPENAI_API_KEY` - OpenAI API key
- [ ] `SECRET_KEY` - Strong random key
- [ ] `FRONTEND_URL` - Your Vercel frontend URL
- [ ] `ENVIRONMENT=production`

### Frontend (phase-3/frontend)
- [ ] `NEXT_PUBLIC_BACKEND_URL` - Your backend URL
- [ ] `NEXT_PUBLIC_API_URL` - Same as backend URL

## Quick Reference URLs

After deployment, you'll have:
- **Frontend**: `https://your-frontend-project.vercel.app`
- **Backend**: `https://your-backend-project.vercel.app`

All API calls from frontend to backend happen through Next.js rewrites (no direct CORS needed).

## Notes
- First request to backend may be slow due to cold start (Vercel Serverless)
- Database connections persist in backend for 60 seconds
- JWT tokens expire after 30 minutes (configured in backend)

## Common Commands

Reset everything locally:
```bash
# Backend
cd phase-3/backend
rm -rf venv db.sqlite
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend
cd phase-3/frontend
rm -rf node_modules .next
npm install
```

Run locally before deployment:
```bash
# Terminal 1 - Backend
cd phase-3/backend
source venv/bin/activate
python main.py

# Terminal 2 - Frontend
cd phase-3/frontend
npm run dev
```

Then visit `http://localhost:3000`
