# Financial Simulator Service

## Overview
The Financial Simulator service provides financial forecasting, simulation, and analysis capabilities using advanced machine learning models. It includes features for financial planning, investment recommendations, and Karma score-based ethical investing.

## Features
- Financial forecasting using Prophet and ARIMA models
- Investment simulation and projection
- Risk assessment and analysis
- Karma score calculation for ethical investing
- Personalized financial recommendations

## API Endpoints

### Core Endpoints
- **POST** `/start-simulation` - Run financial simulation
- **GET** `/simulation/{simulation_id}` - Get simulation results
- **GET** `/simulations` - List all simulations
- **POST** `/forecast` - Create financial forecast
- **POST** `/user-karma` - Get user's Karma score

### Health Check
- **GET** `/health` - Service health status
- **GET** `/` - Service information

## Karma Score System

The Financial Simulator includes a Karma scoring system that evaluates users' financial behavior and provides ethical investing recommendations.

### How Karma Scores Work
Karma scores are calculated based on three key factors:
1. **Goal Alignment (30%)** - How well financial goals align with responsible behavior
2. **Discipline Score (40%)** - Based on savings rate and spending discipline
3. **Wellness Score (30%)** - Based on financial stress and overall health

### Karma Levels
- **90-100**: Enlightened Investor
- **80-89**: Wise Planner
- **70-79**: Conscious Saver
- **60-69**: Awakening Spender
- **0-59**: Seeking Balance

### Ethical Investing Integration
Higher Karma scores unlock premium ethical investment opportunities, including:
- ESG (Environmental, Social, Governance) investments
- Impact investing options
- Sustainable portfolio recommendations

## Installation

1. Navigate to the Financial Simulator directory:
   ```bash
   cd Backend/Financial_simulator/Financial_simulator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the service:
   ```bash
   python langgraph_api.py
   ```

## Configuration
The service uses environment variables for configuration:
- `PORT` - Service port (default: 8002)
- MongoDB connection settings (inherited from shared configuration)

## Testing
Run the test script to verify the service is working:
```bash
python test_karma_score_api.py
```

## Documentation
For detailed API documentation, see:
- [Karma Score API Documentation](KARMA_SCORE_API.md)