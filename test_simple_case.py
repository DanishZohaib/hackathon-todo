import requests
import json
import sys
import uuid

def test_simple_case():
    """
    Test a simple case to see if the basic functionality works
    """
    base_url = "http://localhost:8000"
    
    # Generate unique email for this test
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    
    print(f"Testing Simple Case with email: {test_email}")
    
    # Step 1: Health check
    try:
        health_response = requests.get(f"{base_url}/health")
        print(f"[OK] Health check: {health_response.status_code}, {health_response.json()}")
    except Exception as e:
        print(f"[ERROR] Health check failed: {e}")
        return False

    # Step 2: Register a test user (using /signup endpoint)
    print("\\nCreating a test user...")
    try:
        register_data = {
            "email": test_email,
            "password": "SecurePassword123!",
            "name": "Test User"
        }
        register_response = requests.post(f"{base_url}/auth/signup", json=register_data)
        print(f"Registration response: {register_response.status_code}")
        if register_response.status_code != 200:
            print(f"[ERROR] Registration failed: {register_response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Registration request failed: {e}")
        return False

    # Step 3: Login to get JWT token (using /signin endpoint)
    print("\\nLogging in to get JWT token...")
    try:
        login_data = {
            "email": test_email,
            "password": "SecurePassword123!"
        }
        login_response = requests.post(f"{base_url}/auth/signin", json=login_data)
        print(f"Login response status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            jwt_token = token_data.get("access_token")
            user_id = token_data["user"]["id"]  # Get the user ID from the response
            print(f"[OK] Got JWT token, user_id: {user_id}")
        else:
            print(f"[ERROR] Login failed: {login_response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Login request failed: {e}")
        return False

    # Step 4: Test simple case
    print(f"\\nTesting simple case for user {user_id}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }

    # Add a simple task
    print("\\nAdding a simple task...")
    chat_payload = {"message": "Add a task to buy groceries"}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Added: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to add task: {chat_response.text}")
    except Exception as e:
        print(f"  [ERROR] Failed to add task: {e}")

    # List tasks to see what we have
    print("\\nCurrent tasks:")
    chat_payload = {"message": "List all my tasks"}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Tasks: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to list tasks: {chat_response.text}")
    except Exception as e:
        print(f"  [ERROR] Failed to list tasks: {e}")

    # Try to complete the task by title
    print("\\nTrying to complete the task by title...")
    chat_payload = {"message": 'complete the task "buy groceries"'}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Completed: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to complete task: {chat_response.text}")
    except Exception as e:
        print(f"  [ERROR] Failed to complete task: {e}")

    # Final check of remaining tasks
    print("\\nFinal task list:")
    chat_payload = {"message": "List all my tasks"}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Remaining tasks: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to list tasks: {chat_response.text}")
    except Exception as e:
        print(f"  [ERROR] Failed to list tasks: {e}")

    print("\\n[OK] Simple case test completed!")
    return True

if __name__ == "__main__":
    success = test_simple_case()
    if success:
        print("\\n[SUCCESS] Simple case working properly!")
    else:
        print("\\n[ERROR] There are still issues with the simple case.")
        sys.exit(1)