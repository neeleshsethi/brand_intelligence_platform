"""AnalyzerAgent - Market and competitive analysis."""

from agents.core.base_agent import BaseAgent
from agents.models.outputs import (
    AnalyzerOutput, AnalyzerInput, MarketInsight
)
from agents.prompts.analyzer import ANALYZER_SYSTEM_PROMPT, ANALYZER_USER_PROMPT


# Mock response for demo mode
MOCK_ANALYZER_OUTPUT = AnalyzerOutput(
    key_insights=[
        MarketInsight(
            category="opportunity",
            description="Growing demand for early treatment options as COVID transitions to endemic phase",
            impact="high"
        ),
        MarketInsight(
            category="threat",
            description="Payer resistance to high-cost antivirals as pandemic urgency decreases",
            impact="high"
        ),
        MarketInsight(
            category="trend",
            description="Shift from emergency use to preventive treatment protocols in high-risk populations",
            impact="medium"
        )
    ],
    market_gaps=[
        "Lack of patient awareness about early treatment benefits",
        "Limited primary care physician engagement in antiviral prescribing",
        "Insufficient real-world evidence for long-COVID prevention"
    ],
    opportunities=[
        "Partner with retail pharmacies for rapid access programs",
        "Develop PCP education initiatives on treatment protocols",
        "Invest in long-COVID prevention studies to expand indication"
    ],
    summary="The COVID antiviral market is transitioning from emergency response to endemic management. Key opportunities lie in educating PCPs, expanding access through retail partnerships, and building evidence for long-COVID prevention. Main threats include payer pushback and declining urgency."
)


class AnalyzerAgent(BaseAgent[AnalyzerOutput]):
    """Agent for market and competitive analysis."""

    def __init__(self):
        super().__init__(
            name="AnalyzerAgent",
            system_prompt=ANALYZER_SYSTEM_PROMPT,
            response_model=AnalyzerOutput,
            mock_response=MOCK_ANALYZER_OUTPUT
        )

    async def analyze(self, input_data: AnalyzerInput, news_articles: list = None) -> AnalyzerOutput:
        """Analyze brand and competitive landscape."""

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
{input_data.brand.additional_context or ''}
"""

        # Format competitor info
        competitor_info = "\n\n".join([
            f"Competitor: {comp.name} ({comp.company})\n"
            f"Market Share: {comp.market_share}%\n"
            f"Strengths: {', '.join(comp.strengths or [])}\n"
            f"Weaknesses: {', '.join(comp.weaknesses or [])}"
            for comp in input_data.competitors
        ])

        # Format news context
        news_context = self._format_news_context(news_articles) if news_articles else "No recent news intelligence available."

        # Create user prompt
        user_prompt = ANALYZER_USER_PROMPT.format(
            brand_info=brand_info,
            competitor_info=competitor_info,
            market_context=input_data.market_context or "No additional context provided",
            news_context=news_context
        )

        # Run analysis
        return await self.run(user_prompt)

    def _format_news_context(self, articles: list) -> str:
        """Format news articles for prompt context."""
        if not articles:
            return "No recent news intelligence available."

        formatted = []
        for idx, article in enumerate(articles[:10], 1):  # Limit to top 10
            article_text = f"""
{idx}. [{article.get('priority', 'medium').upper()}] {article.get('title', 'Untitled')}
   Source: {article.get('source', 'Unknown')} | Published: {article.get('published_at', 'Unknown date')}
   Sentiment: {article.get('sentiment', 'neutral')}
   Relevance: {article.get('relevance_reason', 'General market news')}
   Summary: {article.get('content', '')[:300]}...
   URL: {article.get('url', 'N/A')}
"""
            formatted.append(article_text.strip())

        return "\n\n".join(formatted)

    def _get_brand_specific_mock(self, input_data: AnalyzerInput) -> AnalyzerOutput:
        """Get mock response tailored to the brand's therapeutic area."""
        therapeutic_area = input_data.brand.therapeutic_area.lower()

        if "anticoagulant" in therapeutic_area or "blood thinner" in therapeutic_area:
            # Eliquis/Xarelto - Anticoagulant market
            return AnalyzerOutput(
                key_insights=[
                    MarketInsight(
                        category="opportunity",
                        description="Aging population driving increased AFib diagnosis and anticoagulant demand",
                        impact="high"
                    ),
                    MarketInsight(
                        category="threat",
                        description="Generic warfarin pressure and payer preference for lower-cost alternatives",
                        impact="high"
                    ),
                    MarketInsight(
                        category="trend",
                        description="Shift from warfarin to NOACs continuing as standard of care evolves",
                        impact="medium"
                    )
                ],
                market_gaps=[
                    "Limited real-world adherence data compared to clinical trials",
                    "Physician hesitation in elderly patients due to bleeding risk perception",
                    "Inadequate patient education on consistent dosing importance"
                ],
                opportunities=[
                    "Develop elderly patient support programs to improve adherence",
                    "Partner with cardiology practices for AFib detection initiatives",
                    "Invest in real-world evidence studies showing safety in diverse populations"
                ],
                summary="The anticoagulant market continues strong growth driven by aging populations and AFib prevalence. Key opportunities include elderly patient programs, cardiology partnerships, and real-world evidence generation. Main challenges are generic competition and bleeding risk perceptions."
            )
        else:
            # Default to COVID antiviral (Paxlovid/Lagevrio)
            return MOCK_ANALYZER_OUTPUT


# Singleton instance
analyzer_agent = AnalyzerAgent()
