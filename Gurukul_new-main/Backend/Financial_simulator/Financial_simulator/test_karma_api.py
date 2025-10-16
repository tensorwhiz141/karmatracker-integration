"""
Simplified test version of the Financial Simulator API for Karma score testing
This version removes the advanced dependencies for easier testing
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

# FastAPI imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class FinancialProfile(BaseModel):
    """Financial profile for simulation"""
    name: str
    monthly_income: float = Field(gt=0, description="Monthly income in currency units")
    expenses: List[Dict[str, Any]] = Field(default_factory=list, description="List of expenses")
    financial_goal: str = Field(description="Financial goal description")
    financial_type: str = Field(default="Conservative", description="Investment style: Conservative, Moderate, Aggressive")
    risk_level: str = Field(default="Low", description="Risk tolerance: Low, Medium, High")

class SimulationRequest(BaseModel):
    """Request for financial simulation"""
    profile: FinancialProfile
    simulation_months: int = Field(12, ge=1, le=120, description="Number of months to simulate")
    user_id: Optional[str] = Field(None, description="User ID for tracking")

class SimulationResponse(BaseModel):
    """Response from financial simulation"""
    status: str
    simulation_id: str
    results: Dict[str, Any]
    recommendations: List[str]
    timestamp: str

# Add this new model for user Karma score requests
class UserKarmaRequest(BaseModel):
    """Request for user Karma score"""
    user_id: str = Field(..., description="User ID to fetch Karma score for")
    financial_profile: Optional[FinancialProfile] = Field(None, description="Optional financial profile for calculation")

class UserKarmaResponse(BaseModel):
    """Response for user Karma score"""
    user_id: str
    karma_score: float
    karma_level: str
    karma_message: str
    breakdown: Dict[str, float]
    insights: Dict[str, Any]
    timestamp: str

# FastAPI app
app = FastAPI(
    title="Financial Simulator API - Karma Testing Version",
    description="Simplified version for testing Karma score functionality",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FinancialSimulator:
    """Main financial simulator class with enhanced agent-based functionality"""
    
    def __init__(self):
        self.active_simulations = {}
        self.simulation_results = {}
        
    def calculate_savings_potential(self, profile: FinancialProfile) -> Dict[str, float]:
        """Calculate savings potential based on profile"""
        total_expenses = sum(float(expense.get('amount', 0)) for expense in profile.expenses)
        potential_savings = profile.monthly_income - total_expenses
        
        return {
            "monthly_income": profile.monthly_income,
            "total_expenses": total_expenses,
            "potential_savings": potential_savings,
            "savings_rate": (potential_savings / profile.monthly_income) * 100 if profile.monthly_income > 0 else 0
        }
    
    def calculate_karmic_score(self, profile: FinancialProfile, savings_info: Dict) -> Dict[str, Any]:
        """Calculate karmic score based on financial behavior and goals"""
        savings_rate = savings_info["savings_rate"]
        goal_alignment = 0
        discipline_score = 0
        wellness_score = 0
        
        # Goal alignment scoring (0-100)
        if "emergency" in profile.financial_goal.lower():
            goal_alignment = 85  # Emergency fund is high priority
        elif "investment" in profile.financial_goal.lower() or "growth" in profile.financial_goal.lower():
            goal_alignment = 75  # Investment goals are good
        elif "debt" in profile.financial_goal.lower() or "pay off" in profile.financial_goal.lower():
            goal_alignment = 90  # Debt reduction is excellent
        elif "save" in profile.financial_goal.lower():
            goal_alignment = 70  # General saving is good
        else:
            goal_alignment = 50  # Unclear goals
        
        # Discipline score based on savings rate
        if savings_rate >= 20:
            discipline_score = 95
        elif savings_rate >= 15:
            discipline_score = 85
        elif savings_rate >= 10:
            discipline_score = 75
        elif savings_rate >= 5:
            discipline_score = 60
        else:
            discipline_score = 30
        
        # Wellness score based on financial stress indicators
        expense_to_income_ratio = savings_info["total_expenses"] / profile.monthly_income
        if expense_to_income_ratio < 0.7:
            wellness_score = 90  # Very healthy
        elif expense_to_income_ratio < 0.8:
            wellness_score = 80  # Healthy
        elif expense_to_income_ratio < 0.9:
            wellness_score = 65  # Moderate stress
        elif expense_to_income_ratio < 0.95:
            wellness_score = 45  # High stress
        else:
            wellness_score = 25  # Very high stress
        
        # Calculate overall karmic score (weighted average)
        karmic_score = (
            goal_alignment * 0.3 +  # 30% weight
            discipline_score * 0.4 +  # 40% weight
            wellness_score * 0.3     # 30% weight
        )
        
        # Determine karmic level
        if karmic_score >= 90:
            karmic_level = "Enlightened Investor"
            karmic_message = "Your financial wisdom shines brightly! You demonstrate exceptional discipline and clarity."
        elif karmic_score >= 80:
            karmic_level = "Wise Planner"
            karmic_message = "You show great financial wisdom. Continue on this path of mindful money management."
        elif karmic_score >= 70:
            karmic_level = "Conscious Saver"
            karmic_message = "You're developing good financial habits. Keep building your financial consciousness."
        elif karmic_score >= 60:
            karmic_level = "Awakening Spender"
            karmic_message = "You're beginning to understand financial balance. Focus on increasing your savings discipline."
        else:
            karmic_level = "Seeking Balance"
            karmic_message = "Your financial journey is just beginning. Embrace mindful spending and conscious saving."
        
        return {
            "overall_score": round(karmic_score, 2),
            "level": karmic_level,
            "message": karmic_message,
            "breakdown": {
                "goal_alignment": round(goal_alignment, 2),
                "discipline_score": round(discipline_score, 2),
                "wellness_score": round(wellness_score, 2)
            },
            "insights": {
                "savings_rate_category": "Excellent" if savings_rate >= 20 else "Good" if savings_rate >= 10 else "Needs Improvement",
                "stress_level": "Low" if expense_to_income_ratio < 0.8 else "Medium" if expense_to_income_ratio < 0.9 else "High",
                "goal_clarity": "Clear" if goal_alignment >= 70 else "Moderate" if goal_alignment >= 50 else "Unclear"
            }
        }
    
    def generate_investment_recommendations(self, profile: FinancialProfile, karma_score: float = 75.0) -> List[str]:
        """Generate investment recommendations based on profile and Karma score"""
        recommendations = []
        
        savings_info = self.calculate_savings_potential(profile)
        savings_rate = savings_info["savings_rate"]
        
        # Adjust recommendations based on Karma score
        if karma_score >= 90:
            # Enlightened Investor - Most advanced recommendations
            recommendations.append("🌟 Karmic Excellence: You qualify for premium investment opportunities")
            recommendations.append("📈 Advanced Portfolio: Consider ESG investments and impact investing")
            recommendations.append("💰 Wealth Preservation: Explore alternative assets like REITs and commodities")
        elif karma_score >= 80:
            # Wise Planner - Good recommendations
            recommendations.append("🎯 Karmic Wisdom: Focus on diversified, ethical investments")
            recommendations.append("📊 Balanced Growth: Consider a mix of growth and value stocks")
            recommendations.append("🏦 Capital Preservation: Maintain emergency fund at 6-9 months expenses")
        elif karma_score >= 70:
            # Conscious Saver - Standard recommendations
            recommendations.append("🌱 Karmic Growth: Build core portfolio with index funds")
            recommendations.append("⚖️ Balanced Approach: Mix of stocks and bonds appropriate to your risk")
            recommendations.append("🛡️ Safety First: Emergency fund covering 3-6 months expenses")
        elif karma_score >= 60:
            # Awakening Spender - Conservative recommendations
            recommendations.append("🔍 Karmic Awareness: Focus on debt reduction before aggressive investing")
            recommendations.append("📉 Conservative Growth: Start with low-cost index funds")
            recommendations.append("💸 Cash Flow: Prioritize building positive cash flow habits")
        else:
            # Seeking Balance - Basic recommendations
            recommendations.append("🚧 Karmic Foundation: Focus on financial fundamentals")
            recommendations.append("🔐 Security First: Prioritize high-yield savings and CDs")
            recommendations.append("🧾 Budget Mastery: Eliminate high-interest debt before investing")
        
        # Base recommendations based on savings rate
        if savings_rate < 10:
            recommendations.append("Focus on expense reduction to increase savings rate above 10%")
            recommendations.append("Consider creating a detailed budget to track spending")
        elif savings_rate < 20:
            recommendations.append("Good savings rate! Consider diversifying into low-risk investments")
            recommendations.append("Build an emergency fund covering 3-6 months of expenses")
        else:
            recommendations.append("Excellent savings rate! You can consider higher-yield investments")
        
        # Risk-based recommendations
        if profile.risk_level.lower() == "low":
            recommendations.append("Consider government bonds, high-yield savings accounts, and CDs")
            recommendations.append("Focus on capital preservation with modest growth")
        elif profile.risk_level.lower() == "medium":
            recommendations.append("Balanced portfolio with 60% stocks, 40% bonds")
            recommendations.append("Consider index funds and diversified ETFs")
        else:  # High risk
            recommendations.append("Growth-focused portfolio with higher stock allocation")
            recommendations.append("Consider growth stocks, emerging markets, and alternative investments")
        
        return recommendations

# Initialize simulator
simulator = FinancialSimulator()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Financial Simulator - Karma Testing Version",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/user-karma", response_model=UserKarmaResponse)
async def get_user_karma_score(request: UserKarmaRequest):
    """Get user's Karma score with detailed breakdown"""
    try:
        # If financial profile is provided, calculate Karma score
        if request.financial_profile:
            savings_info = simulator.calculate_savings_potential(request.financial_profile)
            karmic_analysis = simulator.calculate_karmic_score(request.financial_profile, savings_info)
        else:
            # Return stored Karma score for user (placeholder implementation)
            # In a real implementation, this would fetch from database
            karmic_analysis = {
                "overall_score": 75.0,
                "level": "Conscious Saver",
                "message": "You're developing good financial habits. Keep building your financial consciousness.",
                "breakdown": {
                    "goal_alignment": 70.0,
                    "discipline_score": 80.0,
                    "wellness_score": 75.0
                },
                "insights": {
                    "savings_rate_category": "Good",
                    "stress_level": "Medium",
                    "goal_clarity": "Clear"
                }
            }
        
        return UserKarmaResponse(
            user_id=request.user_id,
            karma_score=karmic_analysis["overall_score"],
            karma_level=karmic_analysis["level"],
            karma_message=karmic_analysis["message"],
            breakdown=karmic_analysis["breakdown"],
            insights=karmic_analysis["insights"],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error fetching user Karma score: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch Karma score: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Financial Simulator API - Karma Testing Version",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/health",
            "/user-karma"
        ]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(
        "test_karma_api:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )