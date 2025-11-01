"""InsightDiscoveryAgent - Novel insight discovery."""

from agents.core.base_agent import BaseAgent
from agents.models.outputs import InsightDiscoveryOutput, InsightDiscoveryInput, DiscoveredInsight
from agents.prompts.insight_discovery import INSIGHT_DISCOVERY_SYSTEM_PROMPT, INSIGHT_DISCOVERY_USER_PROMPT


# Mock response for demo mode
MOCK_INSIGHT_DISCOVERY_OUTPUT = InsightDiscoveryOutput(
    discovered_insights=[
        DiscoveredInsight(
            title="The 'Pharmacy Desert' Opportunity",
            description="Analysis reveals that 23% of high-risk COVID patients live in areas where the nearest pharmacy stocking antivirals is >15 miles away. These 'pharmacy deserts' correlate with lowest treatment rates but highest hospitalization risk. Mobile health units or direct-to-patient shipping could capture this untapped segment.",
            source="Geographic analysis of prescription data overlaid with hospitalization rates",
            novelty_score=0.85,
            actionability="high"
        ),
        DiscoveredInsight(
            title="The Physician Burnout Blind Spot",
            description="Primary care physicians in high-burnout practices (measured by EMR documentation time) are 40% less likely to prescribe antivirals, even when clinically indicated. The complexity of treatment protocols during time-constrained visits creates a barrier. Simplified decision tools could unlock this segment.",
            source="Correlation analysis of physician burnout metrics and prescribing patterns",
            novelty_score=0.78,
            actionability="high"
        ),
        DiscoveredInsight(
            title="The Caregiver Influence Factor",
            description="Patients whose adult children live within 20 miles are 3x more likely to receive treatment within the critical 48-hour window. Caregivers drive urgency and navigation. Marketing directly to adult children of high-risk parents (vs. patients themselves) could dramatically improve treatment rates.",
            source="Patient journey analysis of treatment timing vs. household proximity data",
            novelty_score=0.82,
            actionability="medium"
        )
    ],
    data_sources_analyzed=[
        "Prescription claims data (12M records)",
        "Geographic accessibility mapping",
        "Physician burnout surveys",
        "Patient demographic and household data",
        "Treatment timing and outcomes data"
    ],
    summary="Three non-obvious insights reveal untapped opportunities: addressing pharmacy access deserts, simplifying prescribing for burned-out physicians, and leveraging the caregiver influence on treatment urgency.",
    recommended_next_steps=[
        "Pilot mobile pharmacy program in 3 high-risk, low-access regions",
        "Develop 1-page clinical decision tool for time-constrained PCPs",
        "Create caregiver-targeted digital campaign: 'Protect Your Parents'",
        "Quantify ROI potential of each opportunity through pilot data"
    ]
)


class InsightDiscoveryAgent(BaseAgent[InsightDiscoveryOutput]):
    """Agent for discovering novel insights."""

    def __init__(self):
        super().__init__(
            name="InsightDiscoveryAgent",
            system_prompt=INSIGHT_DISCOVERY_SYSTEM_PROMPT,
            response_model=InsightDiscoveryOutput,
            mock_response=MOCK_INSIGHT_DISCOVERY_OUTPUT
        )

    async def discover(self, input_data: InsightDiscoveryInput) -> InsightDiscoveryOutput:
        """Discover novel insights."""

        # Format brand info
        brand_info = f"""
Brand: {input_data.brand.name}
Company: {input_data.brand.company}
Therapeutic Area: {input_data.brand.therapeutic_area}
Market Share: {input_data.brand.market_share}%
"""

        # Format data sources
        data_sources = "\n".join(input_data.data_sources or [
            "Market research reports",
            "Prescription claims data",
            "Physician surveys",
            "Patient journey analytics",
            "Competitive intelligence"
        ])

        # Format focus areas
        focus_areas = "\n".join(input_data.focus_areas or [
            "Patient access barriers",
            "Physician behavior patterns",
            "Emerging market trends",
            "Unmet needs",
            "Competitive gaps"
        ])

        # Create user prompt
        user_prompt = INSIGHT_DISCOVERY_USER_PROMPT.format(
            brand_info=brand_info,
            data_sources=data_sources,
            focus_areas=focus_areas
        )

        # Run insight discovery
        return await self.run(user_prompt)


# Singleton instance
insight_discovery_agent = InsightDiscoveryAgent()
