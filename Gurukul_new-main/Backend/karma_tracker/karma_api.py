"""
Karma Tracker API Service

This service handles Karma tracking for user actions and events in the BHIV system.
It provides endpoints for updating and retrieving user Karma scores.
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

# FastAPI imports
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class KarmaUpdateRequest(BaseModel):
    """Request for updating user Karma"""
    user_id: str = Field(..., description="User ID to update Karma for")
    action_type: str = Field(..., description="Type of action performed")
    value: float = Field(..., description="Karma value to add/subtract")

class KarmaUpdateResponse(BaseModel):
    """Response for Karma update"""
    user_id: str
    karma_score: float
    last_update: str
    source_action: str
    message: str

class KarmaGetResponse(BaseModel):
    """Response for getting user Karma"""
    user_id: str
    karma_score: float
    last_update: str
    source_action: str

# FastAPI app
app = FastAPI(
    title="Karma Tracker API",
    description="API for tracking user Karma scores based on actions and events",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for Karma data (in production, this would be a database)
karma_storage = {}

# Event log file
EVENTS_LOG_FILE = "karma_events.log"

class KarmaTracker:
    """Main Karma Tracker class"""
    
    def __init__(self):
        self.load_karma_data()
    
    def load_karma_data(self):
        """Load existing Karma data from file if it exists"""
        try:
            if os.path.exists("karma_data.json"):
                with open("karma_data.json", "r") as f:
                    global karma_storage
                    karma_storage = json.load(f)
                logger.info("Loaded existing Karma data")
        except Exception as e:
            logger.warning(f"Failed to load Karma data: {e}")
    
    def save_karma_data(self):
        """Save Karma data to file"""
        try:
            with open("karma_data.json", "w") as f:
                json.dump(karma_storage, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save Karma data: {e}")
    
    def update_karma(self, user_id: str, action_type: str, value: float) -> Dict[str, Any]:
        """Update Karma for a user based on an action"""
        try:
            # Get current karma data for user or initialize if not exists
            if user_id not in karma_storage:
                karma_storage[user_id] = {
                    "karma_score": 0.0,
                    "last_update": datetime.now().isoformat(),
                    "source_action": "initial"
                }
            
            # Update karma score
            current_data = karma_storage[user_id]
            new_score = current_data["karma_score"] + value
            
            # Update storage
            karma_storage[user_id] = {
                "karma_score": new_score,
                "last_update": datetime.now().isoformat(),
                "source_action": action_type
            }
            
            # Save to file
            self.save_karma_data()
            
            # Log the event
            self.log_karma_event(user_id, new_score, action_type, value)
            
            # Determine message based on value
            if value > 0:
                message = f"Karma increased by {value} points for {action_type}"
            elif value < 0:
                message = f"Karma decreased by {abs(value)} points for {action_type}"
            else:
                message = f"Karma unchanged for {action_type}"
            
            return {
                "user_id": user_id,
                "karma_score": new_score,
                "last_update": datetime.now().isoformat(),
                "source_action": action_type,
                "message": message
            }
            
        except Exception as e:
            logger.error(f"Error updating karma for user {user_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to update karma: {str(e)}")
    
    def get_karma(self, user_id: str) -> Dict[str, Any]:
        """Get current Karma for a user"""
        try:
            if user_id not in karma_storage:
                # Initialize with zero karma if user doesn't exist
                karma_storage[user_id] = {
                    "karma_score": 0.0,
                    "last_update": datetime.now().isoformat(),
                    "source_action": "initial"
                }
                self.save_karma_data()
            
            user_data = karma_storage[user_id]
            return {
                "user_id": user_id,
                "karma_score": user_data["karma_score"],
                "last_update": user_data["last_update"],
                "source_action": user_data["source_action"]
            }
            
        except Exception as e:
            logger.error(f"Error getting karma for user {user_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to get karma: {str(e)}")
    
    def log_karma_event(self, user_id: str, karma_score: float, action_type: str, value: float):
        """Log a Karma event to file"""
        try:
            event_data = {
                "event_id": f"event_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                "event_type": "karma_updated",
                "timestamp": datetime.now().isoformat(),
                "payload": {
                    "user_id": user_id,
                    "karma_score": karma_score,
                    "source_action": action_type,
                    "value": value
                }
            }
            
            # Append to events log file
            with open(EVENTS_LOG_FILE, "a") as f:
                f.write(f"{json.dumps(event_data)}\n")
                
            logger.info(f"Karma event logged: {user_id} - {action_type} ({value})")
            
        except Exception as e:
            logger.error(f"Failed to log karma event: {e}")

# Initialize tracker
karma_tracker = KarmaTracker()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Karma Tracker API",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/update_karma", response_model=KarmaUpdateResponse)
async def update_karma_endpoint(request: KarmaUpdateRequest):
    """Update user's Karma based on an action"""
    logger.info(f"Updating karma for user {request.user_id} with action {request.action_type} and value {request.value}")
    result = karma_tracker.update_karma(request.user_id, request.action_type, request.value)
    return result

@app.get("/get_karma", response_model=KarmaGetResponse)
async def get_karma_endpoint(user_id: str = Query(..., description="User ID to get Karma for")):
    """Get user's current Karma score"""
    logger.info(f"Getting karma for user {user_id}")
    result = karma_tracker.get_karma(user_id)
    return result

@app.get("/seed_users")
async def seed_test_users():
    """Seed test users with initial Karma values"""
    test_users = [
        {"user_id": "test_user_001", "karma_score": 50.0},
        {"user_id": "test_user_002", "karma_score": 75.0},
        {"user_id": "workflow_user_001", "karma_score": 25.0},
        {"user_id": "default_user", "karma_score": 10.0}
    ]
    
    seeded_users = []
    for user in test_users:
        karma_storage[user["user_id"]] = {
            "karma_score": user["karma_score"],
            "last_update": datetime.now().isoformat(),
            "source_action": "seeded"
        }
        seeded_users.append(user["user_id"])
    
    karma_tracker.save_karma_data()
    
    return {
        "message": f"Seeded {len(seeded_users)} test users",
        "users": seeded_users
    }

@app.get("/events")
async def get_karma_events(limit: int = Query(10, description="Number of events to return")):
    """Get recent Karma events"""
    events = []
    try:
        if os.path.exists(EVENTS_LOG_FILE):
            with open(EVENTS_LOG_FILE, "r") as f:
                lines = f.readlines()
                # Get last N events
                for line in lines[-limit:]:
                    events.append(json.loads(line.strip()))
    except Exception as e:
        logger.error(f"Error reading events: {e}")
    
    return {
        "events": events,
        "count": len(events)
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Karma Tracker API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/health",
            "/update_karma",
            "/get_karma",
            "/seed_users",
            "/events"
        ]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8005))  # Default port for Karma Tracker
    logger.info(f"Starting Karma Tracker API on port {port}")
    uvicorn.run(
        "karma_api:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )