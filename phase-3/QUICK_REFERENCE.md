# Phase-3 Deployment Quick Reference

## One-Page Deployment Checklist

### Before Deployment
- [ ] Backend `.env` values tested locally
- [ ] Frontend ran correctly with `npm run dev`
- [ ] Created `.env.production` with actual URLs
- [ ] Git repository initialized and committed

### Deploy Backend

```bash
cd phase-3/backend

# 1. Login to Vercel
vercel login

# 2. Deploy
vercel deploy --prod

# 3. Note the URL: https://your-backend-...vercel.app
# 4. Set environment variables in Vercel Dashboard:
#    - DATABASE_URL (from Neon)
#    - OPENAI_API_KEY (from OpenAI)
#    - SECRET_KEY (generate: python -c "import secrets; print(secrets.token_urlsafe(32))")
#    - FRONTEND_URL (your frontend URL from next step)

# 5. Verify health
curl https://your-backend-url.vercel.app/health
```

### Deploy Frontend

```bash
cd phase-3/frontend

# 1. Update .env.local
echo "NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.vercel.app" > .env.local
echo "NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app" >> .env.local

# 2. Deploy
vercel deploy --prod

# 3. Set environment variables in Vercel Dashboard:
#    - NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.vercel.app
#    - NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app

# 4. Verify
# Visit https://your-frontend-url.vercel.app and test login
```

### Troubleshoot

| Issue | Solution |
|-------|----------|
| Old project showing | Clear Vercel cache: Settings > Advanced > Clear Build Cache |
| 404 API errors | Check NEXT_PUBLIC_BACKEND_URL is correct |
| Network errors | Verify DATABASE_URL on backend env vars |
| Login not working | Check OPENAI_API_KEY is set |
| Chat not responding | Test OpenAI API key separately |

## Environment Variables

### Backend (7 variables)

```
DATABASE_URL=postgresql://user:pass@host/db
OPENAI_API_KEY=sk-...
SECRET_KEY=<generate using: python -c "import secrets; print(secrets.token_urlsafe(32))">
FRONTEND_URL=https://your-frontend.vercel.app
ENVIRONMENT=production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (2 variables)

```
NEXT_PUBLIC_BACKEND_URL=https://your-backend.vercel.app
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
```

## Getting Values

| Variable | Where to Get |
|----------|-------------|
| DATABASE_URL | Neon Console > Connection String (copy the full postgresql://... string) |
| OPENAI_API_KEY | OpenAI API Keys page (starts with sk-) |
| FRONTEND_URL | From your frontend Vercel deployment |
| BACKEND_URL | From your backend Vercel deployment |
| SECRET_KEY | Generate fresh: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |

## Live URLs After Deployment

- **Frontend**: `https://your-frontend-project.vercel.app`
- **Backend**: `https://your-backend-project.vercel.app`
- **Health Check**: `https://your-backend-project.vercel.app/health`

## Important Files

| File | Purpose |
|------|---------|
| `DEPLOYMENT_GUIDE.md` | Detailed step-by-step deployment |
| `TROUBLESHOOTING.md` | Fix common errors |
| `verify-setup.py` | Check configuration before deploy |
| `setup-local.bat` | Quick local development setup |

## Commands Reference

```bash
# Setup local development
phase-3\setup-local.bat

# Verify configuration is correct
python phase-3\verify-setup.py

# Deploy backend
cd phase-3\backend && vercel deploy --prod

# Deploy frontend
cd phase-3\frontend && vercel deploy --prod

# Clear Vercel cache and redeploy
vercel deploy --prod --force

# Test backend API
curl https://your-backend.vercel.app/health

# Check logs
# Backend: Vercel Dashboard > Backend Project > Deployments > Recent > Logs
# Frontend: Vercel Dashboard > Frontend Project > Deployments > Recent > Logs
```

## Success Indicators

✅ Backend deployment succeeds and shows green checkmark  
✅ Frontend deployment succeeds and shows green checkmark  
✅ Backend health check returns `{"status": "healthy"}`  
✅ Frontend loads and doesn't show 404 errors  
✅ Can register new account  
✅ Can login and see chat interface  
✅ Chat responds to messages  

If all these succeed, Phase-3 is fully deployed! 🎉
