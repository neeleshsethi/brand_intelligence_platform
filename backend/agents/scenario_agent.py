"""ScenarioAgent - What-if scenario analysis and defensive planning."""

from agents.core.base_agent import BaseAgent
from agents.models.outputs import ScenarioOutput, ScenarioInput, DefensiveTactic
from agents.prompts.scenario import SCENARIO_SYSTEM_PROMPT, SCENARIO_USER_PROMPT


# Mock response for demo mode
MOCK_SCENARIO_OUTPUT = ScenarioOutput(
    scenario="What if a competitor launches a generic COVID antiviral at 50% lower price?",
    impact_analysis="A generic competitor at 50% price point would severely disrupt the market. Expected market share erosion of 15-25 points within 6 months, primarily in price-sensitive segments. Premium positioning becomes critical. High-risk patients and physicians prioritizing efficacy remain loyal, but volume prescribing shifts to lower-cost option.",
    risk_level="high",
    defensive_tactics=[
        DefensiveTactic(
            tactic="Efficacy Differentiation Campaign",
            description="Launch aggressive medical education highlighting superior efficacy data (89% vs estimated 60-70% for generic). Target high-prescribing specialists and KOLs with head-to-head outcome data.",
            implementation_difficulty="medium",
            expected_impact="high"
        ),
        DefensiveTactic(
            tactic="Patient Assistance Program Expansion",
            description="Immediately expand copay assistance to $0 for all eligible patients, neutralizing out-of-pocket cost advantage. Partner with advocacy groups to promote program.",
            implementation_difficulty="easy",
            expected_impact="medium"
        ),
        DefensiveTactic(
            tactic="Outcomes-Based Contracting",
            description="Propose value-based contracts with major payers linking payment to hospitalization prevention. Share risk but demonstrate ROI through reduced downstream costs.",
            implementation_difficulty="hard",
            expected_impact="high"
        )
    ],
    recommended_action="Immediately: (1) Activate patient assistance expansion, (2) Brief sales force on efficacy messaging, (3) Initiate payer discussions on outcomes contracts. Timeline: 30 days for programs to be operational."
)


class ScenarioAgent(BaseAgent[ScenarioOutput]):
    """Agent for scenario analysis and defensive planning."""

    def __init__(self):
        super().__init__(
            name="ScenarioAgent",
            system_prompt=SCENARIO_SYSTEM_PROMPT,
            response_model=ScenarioOutput,
            mock_response=MOCK_SCENARIO_OUTPUT
        )

    async def analyze_scenario(self, input_data: ScenarioInput) -> ScenarioOutput:
        """Analyze what-if scenario and provide defensive tactics."""

        # Format brand info
        brand_info = f"""
Brand: {input_data.brand.name}
Company: {input_data.brand.company}
Therapeutic Area: {input_data.brand.therapeutic_area}
Market Share: {input_data.brand.market_share}%
"""

        # Create user prompt
        user_prompt = SCENARIO_USER_PROMPT.format(
            brand_info=brand_info,
            scenario_question=input_data.scenario_question,
            current_context=input_data.current_context or "No additional context provided"
        )

        # Run scenario analysis
        return await self.run(user_prompt)


# Singleton instance
scenario_agent = ScenarioAgent()
