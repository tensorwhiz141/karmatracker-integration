"""
Test script for the new Karma Score API endpoint
"""

import requests
import json
from datetime import datetime

def test_karma_score_api():
    """Test the new user-karma endpoint"""
    
    print("="*60)
    print("🧪 TESTING KARMA SCORE API ENDPOINT")
    print("="*60)
    
    # Test data for Karma score calculation
    financial_profile = {
        "name": "Test User",
        "monthly_income": 50000,
        "expenses": [
            {"name": "Rent", "amount": 15000},
            {"name": "Food", "amount": 8000},
            {"name": "Transportation", "amount": 5000},
            {"name": "Utilities", "amount": 3000}
        ],
        "financial_goal": "Build emergency fund and start investing",
        "financial_type": "Moderate",
        "risk_level": "medium"
    }
    
    karma_request = {
        "user_id": "test-user-karma-123",
        "financial_profile": financial_profile
    }
    
    try:
        print("Testing Karma Score API (Port 8002)...")
        print(f"Request: {json.dumps(karma_request, indent=2)}")
        
        response = requests.post(
            "http://localhost:8002/user-karma",
            json=karma_request,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Karma Score API Success!")
            print("\n📊 KARMA SCORE RESULTS:")
            
            print(f"   User ID: {data.get('user_id', 'N/A')}")
            print(f"   Overall Score: {data.get('karma_score', 'N/A')}/100")
            print(f"   Level: {data.get('karma_level', 'N/A')}")
            print(f"   Message: {data.get('karma_message', 'N/A')}")
            
            breakdown = data.get('breakdown', {})
            print(f"   📈 Goal Alignment: {breakdown.get('goal_alignment', 'N/A')}")
            print(f"   💪 Discipline Score: {breakdown.get('discipline_score', 'N/A')}")
            print(f"   🧘 Wellness Score: {breakdown.get('wellness_score', 'N/A')}")
            
            insights = data.get('insights', {})
            print(f"   💰 Savings Rate Category: {insights.get('savings_rate_category', 'N/A')}")
            print(f"   🧠 Stress Level: {insights.get('stress_level', 'N/A')}")
            print(f"   🎯 Goal Clarity: {insights.get('goal_clarity', 'N/A')}")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

def test_karma_score_without_profile():
    """Test the Karma score API without providing a financial profile"""
    
    print("\n" + "="*60)
    print("🧪 TESTING KARMA SCORE API WITHOUT PROFILE")
    print("="*60)
    
    karma_request = {
        "user_id": "test-user-karma-456"
        # No financial_profile provided - should return stored score
    }
    
    try:
        print("Testing Karma Score API without profile (Port 8002)...")
        print(f"Request: {json.dumps(karma_request, indent=2)}")
        
        response = requests.post(
            "http://localhost:8002/user-karma",
            json=karma_request,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Karma Score API Success (No Profile)!")
            print("\n📊 KARMA SCORE RESULTS:")
            
            print(f"   User ID: {data.get('user_id', 'N/A')}")
            print(f"   Overall Score: {data.get('karma_score', 'N/A')}/100")
            print(f"   Level: {data.get('karma_level', 'N/A')}")
            print(f"   Message: {data.get('karma_message', 'N/A')}")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    test_karma_score_api()
    test_karma_score_without_profile()
    print("\n" + "="*60)
    print("🏁 Karma Score API Testing Completed!")
    print("="*60)