"""ValidatorAgent - Content validation and quality assurance."""

from agents.core.base_agent import BaseAgent
from agents.models.outputs import ValidatorOutput, ValidatorInput, SuggestedEdit
from agents.prompts.validator import VALIDATOR_SYSTEM_PROMPT, VALIDATOR_USER_PROMPT


# Mock response for demo mode
MOCK_VALIDATOR_OUTPUT = ValidatorOutput(
    confidence_score=0.82,
    explanation="The content demonstrates strong strategic thinking and is well-structured. Confidence is reduced due to lack of specific quantitative targets in some areas and limited discussion of competitive response scenarios.",
    strengths=[
        "Clear strategic direction with actionable tactics",
        "Realistic budget allocation aligned with priorities",
        "Good balance of offensive and defensive strategies",
        "Strong focus on measurable outcomes"
    ],
    weaknesses=[
        "Timeline lacks specific milestones and dependencies",
        "Limited discussion of competitive response scenarios",
        "Budget allocation doesn't account for contingencies",
        "Missing international market considerations"
    ],
    suggested_edits=[
        SuggestedEdit(
            section="Timeline",
            original="Q1: PCP education launch. Q2: Retail partnerships established.",
            suggested="Q1 (Jan-Mar): PCP education launch (target 10K physicians/month). Milestone: 30K physicians trained by Mar 31. Q2 (Apr-Jun): Retail partnerships with CVS (Apr 15), Walgreens (May 1), Walmart (Jun 1). Milestone: 75% of US population within 5 miles of participating pharmacy.",
            reason="Adding specific dates, targets, and milestones improves accountability and progress tracking"
        ),
        SuggestedEdit(
            section="Budget Allocation",
            original="Current budget allocation totals $45M",
            suggested="Total budget: $45M + 10% contingency reserve ($4.5M) for market response and unforeseen competitive actions",
            reason="Contingency planning is essential given market volatility and competitive threats"
        )
    ],
    validation_status="needs_revision"
)


class ValidatorAgent(BaseAgent[ValidatorOutput]):
    """Agent for validating content quality."""

    def __init__(self):
        super().__init__(
            name="ValidatorAgent",
            system_prompt=VALIDATOR_SYSTEM_PROMPT,
            response_model=ValidatorOutput,
            mock_response=MOCK_VALIDATOR_OUTPUT
        )

    async def validate(self, input_data: ValidatorInput) -> ValidatorOutput:
        """Validate content and provide feedback."""

        # Format validation criteria
        criteria = "\n".join(input_data.validation_criteria or [
            "Accuracy and factual correctness",
            "Completeness and thoroughness",
            "Actionability and specificity",
            "Strategic alignment",
            "Risk consideration"
        ])

        # Create user prompt
        user_prompt = VALIDATOR_USER_PROMPT.format(
            content_type=input_data.content_type,
            content=input_data.content,
            validation_criteria=criteria
        )

        # Run validation
        return await self.run(user_prompt)


# Singleton instance
validator_agent = ValidatorAgent()
