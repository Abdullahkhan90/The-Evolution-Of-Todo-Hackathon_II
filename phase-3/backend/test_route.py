from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Check if the route exists
response = client.get('/api/chat/conversation')
print('GET /api/chat/conversation status:', response.status_code)

response = client.post('/api/chat/conversation', json={'user_id': 'test', 'message': 'hello'})
print('POST /api/chat/conversation status:', response.status_code)
print('Response text:', response.text)