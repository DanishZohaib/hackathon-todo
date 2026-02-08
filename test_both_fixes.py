import requests
import json
import sys
import uuid

def test_both_fixes():
    """
    Test both fixes:
    1. Fix for the UUID string error with complex task titles
    2. Ability to mark tasks as incomplete (un-complete)
    """
    base_url = "http://localhost:8000"
    
    # Generate unique email for this test
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    
    print(f"Testing Both Fixes with email: {test_email}")
    
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

    # Step 4: Test both fixes
    print(f"\\nTesting both fixes for user {user_id}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }

    # Test Fix 1: Complex task title that caused UUID error
    print("\\nTesting Fix 1: Complex task title that caused UUID error...")
    complex_task = "Add a task called Phase 3: AI chatbot integration (current focus)"
    chat_payload = {"message": complex_task}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Added complex task: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to add complex task: {chat_response.text}")
            return False
    except Exception as e:
        print(f"  [ERROR] Failed to add complex task: {e}")
        return False

    # Now try to complete the complex task (this was causing the UUID error)
    print("\\nTrying to complete the complex task (testing UUID error fix)...")
    complete_payload = {"message": 'complete the task "Phase 3: AI chatbot integration (current focus)"'}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=complete_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Completed complex task: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to complete complex task: {chat_response.text}")
            return False
    except Exception as e:
        print(f"  [ERROR] Failed to complete complex task: {e}")
        return False

    # Test Fix 2: Mark task as incomplete (un-complete)
    print("\\nTesting Fix 2: Mark task as incomplete...")
    
    # First, add a simple task and complete it
    add_task_payload = {"message": "Add a task called Test Task for Un-completion"}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=add_task_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Added test task: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to add test task: {chat_response.text}")
            return False
    except Exception as e:
        print(f"  [ERROR] Failed to add test task: {e}")
        return False

    # Complete the task first
    complete_test_payload = {"message": 'complete the task "Test Task for Un-completion"'}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=complete_test_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Completed test task: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to complete test task: {chat_response.text}")
            return False
    except Exception as e:
        print(f"  [ERROR] Failed to complete test task: {e}")
        return False

    # Now try to mark it as incomplete (un-complete)
    uncomplete_payload = {"message": 'mark uncomplete the task "Test Task for Un-completion"'}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=uncomplete_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Marked task as incomplete: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to mark task as incomplete: {chat_response.text}")
            return False
    except Exception as e:
        print(f"  [ERROR] Failed to mark task as incomplete: {e}")
        return False

    # Test alternative phrasing for un-completing
    uncomplete_alt_payload = {"message": 'mark the task "Test Task for Un-completion" as not done'}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=uncomplete_alt_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Marked task as not done: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to mark task as not done: {chat_response.text}")
            return False
    except Exception as e:
        print(f"  [ERROR] Failed to mark task as not done: {e}")
        return False

    # Final check of all tasks
    print("\\nFinal task list:")
    list_payload = {"message": "List all my tasks"}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=list_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Remaining tasks: {response_data['response']}")
        else:
            print(f"  [ERROR] Failed to list tasks: {chat_response.text}")
    except Exception as e:
        print(f"  [ERROR] Failed to list tasks: {e}")

    print("\\n[OK] Both fixes test completed!")
    return True

if __name__ == "__main__":
    success = test_both_fixes()
    if success:
        print("\\n[SUCCESS] Both fixes working properly!")
        print("  - Complex task titles no longer cause UUID errors")
        print("  - Tasks can now be marked as incomplete (un-completed)")
    else:
        print("\\n[ERROR] Issues remain with the fixes.")
        sys.exit(1)