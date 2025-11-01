# API Quick Reference

5 simple endpoints for Pfizer AI Brand Planning prototype.

## Quick Start

```bash
# Start server
cd backend
python main.py

# Server runs at: http://localhost:8000
# API docs at: http://localhost:8000/docs
```

## Demo Mode (Recommended)

```bash
# In backend/.env
DEMO_MODE=true
MOCK_MODE=true
```
✅ Instant responses (<50ms)
✅ No API keys needed
✅ Perfect for demos

---

## 5 Main Endpoints

### 1. List Brands
```bash
GET /api/brands
```

**Example:**
```bash
curl http://localhost:8000/api/brands
```

---

### 2. Analyze Brand
```bash
POST /api/analyze/{brand_id}
```

Runs **AnalyzerAgent + StrategyAgent** → Returns insights + SWOT

**Example:**
```bash
curl -X POST http://localhost:8000/api/analyze/BRAND_ID \
  -H "Content-Type: application/json" \
  -d '{"include_competitors": true}'
```

---

### 3. Generate Brand Plan
```bash
POST /api/generate-plan/{brand_id}
```

Runs **BrandPlanAgent** → Returns complete plan

**Example:**
```bash
curl -X POST http://localhost:8000/api/generate-plan/BRAND_ID \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 45000000,
    "timeframe": "12 months"
  }'
```

---

### 4. Scenario Analysis
```bash
POST /api/scenario
```

Runs **ScenarioAgent** → Returns impact + defensive tactics

**Example:**
```bash
curl -X POST http://localhost:8000/api/scenario \
  -H "Content-Type: application/json" \
  -d '{
    "brand_name": "Paxlovid",
    "scenario_question": "What if a generic competitor launches at 50% lower price?"
  }'
```

---

### 5. Validate Content
```bash
POST /api/validate
```

Runs **ValidatorAgent** → Returns confidence score + suggestions

**Example:**
```bash
curl -X POST http://localhost:8000/api/validate \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "brand_plan",
    "content": "Your plan text here..."
  }'
```

---

## WebSocket (Real-Time Updates)

```javascript
const ws = new WebSocket('ws://localhost:8000/api/ws/progress');

ws.send(JSON.stringify({ action: 'analyze' }));

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(`${data.step}: ${data.progress}%`);
};
```

---

## Interactive Docs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Try all endpoints with built-in UI!

---

## Full Example Workflow

```bash
# 1. List all brands
curl http://localhost:8000/api/brands

# 2. Analyze a brand (copy ID from step 1)
curl -X POST http://localhost:8000/api/analyze/YOUR_BRAND_ID \
  -H "Content-Type: application/json" \
  -d '{"include_competitors": true}'

# 3. Generate plan for that brand
curl -X POST http://localhost:8000/api/generate-plan/YOUR_BRAND_ID \
  -H "Content-Type: application/json" \
  -d '{"budget": 45000000}'

# 4. Run a what-if scenario
curl -X POST http://localhost:8000/api/scenario \
  -H "Content-Type: application/json" \
  -d '{
    "brand_id": "YOUR_BRAND_ID",
    "scenario_question": "What if COVID cases drop 80%?"
  }'

# 5. Validate the generated plan
curl -X POST http://localhost:8000/api/validate \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "brand_plan",
    "content": "<paste plan from step 3>"
  }'
```

---

## Response Times

**DEMO_MODE=true:**
- All endpoints: <50ms ⚡

**Production mode:**
- Analyze: 3-4 seconds
- Generate plan: 4-6 seconds
- Scenario: 2-3 seconds
- Validate: 2-3 seconds

---

## Error Handling

All errors return:
```json
{
  "error": "Error type",
  "message": "Specific error message",
  "detail": "Stack trace (dev mode only)"
}
```

Common errors:
- `404`: Brand not found
- `500`: Agent processing failed

---

## CORS Enabled

Frontend allowed origins:
- http://localhost:3000
- http://localhost:5173
- http://127.0.0.1:3000
- http://127.0.0.1:5173
