import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("Starting server setup...")

try:
    from app.main import app
    print("App imported successfully!")
    
    # Print routes to verify auth endpoints are there
    print("\nAll routes:")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            print(f"  {route.methods} {route.path}")
    
    print("\nChecking for auth routes...")
    auth_found = False
    for route in app.routes:
        if hasattr(route, 'path') and '/auth' in route.path.lower():
            print(f"  Found auth route: {route.methods} {route.path}")
            auth_found = True
    
    if not auth_found:
        print("  No auth routes found!")
    else:
        print(f"  Auth routes are properly registered!")
        
    # Now start the server
    import uvicorn
    print("\nStarting server on port 8006...")
    uvicorn.run(app, host='127.0.0.1', port=8006, log_level='info')
    
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")  # Keep window open to see error