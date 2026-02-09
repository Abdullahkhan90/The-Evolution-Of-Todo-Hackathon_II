#!/usr/bin/env python3
"""
Phase-3 Configuration Verification Script

This script checks if the Phase-3 application is properly configured
for deployment and identifies any issues.
"""

import os
import sys
import json
from pathlib import Path

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def check(condition, message):
    """Print check result"""
    status = f"{GREEN}✓{RESET}" if condition else f"{RED}✗{RESET}"
    print(f"  {status} {message}")
    return condition

def section(title):
    """Print section header"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{title}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def verify_phase3_setup():
    """Verify Phase-3 setup"""
    
    print(f"\n{BLUE}Phase-3 Deployment Configuration Checker{RESET}\n")
    
    # Check root directory
    section("Directory Structure")
    
    checks_passed = 0
    checks_total = 0
    
    # Check Phase-3 exists
    checks_total += 1
    if check(Path("phase-3").exists(), "phase-3 directory exists"):
        checks_passed += 1
    else:
        print(f"{RED}Error: Run this script from the root TODO directory{RESET}")
        return False
    
    # Check subdirectories
    for subdir in ["backend", "frontend"]:
        checks_total += 1
        if check(Path(f"phase-3/{subdir}").exists(), f"phase-3/{subdir} exists"):
            checks_passed += 1
    
    # Backend Checks
    section("Backend Configuration")
    
    # Check main.py
    checks_total += 1
    backend_main = Path("phase-3/backend/app/main.py")
    if check(backend_main.exists(), "backend/app/main.py exists"):
        checks_passed += 1
        # Check for proper CORS configuration
        with open(backend_main) as f:
            content = f.read()
            checks_total += 1
            if check("FRONTEND_URL" in content, "CORS configured with FRONTEND_URL"):
                checks_passed += 1
            else:
                print(f"    {YELLOW}Warning: FRONTEND_URL not used in main.py{RESET}")
    
    # Check requirements.txt
    checks_total += 1
    if check(Path("phase-3/backend/requirements.txt").exists(), "requirements.txt exists"):
        checks_passed += 1
        with open("phase-3/backend/requirements.txt") as f:
            reqs = f.read()
            checks_total += 2
            check("fastapi" in reqs, "FastAPI is in requirements")
            check("sqlmodel" in reqs, "SQLModel is in requirements")
    
    # Check environment template
    checks_total += 1
    if check(Path("phase-3/backend/.env.production").exists(), ".env.production template exists"):
        checks_passed += 1
    
    # Frontend Checks
    section("Frontend Configuration")
    
    # Check package.json
    checks_total += 1
    if check(Path("phase-3/frontend/package.json").exists(), "package.json exists"):
        checks_passed += 1
        with open("phase-3/frontend/package.json") as f:
            pkg = json.load(f)
            checks_total += 2
            check("next" in str(pkg.get("dependencies", {})), "Next.js is in dependencies")
            check("react" in str(pkg.get("dependencies", {})), "React is in dependencies")
    
    # Check next.config.js
    checks_total += 1
    next_config = Path("phase-3/frontend/next.config.js")
    if check(next_config.exists(), "next.config.js exists"):
        checks_passed += 1
        with open(next_config) as f:
            content = f.read()
            checks_total += 2
            if check("rewrites" in content, "API rewrites configured"):
                checks_passed += 1
            if check("NEXT_PUBLIC_BACKEND_URL" in content, "Backend URL configured"):
                checks_passed += 1
            # Check it doesn't have the old HF URL
            checks_total += 1
            if check("hafizabdullah9" not in content and "hf.space" not in content, 
                     "Old HuggingFace URL removed"):
                checks_passed += 1
    
    # Check .env files
    checks_total += 1
    if check(Path("phase-3/frontend/.env.production").exists(), ".env.production exists"):
        checks_passed += 1
    
    checks_total += 1
    if check(Path("phase-3/frontend/.env.local").exists(), ".env.local exists"):
        checks_passed += 1
    
    # API Configuration
    section("API Endpoints")
    
    # Check routers exist
    for router in ["auth", "tasks", "users", "todo", "chat"]:
        checks_total += 1
        if check(Path(f"phase-3/backend/app/routers/{router}.py").exists(), f"{router} router exists"):
            checks_passed += 1
    
    # Deployment Files
    section("Deployment Support Files")
    
    checks_total += 1
    if check(Path("phase-3/DEPLOYMENT_GUIDE.md").exists(), "DEPLOYMENT_GUIDE.md exists"):
        checks_passed += 1
    
    checks_total += 1
    if check(Path("phase-3/setup-local.bat").exists(), "setup-local.bat exists"):
        checks_passed += 1
    
    # Summary
    section("Summary")
    
    percentage = (checks_passed / checks_total) * 100
    status_color = GREEN if percentage == 100 else YELLOW if percentage >= 80 else RED
    
    print(f"\nConfiguration Status: {status_color}{checks_passed}/{checks_total} checks passed ({percentage:.0f}%){RESET}\n")
    
    if checks_passed == checks_total:
        print(f"{GREEN}✓ Phase-3 is properly configured and ready to deploy!{RESET}")
        print(f"\nNext steps:")
        print(f"1. Run setup-local.bat to set up local development environment")
        print(f"2. Follow DEPLOYMENT_GUIDE.md for production deployment")
        print(f"3. Set environment variables in Vercel dashboard with your actual URLs")
        return True
    else:
        print(f"{YELLOW}⚠ Some configuration issues found. Please review above.{RESET}")
        return False

if __name__ == "__main__":
    try:
        success = verify_phase3_setup()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)
