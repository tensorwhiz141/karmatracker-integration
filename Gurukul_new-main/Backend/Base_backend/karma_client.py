"""
Karma Tracker Client Module
Handles communication with the Karma Tracker API for BHIV Core services.
"""

import requests
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KarmaTrackerClient:
    """
    Client for interacting with the Karma Tracker API.
    Provides methods to get and update user karma scores.
    """
    
    def __init__(self, base_url: str = "http://localhost:8002"):
        """
        Initialize the Karma Tracker client.
        
        Args:
            base_url (str): Base URL for the Karma Tracker API
        """
        self.base_url = base_url.rstrip('/')
        self.karma_endpoint = f"{self.base_url}/user-karma"
        
    def get_karma(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's current karma score.
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            Dict[str, Any]: User's karma information including score, level, and breakdown
        """
        try:
            payload = {
                "user_id": user_id
            }
            
            response = requests.post(
                self.karma_endpoint,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                karma_data = response.json()
                logger.info(f"Successfully retrieved karma for user {user_id}")
                return karma_data
            else:
                logger.error(f"Failed to get karma for user {user_id}: {response.status_code}")
                return {
                    "user_id": user_id,
                    "karma_score": 0.0,
                    "karma_level": "Unknown",
                    "karma_message": "Unable to retrieve karma score",
                    "breakdown": {},
                    "insights": {},
                    "timestamp": datetime.now().isoformat(),
                    "error": f"API returned status {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error when getting karma for user {user_id}: {e}")
            return {
                "user_id": user_id,
                "karma_score": 0.0,
                "karma_level": "Unknown",
                "karma_message": "Network error occurred",
                "breakdown": {},
                "insights": {},
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
        except Exception as e:
            logger.error(f"Unexpected error when getting karma for user {user_id}: {e}")
            return {
                "user_id": user_id,
                "karma_score": 0.0,
                "karma_level": "Unknown",
                "karma_message": "Unexpected error occurred",
                "breakdown": {},
                "insights": {},
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def update_karma(self, user_id: str, action_type: str, value: float, 
                     financial_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update user's karma based on an action.
        
        Args:
            user_id (str): Unique identifier for the user
            action_type (str): Type of action that triggered the karma update
            value (float): Value associated with the action (can be positive or negative)
            financial_profile (Optional[Dict]): Optional financial profile for detailed karma calculation
            
        Returns:
            Dict[str, Any]: Updated karma information
        """
        try:
            # For now, we'll just get the current karma and log the action
            # In a full implementation, this would update the karma based on the action
            payload = {
                "user_id": user_id
            }
            
            # Include financial profile if provided
            if financial_profile:
                payload["financial_profile"] = financial_profile
            
            response = requests.post(
                self.karma_endpoint,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                karma_data = response.json()
                logger.info(f"Successfully updated karma for user {user_id} with action '{action_type}' (value: {value})")
                
                # Add source action information to the response
                karma_data["source_action"] = {
                    "action_type": action_type,
                    "value": value,
                    "timestamp": datetime.now().isoformat()
                }
                
                return karma_data
            else:
                logger.error(f"Failed to update karma for user {user_id}: {response.status_code}")
                return {
                    "user_id": user_id,
                    "karma_score": 0.0,
                    "karma_level": "Unknown",
                    "karma_message": "Unable to update karma score",
                    "breakdown": {},
                    "insights": {},
                    "timestamp": datetime.now().isoformat(),
                    "source_action": {
                        "action_type": action_type,
                        "value": value,
                        "timestamp": datetime.now().isoformat()
                    },
                    "error": f"API returned status {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error when updating karma for user {user_id}: {e}")
            return {
                "user_id": user_id,
                "karma_score": 0.0,
                "karma_level": "Unknown",
                "karma_message": "Network error occurred",
                "breakdown": {},
                "insights": {},
                "timestamp": datetime.now().isoformat(),
                "source_action": {
                    "action_type": action_type,
                    "value": value,
                    "timestamp": datetime.now().isoformat()
                },
                "error": str(e)
            }
        except Exception as e:
            logger.error(f"Unexpected error when updating karma for user {user_id}: {e}")
            return {
                "user_id": user_id,
                "karma_score": 0.0,
                "karma_level": "Unknown",
                "karma_message": "Unexpected error occurred",
                "breakdown": {},
                "insights": {},
                "timestamp": datetime.now().isoformat(),
                "source_action": {
                    "action_type": action_type,
                    "value": value,
                    "timestamp": datetime.now().isoformat()
                },
                "error": str(e)
            }
    
    def emit_karma_updated_event(self, user_id: str, karma_data: Dict[str, Any]):
        """
        Emit a karma_updated event for the Bucket to consume.
        This is a stub implementation - in a real system, this would integrate
        with an event system like Kafka, RabbitMQ, or a webhook system.
        
        Args:
            user_id (str): Unique identifier for the user
            karma_data (Dict[str, Any]): Updated karma information
        """
        event_data = {
            "event_type": "karma_updated",
            "user_id": user_id,
            "karma_data": karma_data,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Karma updated event emitted for user {user_id}")
        logger.debug(f"Event data: {json.dumps(event_data, indent=2)}")
        
        # In a real implementation, this would send the event to a message queue
        # or webhook endpoint for the Bucket service to consume
        return event_data

# Global instance for easy access
karma_client = KarmaTrackerClient()

# Convenience functions for direct import
def get_karma(user_id: str) -> Dict[str, Any]:
    """Convenience function to get user karma"""
    return karma_client.get_karma(user_id)

def update_karma(user_id: str, action_type: str, value: float,
                 financial_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Convenience function to update user karma"""
    return karma_client.update_karma(user_id, action_type, value, financial_profile)

def emit_karma_updated_event(user_id: str, karma_data: Dict[str, Any]):
    """Convenience function to emit karma updated event"""
    return karma_client.emit_karma_updated_event(user_id, karma_data)

if __name__ == "__main__":
    # Test the client
    print("Testing Karma Tracker Client...")
    
    # Test get_karma
    test_user_id = "test-user-123"
    karma_info = get_karma(test_user_id)
    print(f"Karma info for {test_user_id}:")
    print(json.dumps(karma_info, indent=2))
    
    # Test update_karma
    updated_karma = update_karma(
        user_id=test_user_id,
        action_type="completed_learning_task",
        value=5.0
    )
    print(f"\nUpdated karma for {test_user_id}:")
    print(json.dumps(updated_karma, indent=2))
    
    # Test emit event
    emit_karma_updated_event(test_user_id, updated_karma)
    print(f"\nEvent emitted for {test_user_id}")