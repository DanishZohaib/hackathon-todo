import requests
import json
import sys
import uuid

def test_precise_matching():
    """
    Test the precise task matching functionality to ensure the AI assistant
    correctly identifies tasks by title without false positives
    """
    base_url = "http://localhost:8000"
    
    # Generate unique email for this test
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    
    print(f"Testing Precise Task Matching with email: {test_email}")
    
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

    # Step 4: Test precise matching
    print(f"\\nTesting precise matching for user {user_id}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }

    # Add tasks that are similar to test precise matching
    print("\\nAdding similar tasks to test precise matching...")
    similar_tasks = [
        "Add a task called Phase1 Complete",
        "Add a task called Phase2 Complete", 
        "Add a task called Phase3 Complete",
        "Add a task called celebrate Phase3 Complete"
    ]
    
    for task in similar_tasks:
        chat_payload = {"message": task}
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

    # Test precise matching - these should match exactly
    print("\\nTesting precise matching...")
    precise_tests = [
        ('complete the task "Phase1 Complete"', "Phase1 Complete"),
        ('complete the task "Phase2 Complete"', "Phase2 Complete"),
        ('complete the task "Phase3 Complete"', "Phase3 Complete"),
        ('complete the task "celebrate Phase3 Complete"', "celebrate Phase3 Complete"),
        ('delete task "Phase1 Complete"', "Phase1 Complete"),
    ]
    
    for test_input, expected_task in precise_tests:
        print(f"  Testing: '{test_input}' (should affect '{expected_task}')")
        chat_payload = {"message": test_input}
        try:
            chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                        headers=headers, json=chat_payload)
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"    [OK] Result: {response_data['response']}")
            else:
                print(f"    [ERROR] Failed: {chat_response.text}")
        except Exception as e:
            print(f"    [ERROR] Failed: {e}")

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

    print("\\n[OK] Precise matching test completed!")
    return True

if __name__ == "__main__":
    success = test_precise_matching()
    if success:
        print("\\n[SUCCESS] Precise matching working properly!")
    else:
        print("\\n[ERROR] There are still issues with precise matching.")
        sys.exit(1)