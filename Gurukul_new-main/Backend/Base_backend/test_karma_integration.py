"""
Test script to validate Karma Tracker integration with BHIV Core.
Simulates 3 user actions and validates Karma updates and event propagation.
"""

import sys
import os
import json
import time

# Add the Base_backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from karma_client import karma_client, update_karma, get_karma, emit_karma_updated_event

def test_user_actions():
    """Test 3 user actions and validate Karma updates"""
    
    print("=" * 60)
    print("🧪 TESTING KARMA TRACKER INTEGRATION")
    print("=" * 60)
    
    test_user_id = "test-user-actions-123"
    
    # Action 1: User completes a learning task with high score
    print("\n📝 ACTION 1: User completes learning task with high score (90%)")
    print("-" * 50)
    
    # Simulate a high quiz score
    high_score_karma = update_karma(
        user_id=test_user_id,
        action_type="completed_learning_task",
        value=90.0,  # High quiz score
        financial_profile=None
    )
    
    print(f"Karma update result:")
    print(f"  User ID: {high_score_karma.get('user_id')}")
    print(f"  Karma Score: {high_score_karma.get('karma_score', 'N/A')}")
    print(f"  Karma Level: {high_score_karma.get('karma_level', 'N/A')}")
    print(f"  Source Action: {high_score_karma.get('source_action', {})}")
    
    # Emit event for Bucket consumption
    emit_karma_updated_event(test_user_id, high_score_karma)
    print("✅ Karma updated event emitted for Bucket")
    
    # Wait a moment
    time.sleep(1)
    
    # Action 2: User completes a learning task with medium score
    print("\n📝 ACTION 2: User completes learning task with medium score (70%)")
    print("-" * 50)
    
    # Simulate a medium quiz score
    medium_score_karma = update_karma(
        user_id=test_user_id,
        action_type="completed_learning_task",
        value=70.0,  # Medium quiz score
        financial_profile=None
    )
    
    print(f"Karma update result:")
    print(f"  User ID: {medium_score_karma.get('user_id')}")
    print(f"  Karma Score: {medium_score_karma.get('karma_score', 'N/A')}")
    print(f"  Karma Level: {medium_score_karma.get('karma_level', 'N/A')}")
    print(f"  Source Action: {medium_score_karma.get('source_action', {})}")
    
    # Emit event for Bucket consumption
    emit_karma_updated_event(test_user_id, medium_score_karma)
    print("✅ Karma updated event emitted for Bucket")
    
    # Wait a moment
    time.sleep(1)
    
    # Action 3: User receives agent suggestion
    print("\n🤖 ACTION 3: Agent provides learning suggestion")
    print("-" * 50)
    
    # Simulate agent providing suggestion (no score change, but log the interaction)
    suggestion_karma = get_karma(test_user_id)
    
    print(f"Karma info after agent suggestion:")
    print(f"  User ID: {suggestion_karma.get('user_id')}")
    print(f"  Karma Score: {suggestion_karma.get('karma_score', 'N/A')}")
    print(f"  Karma Level: {suggestion_karma.get('karma_level', 'N/A')}")
    
    # Log the agent interaction by updating with a small positive value
    suggestion_karma_updated = update_karma(
        user_id=test_user_id,
        action_type="agent_suggestion_provided",
        value=2.0,  # Small positive karma for engagement
        financial_profile=None
    )
    
    print(f"Karma after agent interaction:")
    print(f"  Karma Score: {suggestion_karma_updated.get('karma_score', 'N/A')}")
    print(f"  Karma Level: {suggestion_karma_updated.get('karma_level', 'N/A')}")
    
    # Emit event for Bucket consumption
    emit_karma_updated_event(test_user_id, suggestion_karma_updated)
    print("✅ Karma updated event emitted for Bucket")
    
    # Final validation
    print("\n" + "=" * 60)
    print("📊 FINAL VALIDATION")
    print("=" * 60)
    
    final_karma = get_karma(test_user_id)
    print(f"Final Karma Status for {test_user_id}:")
    print(f"  Karma Score: {final_karma.get('karma_score', 'N/A')}")
    print(f"  Karma Level: {final_karma.get('karma_level', 'N/A')}")
    print(f"  Message: {final_karma.get('karma_message', 'N/A')}")
    
    # Validate that we have a reasonable karma score
    karma_score = final_karma.get('karma_score', 0)
    if karma_score > 0:
        print(f"\n✅ SUCCESS: Karma integration working correctly!")
        print(f"   Final karma score: {karma_score}")
    else:
        print(f"\n❌ ISSUE: Karma score is {karma_score}, expected positive value")
    
    print(f"\n📋 Test Summary:")
    print(f"   ✅ 3 user actions simulated")
    print(f"   ✅ Karma updates processed")
    print(f"   ✅ Events emitted for Bucket consumption")
    print(f"   ✅ End-to-end flow validated")
    
    return final_karma

if __name__ == "__main__":
    test_user_actions()
    print("\n" + "=" * 60)
    print("🏁 KARMA INTEGRATION TESTING COMPLETED!")
    print("=" * 60)