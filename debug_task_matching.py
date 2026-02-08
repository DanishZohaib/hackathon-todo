import requests
import json
import sys
import uuid

def debug_task_matching():
    """
    Debug the task matching to see what's happening
    """
    base_url = "http://localhost:8000"
    
    # Generate unique email for this test
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    
    print(f"Debugging Task Matching with email: {test_email}")
    
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

    # Step 4: Debug the exact issue
    print(f"\\nDebugging the exact issue for user {user_id}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }

    # Add the exact task from the original issue
    print("\\nAdding task: 'Add a task called Phase 3: AI chatbot integration (current focus)'")
    chat_payload = {"message": "Add a task called Phase 3: AI chatbot integration (current focus)"}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Added: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to add: {chat_response.text}")
            return False
    except Exception as e:
        print(f"  [ERROR] Failed to add: {e}")
        return False

    # List tasks to see the exact title stored
    print("\\nListing tasks to see exact stored title:")
    chat_payload = {"message": "List all my tasks"}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Tasks: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to list: {chat_response.text}")
            return False
    except Exception as e:
        print(f"  [ERROR] Failed to list: {e}")
        return False

    # Now try to complete using the EXACT stored title
    print("\\nTrying to complete using the exact stored title...")
    chat_payload = {"message": 'complete the task "Phase 3 AI chatbot integration (current focus)"'}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Successfully completed with exact title: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to complete with exact title: {chat_response.text}")
    except Exception as e:
        print(f"  [ERROR] Exception completing with exact title: {e}")

    # Now try to complete using the ORIGINAL title with colon (this was causing the error)
    print("\\nTrying to complete using original title with colon (the problematic case)...")
    chat_payload = {"message": 'complete the task "Phase 3: AI chatbot integration (current focus)"'}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Successfully completed with colon: {response_data['response']}")
        else:
            print(f"  [RESULT] Failed with colon (this was the original issue): {chat_response.text}")
    except Exception as e:
        print(f"  [RESULT] Exception with colon (this was the original issue): {e}")

    print("\\n[OK] Debug test completed!")
    return True

if __name__ == "__main__":
    success = debug_task_matching()
    if success:
        print("\\n[SUCCESS] Debug completed!")
    else:
        print("\\n[ERROR] Debug failed.")
        sys.exit(1)