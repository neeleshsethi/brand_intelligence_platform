"""StrategyAgent - Strategic planning and SWOT analysis."""

from agents.core.base_agent import BaseAgent
from agents.models.outputs import StrategyOutput, StrategyInput, SWOTAnalysis
from agents.prompts.strategy import STRATEGY_SYSTEM_PROMPT, STRATEGY_USER_PROMPT


# Mock response for demo mode
MOCK_STRATEGY_OUTPUT = StrategyOutput(
    swot=SWOTAnalysis(
        strengths=[
            "Superior clinical efficacy (89% hospitalization reduction)",
            "Strong brand recognition from emergency use",
            "Robust manufacturing and distribution network"
        ],
        weaknesses=[
            "High price point vs competitors",
            "Complex drug-drug interaction profile",
            "Limited long-term safety data"
        ],
        opportunities=[
            "Long-COVID prevention indication expansion",
            "International market penetration",
            "Combination therapy protocols"
        ],
        threats=[
            "Generic competition in 18-24 months",
            "Declining COVID prevalence reduces demand",
            "Payer coverage restrictions"
        ]
    ),
    competitive_positioning="Position as the gold-standard early treatment for high-risk COVID patients, emphasizing superior efficacy and established safety profile.",
    key_differentiators=[
        "Highest efficacy in preventing hospitalization (89% vs 30%)",
        "Fastest time to viral clearance",
        "Most extensive clinical trial data"
    ],
    strategic_recommendations=[
        "Pivot marketing from emergency response to endemic preparedness",
        "Invest in long-COVID prevention clinical trials",
        "Build PCP education programs for early treatment protocols",
        "Develop risk stratification tools for patient identification",
        "Establish retail pharmacy partnerships for rapid access"
    ]
)


class StrategyAgent(BaseAgent[StrategyOutput]):
    """Agent for strategic planning and analysis."""

    def __init__(self):
        super().__init__(
            name="StrategyAgent",
            system_prompt=STRATEGY_SYSTEM_PROMPT,
            response_model=StrategyOutput,
            mock_response=MOCK_STRATEGY_OUTPUT
        )

    async def strategize(self, input_data: StrategyInput) -> StrategyOutput:
        """Develop strategic framework."""

        # Generate brand-specific mock response if in MOCK_MODE
        from core.config import settings
        if settings.MOCK_MODE:
            return self._get_brand_specific_mock(input_data)

        # Format brand info
        brand_info = f"""
Brand: {input_data.brand.name}
Company: {input_data.brand.company}
Therapeutic Area: {input_data.brand.therapeutic_area}
Market Share: {input_data.brand.market_share}%
"""

        # Create user prompt
        user_prompt = STRATEGY_USER_PROMPT.format(
            brand_info=brand_info,
            market_analysis=input_data.analyzer_output or "No market analysis provided"
        )

        # Run strategy development
        return await self.run(user_prompt)

    def _get_brand_specific_mock(self, input_data: StrategyInput) -> StrategyOutput:
        """Get mock response tailored to the brand's therapeutic area."""
        therapeutic_area = input_data.brand.therapeutic_area.lower()

        if "anticoagulant" in therapeutic_area or "blood thinner" in therapeutic_area:
            # Eliquis/Xarelto - Anticoagulant market
            return StrategyOutput(
                swot=SWOTAnalysis(
                    strengths=[
                        "No dietary restrictions (vs warfarin)",
                        "Predictable pharmacokinetics, no INR monitoring required",
                        "Strong clinical trial data (RE-LY, ARISTOTLE studies)"
                    ],
                    weaknesses=[
                        "No specific reversal agent widely available",
                        "Higher cost than warfarin",
                        "Limited dose adjustment options"
                    ],
                    opportunities=[
                        "Expanding indications beyond AFib (VTE, DVT)",
                        "Post-surgery thromboprophylaxis market",
                        "Patient convenience messaging vs warfarin"
                    ],
                    threats=[
                        "Competing NOACs with similar profiles",
                        "Generic competition approaching",
                        "Payer pressure for therapeutic substitution"
                    ]
                ),
                competitive_positioning="Position as the most convenient and reliable anticoagulant option for AFib patients, emphasizing freedom from dietary restrictions and monitoring requirements.",
                key_differentiators=[
                    "No dietary restrictions unlike warfarin",
                    "No routine blood monitoring (INR) required",
                    "Proven efficacy in preventing stroke in AFib patients"
                ],
                strategic_recommendations=[
                    "Target newly diagnosed AFib patients before warfarin initiation",
                    "Partner with cardiology practices for direct patient education",
                    "Develop adherence support programs for elderly patients",
                    "Build real-world evidence showing lower bleeding rates",
                    "Create patient-friendly materials highlighting convenience benefits"
                ]
            )
        else:
            # Default to COVID antiviral (Paxlovid/Lagevrio)
            return MOCK_STRATEGY_OUTPUT


# Singleton instance
strategy_agent = StrategyAgent()
