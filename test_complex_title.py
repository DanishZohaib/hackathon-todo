import requests
import json
import sys
import uuid

def test_complex_task_title():
    """
    Test specifically for the complex task title issue
    """
    base_url = "http://localhost:8000"
    
    # Generate unique email for this test
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    
    print(f"Testing Complex Task Title with email: {test_email}")
    
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

    # Step 4: Test complex task title
    print(f"\\nTesting complex task title for user {user_id}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }

    # Add the exact complex task that was causing the issue
    print("\\nAdding complex task: 'Phase 3: AI chatbot integration (current focus)'")
    # Try different ways to add this task
    chat_payload = {"message": 'Add a task called "Phase 3: AI chatbot integration (current focus)"'}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Added complex task: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to add complex task: {chat_response.text}")
            # Try alternative approach
            chat_payload = {"message": "Add a task called Phase 3: AI chatbot integration (current focus)"}
            chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                        headers=headers, json=chat_payload)
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"  [OK] Added complex task (alternative): {response_data['response']}")
            else:
                print(f"  [ERROR] Failed to add complex task (alternative): {chat_response.text}")
                return False
    except Exception as e:
        print(f"  [ERROR] Failed to add complex task: {e}")
        return False

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
            return False
    except Exception as e:
        print(f"  [ERROR] Failed to list tasks: {e}")
        return False

    # Now try to complete the complex task (this was causing the UUID error)
    print("\\nTrying to complete the complex task (testing UUID error fix)...")
    # Try different ways to reference the task
    completion_attempts = [
        'complete the task "Phase 3: AI chatbot integration (current focus)"',
        'complete the task Phase 3: AI chatbot integration (current focus)',
        'complete task called "Phase 3: AI chatbot integration (current focus)"'
    ]
    
    success = False
    for i, attempt in enumerate(completion_attempts):
        print(f"  Attempt {i+1}: {attempt}")
        try:
            chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                        headers=headers, json={"message": attempt})
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"    [OK] Success: {response_data['response']}")
                success = True
                break
            else:
                print(f"    [INFO] Failed: {chat_response.text}")
        except Exception as e:
            print(f"    [ERROR] Exception: {e}")
    
    if not success:
        print("  [ERROR] All completion attempts failed")
        return False

    print("\\n[OK] Complex task title test completed!")
    return True

if __name__ == "__main__":
    success = test_complex_task_title()
    if success:
        print("\\n[SUCCESS] Complex task title issue resolved!")
    else:
        print("\\n[ERROR] Complex task title issue still exists.")
        sys.exit(1)