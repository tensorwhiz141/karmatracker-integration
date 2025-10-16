# Karma Score API Documentation

## Overview
The Financial Simulator service now includes a dedicated API endpoint for fetching user Karma scores, which are used to dynamically adjust financial recommendations, spending behavior analysis, and ethical weighting in investment advice.

## API Endpoint

### Fetch User Karma Score
**POST** `/user-karma`

Get a user's Karma score with detailed breakdown and insights.

#### Request Body
```json
{
  "user_id": "string",
  "financial_profile": {
    "name": "string",
    "monthly_income": "number",
    "expenses": [
      {
        "name": "string",
        "amount": "number"
      }
    ],
    "financial_goal": "string",
    "financial_type": "string",
    "risk_level": "string"
  }
}
```

#### Response
```json
{
  "user_id": "string",
  "karma_score": "number",
  "karma_level": "string",
  "karma_message": "string",
  "breakdown": {
    "goal_alignment": "number",
    "discipline_score": "number",
    "wellness_score": "number"
  },
  "insights": {
    "savings_rate_category": "string",
    "stress_level": "string",
    "goal_clarity": "string"
  },
  "timestamp": "string"
}
```

## Karma Score Calculation

The Karma score is calculated based on three main factors:

1. **Goal Alignment (30% weight)** - How well the user's financial goals align with responsible financial behavior
2. **Discipline Score (40% weight)** - Based on the user's savings rate and spending discipline
3. **Wellness Score (30% weight)** - Based on financial stress indicators and overall financial health

### Karma Levels
- **90-100**: Enlightened Investor
- **80-89**: Wise Planner
- **70-79**: Conscious Saver
- **60-69**: Awakening Spender
- **0-59**: Seeking Balance

## Finance Bot Integration

The Finance Bot dynamically references Karma scores to:

1. **Adjust Financial Recommendations**
   - Higher Karma scores unlock premium investment opportunities
   - Ethical investing options are prioritized for high Karma users
   - Risk tolerance is adjusted based on financial discipline

2. **Influence Spending Behavior Analysis**
   - Karma scores affect growth rate projections in financial simulations
   - Spending recommendations are tailored to the user's Karma level
   - Long-term financial wellness is emphasized for all users

3. **Apply Ethical Weighting**
   - Investment recommendations include ESG (Environmental, Social, Governance) factors
   - Impact investing opportunities are highlighted for high Karma users
   - Ethical considerations are integrated into all financial advice

## Positive vs. Negative Financial Behaviors

### Positive Behaviors (Increase Karma Score)
- Maintaining emergency funds
- Paying down debt consistently
- Regular saving habits
- Responsible investment choices
- Ethical spending decisions
- Long-term financial planning

### Negative Behaviors (Decrease Karma Score)
- Living beyond means
- Accumulating high-interest debt
- Impulse spending
- Neglecting financial planning
- Ignoring investment opportunities
- Short-term thinking

## Usage Examples

### Fetch Existing User's Karma Score
```bash
curl -X POST http://localhost:8002/user-karma \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123"
  }'
```

### Calculate Karma Score from Financial Profile
```bash
curl -X POST http://localhost:8002/user-karma \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "financial_profile": {
      "name": "John Doe",
      "monthly_income": 50000,
      "expenses": [
        {"name": "Rent", "amount": 15000},
        {"name": "Food", "amount": 8000},
        {"name": "Transportation", "amount": 5000}
      ],
      "financial_goal": "Build emergency fund and start investing",
      "financial_type": "Moderate",
      "risk_level": "medium"
    }
  }'
```