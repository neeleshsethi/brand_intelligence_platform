# AI Agents Quick Start Guide

Get started with the 6 LangGraph agents in 5 minutes.

## 1. Enable Mock Mode (Instant Responses)

For demos without LLM API calls:

```bash
# Edit backend/.env
MOCK_MODE=true
```

All agents return realistic mock responses instantly (<10ms).

## 2. Start the Backend

```bash
cd backend
python main.py
```

Visit: http://localhost:8000/docs for interactive API documentation

## 3. Test Agents

### AnalyzerAgent - Market Analysis

```bash
curl -X POST http://localhost:8000/api/agents/analyzer \
  -H "Content-Type: application/json" \
  -d '{
    "brand": {
      "name": "Paxlovid",
      "company": "Pfizer",
      "therapeutic_area": "COVID-19 Antiviral",
      "market_share": 65.4
    },
    "competitors": [
      {
        "name": "Lagevrio",
        "company": "Merck",
        "market_share": 34.6
      }
    ]
  }'
```

**Returns**: Key insights, market gaps, opportunities

### ScenarioAgent - What-If Analysis

```bash
curl -X POST http://localhost:8000/api/agents/scenario \
  -H "Content-Type: application/json" \
  -d '{
    "brand": {
      "name": "Paxlovid",
      "company": "Pfizer",
      "therapeutic_area": "COVID-19 Antiviral",
      "market_share": 65.4
    },
    "scenario_question": "What if a generic competitor launches at 50% lower price?"
  }'
```

**Returns**: Impact analysis + 3 defensive tactics

### ValidatorAgent - Quality Check

```bash
curl -X POST http://localhost:8000/api/agents/validator \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "brand_plan",
    "content": "Launch aggressive marketing campaign targeting all demographics..."
  }'
```

**Returns**: Confidence score + suggested improvements

### InsightDiscoveryAgent - Novel Insights

```bash
curl -X POST http://localhost:8000/api/agents/insight-discovery \
  -H "Content-Type: application/json" \
  -d '{
    "brand": {
      "name": "Paxlovid",
      "company": "Pfizer",
      "therapeutic_area": "COVID-19 Antiviral",
      "market_share": 65.4
    }
  }'
```

**Returns**: "Things you might not know" insights

## 4. Enable Production Mode (Real LLMs)

```bash
# Edit backend/.env
MOCK_MODE=false
OPENAI_API_KEY=sk-your-key-here
LANGCHAIN_API_KEY=your-langsmith-key
```

Restart the server. Agents now call OpenAI GPT-4o-mini with retry logic and LangSmith tracing.

## 5. Agent Workflow Example

Typical multi-agent workflow:

```python
import requests

BASE_URL = "http://localhost:8000/api/agents"

# Step 1: Analyze market
analyzer_response = requests.post(f"{BASE_URL}/analyzer", json={
    "brand": {...},
    "competitors": [...]
})
market_analysis = analyzer_response.json()

# Step 2: Develop strategy
strategy_response = requests.post(f"{BASE_URL}/strategy", json={
    "brand": {...},
    "analyzer_output": str(market_analysis)
})
strategy = strategy_response.json()

# Step 3: Create brand plan
plan_response = requests.post(f"{BASE_URL}/brand-plan", json={
    "brand": {...},
    "strategy_output": str(strategy),
    "budget": 45000000,
    "timeframe": "12 months"
})
brand_plan = plan_response.json()

# Step 4: Validate the plan
validation_response = requests.post(f"{BASE_URL}/validator", json={
    "content_type": "brand_plan",
    "content": str(brand_plan)
})
validation = validation_response.json()

print(f"Plan confidence: {validation['confidence_score']}")
print(f"Status: {validation['validation_status']}")
```

## 6. API Endpoints Summary

| Endpoint | Agent | Purpose |
|----------|-------|---------|
| `/api/agents/analyzer` | AnalyzerAgent | Market & competitive analysis |
| `/api/agents/strategy` | StrategyAgent | SWOT & strategic planning |
| `/api/agents/brand-plan` | BrandPlanAgent | Comprehensive brand plan |
| `/api/agents/scenario` | ScenarioAgent | What-if scenario analysis |
| `/api/agents/validator` | ValidatorAgent | Content validation & QA |
| `/api/agents/insight-discovery` | InsightDiscoveryAgent | Novel insight mining |
| `/api/agents/health` | - | Agent health check |

## 7. Interactive API Documentation

Visit http://localhost:8000/docs for:
- Interactive API testing
- Request/response schemas
- Example payloads
- Try-it-out functionality

## 8. Monitoring with LangSmith

When `LANGCHAIN_TRACING_V2=true`:

1. Visit https://smith.langchain.com/
2. Select your project: `pfizer-brand-planning`
3. View all agent runs, traces, and performance metrics

## 9. Common Patterns

### Pattern 1: Chained Analysis

Analyzer → Strategy → Brand Plan

### Pattern 2: Scenario Testing

Brand Plan → Scenario Agent (multiple what-if questions)

### Pattern 3: Quality Loop

Any Agent → Validator → Revise → Validator

### Pattern 4: Insight Discovery

Insight Discovery → Analyzer (validate insights)

## 10. Troubleshooting

**"Mock mode enabled but no OpenAI key"**
- Expected behavior in mock mode
- No action needed for demos

**"Agent timeout"**
- Check `MAX_RETRIES` in .env
- Increase to 5 for flaky connections

**"Validation failed"**
- Check Pydantic model schemas in `agents/models/outputs.py`
- Ensure input matches expected format

**LangSmith not tracking**
- Verify `LANGCHAIN_TRACING_V2=true`
- Check `LANGCHAIN_API_KEY` is valid
- Ensure `LANGCHAIN_PROJECT` matches your project name

## Next Steps

- Read [backend/agents/README.md](backend/agents/README.md) for detailed docs
- Modify prompts in `backend/agents/prompts/` to customize agent behavior
- Add new agents by extending `BaseAgent` class
- Integrate agents with frontend UI

## Support

For issues or questions, see the main [README.md](README.md)
