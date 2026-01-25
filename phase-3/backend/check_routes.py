from app.main import app

print("Checking registered routes...")
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        if 'chat' in route.path.lower():
            print(f"Found chat route: {route.methods} {route.path}")
        elif 'conversation' in route.path.lower():
            print(f"Found conversation route: {route.methods} {route.path}")
        elif 'tasks' in route.path.lower():
            print(f"Found tasks route: {route.methods} {route.path}")
    elif hasattr(route, 'path'):
        if 'chat' in route.path.lower() or 'conversation' in route.path.lower() or 'tasks' in route.path.lower():
            print(f"Found route: {route.path}")

print("\nAll routes:")
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        print(f"{route.methods} {route.path}")
    elif hasattr(route, 'path'):
        print(f"GET {route.path}")