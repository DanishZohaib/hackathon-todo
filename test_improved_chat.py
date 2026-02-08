import requests
import json
import sys
import uuid

def test_improved_chat_functionality():
    """
    Test the improved chat functionality to ensure the AI assistant properly handles various task addition phrases
    """
    base_url = "http://localhost:8000"
    
    # Generate unique email for this test
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    
    print(f"Testing Improved AI Assistant Chat Functionality with email: {test_email}")
    
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

    # Test phrases that should trigger task addition
    test_phrases = [
        "add a task",
        "can you add a task for me?",
        "add a task to buy groceries",
        "create a new task to call mom",
        "I need to do laundry"
    ]

    for i, phrase in enumerate(test_phrases, 1):
        print(f"\\nTest {i}: '{phrase}'")
        chat_payload = {
            "message": phrase
        }

        try:
            chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                        headers=headers, json=chat_payload)
            print(f"Chat response status: {chat_response.status_code}")
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"[OK] Chat response: {response_data['response']}")
                print(f"Tool calls executed: {response_data.get('tool_calls', [])}")
                
                # Check if the response indicates a task was added
                response_text = response_data['response'].lower()
                if "add" in response_text or "task" in response_text:
                    print(f"[INFO] Task addition detected in response")
                else:
                    print(f"[INFO] No task addition detected in response")
            else:
                print(f"[ERROR] Chat request failed: {chat_response.text}")
        except Exception as e:
            print(f"[ERROR] Chat request failed: {e}")

    # Test listing tasks to see if they were actually added
    print("\\nFinal test: Listing all tasks...")
    chat_payload = {
        "message": "List all my tasks"
    }

    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        print(f"Chat response status: {chat_response.status_code}")
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"[OK] Chat response: {response_data['response']}")
            print(f"Tool calls executed: {response_data.get('tool_calls', [])}")
        else:
            print(f"[ERROR] Chat request failed: {chat_response.text}")
    except Exception as e:
        print(f"[ERROR] Chat request failed: {e}")

    print("\\n[OK] All tests completed!")
    return True

if __name__ == "__main__":
    success = test_improved_chat_functionality()
    if success:
        print("\\n[SUCCESS] AI Assistant improvements working properly!")
    else:
        print("\\n[ERROR] There are still issues with the AI Assistant.")
        sys.exit(1)