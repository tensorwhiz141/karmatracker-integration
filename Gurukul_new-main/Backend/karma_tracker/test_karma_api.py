"""
Test script for Karma Tracker API
"""

import requests
import json
import time
from datetime import datetime

def test_karma_api():
    """Test the Karma Tracker API endpoints"""
    
    base_url = "http://localhost:8005"
    
    print("="*60)
    print("🧪 TESTING KARMA TRACKER API")
    print("="*60)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test 2: Seed test users
    print("\n2. Seeding test users...")
    try:
        response = requests.get(f"{base_url}/seed_users", timeout=10)
        if response.status_code == 200:
            print("✅ Test users seeded")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Seeding failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
    
    # Test 3: Get initial karma
    print("\n3. Getting initial karma for test user...")
    try:
        response = requests.get(f"{base_url}/get_karma?user_id=test_user_001", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Initial karma retrieved")
            print(f"   User ID: {data['user_id']}")
            print(f"   Karma Score: {data['karma_score']}")
            print(f"   Last Update: {data['last_update']}")
        else:
            print(f"❌ Failed to get karma with status {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to get karma: {e}")
    
    # Test 4: Update karma - learning task completed
    print("\n4. Updating karma for learning task completion...")
    karma_update = {
        "user_id": "test_user_001",
        "action_type": "learning_task_completed",
        "value": 10.0
    }
    try:
        response = requests.post(f"{base_url}/update_karma", json=karma_update, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Karma updated for learning task")
            print(f"   New Karma Score: {data['karma_score']}")
            print(f"   Message: {data['message']}")
        else:
            print(f"❌ Failed to update karma with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Failed to update karma: {e}")
    
    # Test 5: Update karma - agent suggestion provided
    print("\n5. Updating karma for agent suggestion...")
    karma_update = {
        "user_id": "test_user_001",
        "action_type": "agent_suggestion_provided",
        "value": 5.0
    }
    try:
        response = requests.post(f"{base_url}/update_karma", json=karma_update, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Karma updated for agent suggestion")
            print(f"   New Karma Score: {data['karma_score']}")
            print(f"   Message: {data['message']}")
        else:
            print(f"❌ Failed to update karma with status {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to update karma: {e}")
    
    # Test 6: Update karma - negative action
    print("\n6. Updating karma for negative action (skipped task)...")
    karma_update = {
        "user_id": "test_user_001",
        "action_type": "task_skipped",
        "value": -2.0
    }
    try:
        response = requests.post(f"{base_url}/update_karma", json=karma_update, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Karma updated for negative action")
            print(f"   New Karma Score: {data['karma_score']}")
            print(f"   Message: {data['message']}")
        else:
            print(f"❌ Failed to update karma with status {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to update karma: {e}")
    
    # Test 7: Final karma check
    print("\n7. Final karma check...")
    try:
        response = requests.get(f"{base_url}/get_karma?user_id=test_user_001", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Final karma retrieved")
            print(f"   User ID: {data['user_id']}")
            print(f"   Final Karma Score: {data['karma_score']}")
            print(f"   Last Action: {data['source_action']}")
        else:
            print(f"❌ Failed to get final karma with status {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to get final karma: {e}")
    
    # Test 8: Check events
    print("\n8. Checking karma events...")
    try:
        response = requests.get(f"{base_url}/events?limit=5", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Events retrieved")
            print(f"   Event count: {data['count']}")
            for event in data['events']:
                print(f"   - {event['payload']['user_id']}: {event['payload']['source_action']} ({event['payload']['value']})")
        else:
            print(f"❌ Failed to get events with status {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to get events: {e}")
    
    print("\n" + "="*60)
    print("🏁 Karma Tracker API Testing Completed!")
    print("="*60)

if __name__ == "__main__":
    test_karma_api()