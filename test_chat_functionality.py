import requests
import json
import time
import subprocess
import sys

def test_chat_functionality():
    """
    Test the chat functionality to ensure the AI assistant properly handles task additions
    """
    base_url = "http://localhost:8000"
    
    print("Testing AI Assistant Chat Functionality...")
    
    # Step 1: Health check
    try:
        health_response = requests.get(f"{base_url}/health")
        print(f"[OK] Health check: {health_response.status_code}, {health_response.json()}")
    except Exception as e:
        print(f"[ERROR] Health check failed: {e}")
        return False

    # Step 2: Register a test user
    print("\nCreating a test user...")
    try:
        register_data = {
            "email": "testuser@example.com",
            "password": "SecurePassword123!",
            "full_name": "Test User"
        }
        register_response = requests.post(f"{base_url}/auth/register", json=register_data)
        print(f"Registration response: {register_response.status_code}")
        if register_response.status_code != 200 and register_response.status_code != 400:  # 400 might mean user already exists
            print(f"✗ Registration failed: {register_response.text}")
            return False
    except Exception as e:
        print(f"✗ Registration request failed: {e}")
        return False

    # Step 3: Login to get JWT token
    print("\nLogging in to get JWT token...")
    try:
        login_data = {
            "username": "testuser@example.com",
            "password": "SecurePassword123!"
        }
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login response status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            jwt_token = token_data.get("access_token")
            user_id = token_data.get("user_id")  # Get the user ID from the response
            print(f"✓ Got JWT token, user_id: {user_id}")
        else:
            print(f"✗ Login failed: {login_response.text}")
            
            # Try to login again in case user already existed
            if "already exists" in login_response.text or login_response.status_code == 400:
                login_response = requests.post(f"{base_url}/auth/login", json=login_data)
                if login_response.status_code == 200:
                    token_data = login_response.json()
                    jwt_token = token_data.get("access_token")
                    user_id = token_data.get("user_id")
                    print(f"✓ Got JWT token after retry, user_id: {user_id}")
                else:
                    print(f"✗ Login still failed after retry: {login_response.text}")
                    return False
            else:
                return False
    except Exception as e:
        print(f"✗ Login request failed: {e}")
        return False

    # Step 4: Test the chat functionality
    print(f"\nTesting chat functionality for user {user_id}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }

    # Test 1: Add a task
    print("\nTest 1: Adding a task...")
    chat_payload = {
        "message": "Add a task to buy groceries"
    }

    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        print(f"Chat response status: {chat_response.status_code}")
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"✓ Chat response: {response_data['response']}")
            print(f"Tool calls executed: {response_data.get('tool_calls', [])}")
        else:
            print(f"✗ Chat request failed: {chat_response.text}")
            return False
    except Exception as e:
        print(f"✗ Chat request failed: {e}")
        return False

    # Test 2: List tasks
    print("\nTest 2: Listing tasks...")
    chat_payload = {
        "message": "List all my tasks"
    }

    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        print(f"Chat response status: {chat_response.status_code}")
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"✓ Chat response: {response_data['response']}")
            print(f"Tool calls executed: {response_data.get('tool_calls', [])}")
        else:
            print(f"✗ Chat request failed: {chat_response.text}")
            return False
    except Exception as e:
        print(f"✗ Chat request failed: {e}")
        return False

    # Test 3: Complete a task
    print("\nTest 3: Completing a task...")
    chat_payload = {
        "message": "Complete the first task"
    }

    try:
        chat_response = requests.post(f"{base_url}/api/{user_id}/chat", 
                                    headers=headers, json=chat_payload)
        print(f"Chat response status: {chat_response.status_code}")
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"✓ Chat response: {response_data['response']}")
            print(f"Tool calls executed: {response_data.get('tool_calls', [])}")
        else:
            print(f"✗ Chat request failed: {chat_response.text}")
            return False
    except Exception as e:
        print(f"✗ Chat request failed: {e}")
        return False

    print("\n✓ All tests completed successfully!")
    return True

if __name__ == "__main__":
    success = test_chat_functionality()
    if success:
        print("\n🎉 AI Assistant is working properly!")
    else:
        print("\n❌ There are issues with the AI Assistant that need to be fixed.")
        sys.exit(1)