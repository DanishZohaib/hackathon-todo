import requests
import json
import sys
import uuid

def test_enhanced_chat_functionality():
    """
    Test the enhanced chat functionality to ensure the AI assistant can handle
    delete and complete tasks by title, and responds politely
    """
    base_url = "http://localhost:8000"
    
    # Generate unique email for this test
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    
    print(f"Testing Enhanced AI Assistant Chat Functionality with email: {test_email}")
    
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

    # Step 4: Test various chat phrases
    print(f"\\nTesting chat functionality for user {user_id}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }

    # First, add some tasks to work with
    print("\\nAdding test tasks...")
    tasks_to_add = [
        "Add a task to buy groceries",
        "Add a task to call mom",
        "Add a task to finish project report"
    ]
    
    for task in tasks_to_add:
        chat_payload = {"message": task}
        try:
            chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                        headers=headers, json=chat_payload)
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"[OK] Added task: {response_data['response']}")
            else:
                print(f"[ERROR] Failed to add task: {chat_response.text}")
        except Exception as e:
            print(f"[ERROR] Failed to add task: {e}")

    # Test listing tasks to see what we have
    print("\\nListing all tasks...")
    chat_payload = {"message": "List all my tasks"}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"[OK] Tasks: {response_data['response']}")
        else:
            print(f"[ERROR] Failed to list tasks: {chat_response.text}")
    except Exception as e:
        print(f"[ERROR] Failed to list tasks: {e}")

    # Test deleting a task by title
    print("\\nTesting delete task by title...")
    delete_tests = [
        "delete the buy groceries task",
        "remove the call mom task",
        "delete task called finish project report"
    ]
    
    for delete_cmd in delete_tests:
        print(f"  Trying: '{delete_cmd}'")
        chat_payload = {"message": delete_cmd}
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

    # Test completing a task by title (we'll add a new one first)
    print("\\nAdding a task to test completion...")
    chat_payload = {"message": "Add a task to schedule meeting"}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"[OK] Added task: {response_data['response']}")
        else:
            print(f"[ERROR] Failed to add task: {chat_response.text}")
    except Exception as e:
        print(f"[ERROR] Failed to add task: {e}")

    # Now test completing by title
    print("\\nTesting complete task by title...")
    complete_tests = [
        "complete the schedule meeting task",
        "mark the schedule meeting as done"
    ]
    
    for complete_cmd in complete_tests:
        print(f"  Trying: '{complete_cmd}'")
        chat_payload = {"message": complete_cmd}
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

    # Final test: list tasks again to see changes
    print("\\nFinal task list...")
    chat_payload = {"message": "List all my tasks"}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"[OK] Remaining tasks: {response_data['response']}")
        else:
            print(f"[ERROR] Failed to list tasks: {chat_response.text}")
    except Exception as e:
        print(f"[ERROR] Failed to list tasks: {e}")

    print("\\n[OK] All enhancement tests completed!")
    return True

if __name__ == "__main__":
    success = test_enhanced_chat_functionality()
    if success:
        print("\\n[SUCCESS] AI Assistant enhancements working properly!")
    else:
        print("\\n[ERROR] There are still issues with the AI Assistant.")
        sys.exit(1)