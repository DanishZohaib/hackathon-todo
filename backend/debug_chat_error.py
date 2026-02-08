import requests
import json
import uuid

def debug_chat_error():
    """
    Debug script to reproduce and identify the specific error causing the 500 error
    """
    base_url = "http://localhost:8000"

    print("Testing chat endpoint to identify the 500 error...")

    # Test 1: Health check
    try:
        health_response = requests.get(f"{base_url}/health")
        print(f"Health check: {health_response.status_code}, {health_response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return

    # Test 2: Try to make a chat request with a proper user ID but invalid token
    # This will help us see if it's an auth issue or something else
    user_id = str(uuid.uuid4())  # Generate a random UUID
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer invalid-token"  # Invalid token to test auth error
    }

    chat_payload = {
        "message": "add a task"
    }

    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat",
                                     headers=headers, json=chat_payload)
        print(f"Chat response status: {chat_response.status_code}")
        print(f"Chat response: {chat_response.text}")

        if chat_response.status_code == 500:
            print("Got 500 Internal Server Error - this is the issue we need to fix")
        elif chat_response.status_code == 401:
            print("Expected 401 Unauthorized (invalid token)")
        elif chat_response.status_code == 403:
            print("Expected 403 Forbidden (mismatched user ID)")
        else:
            print(f"? Unexpected status: {chat_response.status_code}")
    except Exception as e:
        print(f"Chat request failed: {e}")

    # Test 3: Let's also check if the routes are accessible
    try:
        # Check if the chat route exists
        route_check = requests.get(f"{base_url}/docs")  # Swagger docs
        print(f"API Documentation accessible: {route_check.status_code}")
    except Exception as e:
        print(f"API Documentation not accessible: {e}")

    print("\nFor proper testing, you need a valid user account and JWT token.")
    print("The 500 error suggests an internal server error in the chat processing.")

if __name__ == "__main__":
    debug_chat_error()