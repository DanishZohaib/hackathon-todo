import requests
import json

# Test script to debug the chatbot issue
def test_chat_api():
    # Assuming you have a valid user ID and JWT token
    # This is a basic test - you'll need to replace with actual values
    user_id = "test-user-id"  # Replace with actual user ID
    token = "your-jwt-token"  # Replace with actual JWT token

    url = f"http://localhost:8000/api/{user_id}/chat"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "message": "add a task"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_chat_api()