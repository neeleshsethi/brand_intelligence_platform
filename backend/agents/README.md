# LangGraph Multi-Agent System

Simplified 6-agent system for pharmaceutical brand planning with structured outputs, retry logic, and demo mode.

## Architecture

### Agents

1. **AnalyzerAgent** - Market & competitive analysis
   - Input: Brand data + competitor data
   - Output: Key insights, market gaps, opportunities

2. **StrategyAgent** - Strategic planning
   - Input: Analyzer output
   - Output: SWOT analysis, competitive positioning, differentiators

3. **BrandPlanAgent** - Comprehensive planning
   - Input: Brand info + strategy
   - Output: Complete brand plan (executive summary, market analysis, strategy, KPIs)

4. **ScenarioAgent** - What-if analysis
   - Input: "What-if" question
   - Output: Impact analysis + 3 defensive tactics

5. **ValidatorAgent** - Quality assurance
   - Input: AI-generated content
   - Output: Confidence score + explanation + suggested edits

6. **InsightDiscoveryAgent** - Novel insight mining
   - Input: Latest market data
   - Output: "Things you might not know" insights

### Technology Stack

- **LangChain/LangGraph**: Agent framework
- **Instructor**: Structured outputs with Pydantic
- **Tenacity**: Retry logic with exponential backoff
- **LangSmith**: Tracing and observability
- **Pydantic**: Schema validation and structured outputs

### Key Features

**Structured Outputs**: All agents return validated Pydantic models

**Retry Logic**: Automatic retry with exponential backoff (configurable)

**Mock Mode**: Instant fake responses for demos without LLM API calls

**Prompt Separation**: All prompts in separate files for easy modification

**Type Safety**: Full TypeScript-like type safety with Pydantic

## Usage

### 1. Enable Mock Mode (for demos)

```bash
# In backend/.env
MOCK_MODE=true
```

All agents will return instant mock responses without calling LLMs.

### 2. Production Mode

```bash
# In backend/.env
MOCK_MODE=false
OPENAI_API_KEY=your_key_here
LANGCHAIN_API_KEY=your_langsmith_key
```

### 3. API Endpoints

```
POST /api/agents/analyzer          - Run market analysis
POST /api/agents/strategy           - Develop strategy
POST /api/agents/brand-plan         - Create brand plan
POST /api/agents/scenario           - Analyze what-if scenario
POST /api/agents/validator          - Validate content
POST /api/agents/insight-discovery  - Discover insights
GET  /api/agents/health             - Check agent health
```

### 4. Example: Analyzer Agent

```python
from agents.models.outputs import AnalyzerInput, BrandData, CompetitorData

# Create input
input_data = AnalyzerInput(
    brand=BrandData(
        name="Paxlovid",
        company="Pfizer",
        therapeutic_area="COVID-19 Antiviral",
        market_share=65.4
    ),
    competitors=[
        CompetitorData(
            name="Lagevrio",
            company="Merck",
            market_share=34.6
        )
    ]
)

# Call API
response = requests.post(
    "http://localhost:8000/api/agents/analyzer",
    json=input_data.model_dump()
)

result = response.json()
# Returns: AnalyzerOutput with key_insights, market_gaps, opportunities
```

### 5. Example: Scenario Agent

```python
from agents.models.outputs import ScenarioInput, BrandData

input_data = ScenarioInput(
    brand=BrandData(
        name="Paxlovid",
        company="Pfizer",
        therapeutic_area="COVID-19 Antiviral",
        market_share=65.4
    ),
    scenario_question="What if a generic competitor launches at 50% lower price?"
)

response = requests.post(
    "http://localhost:8000/api/agents/scenario",
    json=input_data.model_dump()
)

result = response.json()
# Returns: ScenarioOutput with impact_analysis, risk_level, 3 defensive_tactics
```

## Project Structure

```
backend/agents/
├── README.md                          # This file
├── core/
│   └── base_agent.py                  # Base agent with retry & mock support
├── models/
│   └── outputs.py                     # Pydantic models for all I/O
├── prompts/
│   ├── analyzer.py                    # Analyzer prompts
│   ├── strategy.py                    # Strategy prompts
│   ├── brand_plan.py                  # Brand plan prompts
│   ├── scenario.py                    # Scenario prompts
│   ├── validator.py                   # Validator prompts
│   └── insight_discovery.py           # Insight discovery prompts
├── analyzer_agent.py                  # AnalyzerAgent implementation
├── strategy_agent.py                  # StrategyAgent implementation
├── brand_plan_agent.py                # BrandPlanAgent implementation
├── scenario_agent.py                  # ScenarioAgent implementation
├── validator_agent.py                 # ValidatorAgent implementation
└── insight_discovery_agent.py         # InsightDiscoveryAgent implementation
```

## Configuration

### Environment Variables

```bash
# Mock mode
MOCK_MODE=false                    # Set to true for instant demo responses

# OpenAI
OPENAI_API_KEY=sk-...              # Required for production mode

# LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=pfizer-brand-planning

# Retry configuration
MAX_RETRIES=3                      # Number of retry attempts
RETRY_WAIT_SECONDS=2               # Initial wait time (exponential backoff)
```

## Retry Logic

All agents automatically retry on failures with exponential backoff:

```python
@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=RETRY_WAIT_SECONDS, max=10),
    retry=retry_if_exception_type((Exception,))
)
```

- Attempt 1: Immediate
- Attempt 2: Wait 2 seconds
- Attempt 3: Wait 4 seconds
- Max wait: 10 seconds

## Adding New Agents

1. **Create prompt file** in `prompts/`
2. **Define Pydantic models** in `models/outputs.py`
3. **Create agent class** extending `BaseAgent`
4. **Add mock response** for demo mode
5. **Add API route** in `api/agents.py`

Example:

```python
from agents.core.base_agent import BaseAgent
from agents.models.outputs import MyOutput, MyInput
from agents.prompts.my_agent import MY_SYSTEM_PROMPT, MY_USER_PROMPT

MOCK_MY_OUTPUT = MyOutput(...)

class MyAgent(BaseAgent[MyOutput]):
    def __init__(self):
        super().__init__(
            name="MyAgent",
            system_prompt=MY_SYSTEM_PROMPT,
            response_model=MyOutput,
            mock_response=MOCK_MY_OUTPUT
        )

    async def my_method(self, input_data: MyInput) -> MyOutput:
        user_prompt = MY_USER_PROMPT.format(data=input_data)
        return await self.run(user_prompt)

my_agent = MyAgent()
```

## Testing

### Test with Mock Mode

```bash
# Start server with mock mode
export MOCK_MODE=true
python main.py

# All agents return instant mock responses
curl -X POST http://localhost:8000/api/agents/analyzer \
  -H "Content-Type: application/json" \
  -d '{"brand": {...}, "competitors": [...]}'
```

### Test with Real LLMs

```bash
# Start server with real API keys
export MOCK_MODE=false
export OPENAI_API_KEY=sk-...
python main.py

# Agents call OpenAI GPT-4
curl -X POST http://localhost:8000/api/agents/analyzer ...
```

## LangSmith Tracing

When `LANGCHAIN_TRACING_V2=true`, all agent runs are automatically traced in LangSmith:

- View full conversation history
- Monitor latency and costs
- Debug agent behavior
- Analyze prompt performance

Visit: https://smith.langchain.com/

## Performance

**Mock Mode**: <10ms response time
**Production Mode**: 2-5 seconds per agent (depending on LLM)

Retry logic adds minimal overhead (~2-4s on failures).

## License

Proprietary - Pfizer Internal Use Only
