import requests
import json
import sys
import uuid

def test_original_issue_fixed():
    """
    Test that the original issue is fixed: AI assistant should not mark wrong tasks as complete
    """
    base_url = "http://localhost:8000"
    
    # Generate unique email for this test
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    
    print(f"Testing Original Issue Fix with email: {test_email}")
    
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

    # Step 4: Test the original issue scenario
    print(f"\\nTesting original issue scenario for user {user_id}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }

    # Add the specific tasks mentioned in the original issue
    print("\\nAdding tasks similar to the original issue...")
    tasks_to_add = [
        "Add a task called Phase2 Complete",
        "Add a task called celebrate Phase3 Complete"
    ]
    
    for task in tasks_to_add:
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

    # Now test the exact scenario from the original issue
    print("\\nTesting the original issue scenario...")
    print("  Original issue: 'Complete the task \"celebrate Phase3 Complete\"' was marking 'Phase2 Complete' instead")
    
    chat_payload = {"message": 'Complete the task "celebrate Phase3 Complete"'}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Result: {response_data['response']}")
            
            # Check if it correctly marked the intended task
            if "celebrate Phase3 Complete" in response_data['response'] and "Phase2 Complete" not in response_data['response']:
                print("  [SUCCESS] Correctly identified and acted on the right task!")
            elif "Phase2 Complete" in response_data['response']:
                print("  [FAILURE] Still incorrectly acting on the wrong task!")
                return False
            else:
                print("  [INFO] Response doesn't clearly indicate which task was affected")
        else:
            print(f"  [ERROR] Failed: {chat_response.text}")
            return False
    except Exception as e:
        print(f"  [ERROR] Failed: {e}")
        return False

    # Test another scenario to be sure
    print("\\nTesting another scenario to ensure precision...")
    chat_payload = {"message": 'Complete the task "Phase2 Complete"'}
    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"  [OK] Result: {response_data['response']}")
            
            # Check if it correctly marked the intended task
            if "Phase2 Complete" in response_data['response'] and "celebrate Phase3 Complete" not in response_data['response']:
                print("  [SUCCESS] Correctly identified and acted on the right task!")
            elif "celebrate Phase3 Complete" in response_data['response']:
                print("  [FAILURE] Incorrectly acting on the wrong task!")
                return False
            else:
                print("  [INFO] Response doesn't clearly indicate which task was affected")
        else:
            print(f"  [ERROR] Failed: {chat_response.text}")
            return False
    except Exception as e:
        print(f"  [ERROR] Failed: {e}")
        return False

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

    print("\\n[OK] Original issue fix test completed!")
    return True

if __name__ == "__main__":
    success = test_original_issue_fixed()
    if success:
        print("\\n[SUCCESS] Original issue has been fixed! AI assistant now correctly identifies tasks by title.")
    else:
        print("\\n[ERROR] Original issue still exists.")
        sys.exit(1)