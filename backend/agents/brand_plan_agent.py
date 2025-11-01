"""BrandPlanAgent - Comprehensive brand planning."""

from agents.core.base_agent import BaseAgent
from agents.models.outputs import BrandPlanOutput, BrandPlanInput, KPI
from agents.prompts.brand_plan import BRAND_PLAN_SYSTEM_PROMPT, BRAND_PLAN_USER_PROMPT


# Mock response for demo mode
MOCK_BRAND_PLAN_OUTPUT = BrandPlanOutput(
    executive_summary="Comprehensive 12-month plan to transition Paxlovid from pandemic emergency treatment to endemic standard of care, focusing on PCP education, patient access, and evidence generation for long-COVID prevention.",
    market_analysis="COVID-19 antiviral market declining 35% YoY but stabilizing with endemic phase. High-risk populations (65+, immunocompromised) remain significant opportunity. Competition limited but price pressure increasing.",
    strategy="Position as gold-standard treatment for high-risk patients. Invest in clinical evidence for long-COVID prevention. Build PCP capability and retail pharmacy partnerships for rapid access.",
    tactics=[
        "Launch 'Early Treatment Saves Lives' PCP education campaign",
        "Deploy risk stratification tools to 50,000 primary care practices",
        "Partner with top 5 retail pharmacy chains for rapid dispensing",
        "Initiate Phase 3 trial for long-COVID prevention indication",
        "Develop patient awareness campaign targeting 65+ demographic"
    ],
    kpis=[
        KPI(metric="Market Share", target="62%", timeframe="Q4 2025"),
        KPI(metric="PCP Prescribers", target="50,000 active", timeframe="6 months"),
        KPI(metric="Time to Treatment", target="<48 hours", timeframe="9 months"),
        KPI(metric="Patient Awareness (65+)", target="75%", timeframe="12 months")
    ],
    budget_allocation={
        "PCP Sales Force": 15750000,
        "Medical Education": 11250000,
        "Patient Awareness": 9000000,
        "Retail Partnerships": 4500000,
        "Clinical Trials": 4500000
    },
    timeline="Q1: PCP education launch. Q2: Retail partnerships established. Q3: Patient campaign launch. Q4: Long-COVID trial enrollment complete."
)


class BrandPlanAgent(BaseAgent[BrandPlanOutput]):
    """Agent for comprehensive brand planning."""

    def __init__(self):
        super().__init__(
            name="BrandPlanAgent",
            system_prompt=BRAND_PLAN_SYSTEM_PROMPT,
            response_model=BrandPlanOutput,
            mock_response=MOCK_BRAND_PLAN_OUTPUT
        )

    async def create_plan(self, input_data: BrandPlanInput) -> BrandPlanOutput:
        """Create comprehensive brand plan."""

        # Format brand info
        brand_info = f"""
Brand: {input_data.brand.name}
Company: {input_data.brand.company}
Therapeutic Area: {input_data.brand.therapeutic_area}
Market Share: {input_data.brand.market_share}%
"""

        # Create user prompt
        user_prompt = BRAND_PLAN_USER_PROMPT.format(
            brand_info=brand_info,
            strategy=input_data.strategy_output or "No strategy provided",
            budget=f"${input_data.budget:,.0f}" if input_data.budget else "Not specified",
            timeframe=input_data.timeframe
        )

        # Run brand planning
        return await self.run(user_prompt)


# Singleton instance
brand_plan_agent = BrandPlanAgent()
