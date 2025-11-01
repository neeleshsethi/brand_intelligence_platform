"""Pydantic models for structured agent outputs."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


# Analyzer Agent Output
class MarketInsight(BaseModel):
    """Individual market insight."""
    category: str = Field(description="Category of insight (opportunity, threat, trend, etc.)")
    description: str = Field(description="Detailed description of the insight")
    impact: str = Field(description="Potential impact (high, medium, low)")


class AnalyzerOutput(BaseModel):
    """Output from AnalyzerAgent."""
    key_insights: List[MarketInsight] = Field(description="List of key market insights")
    market_gaps: List[str] = Field(description="Identified gaps in the market")
    opportunities: List[str] = Field(description="Strategic opportunities")
    summary: str = Field(description="Executive summary of analysis")


# Strategy Agent Output
class SWOTAnalysis(BaseModel):
    """SWOT analysis structure."""
    strengths: List[str] = Field(description="Internal strengths")
    weaknesses: List[str] = Field(description="Internal weaknesses")
    opportunities: List[str] = Field(description="External opportunities")
    threats: List[str] = Field(description="External threats")


class StrategyOutput(BaseModel):
    """Output from StrategyAgent."""
    swot: SWOTAnalysis = Field(description="SWOT analysis")
    competitive_positioning: str = Field(description="Recommended competitive positioning")
    key_differentiators: List[str] = Field(description="Key brand differentiators")
    strategic_recommendations: List[str] = Field(description="Strategic recommendations")


# Brand Plan Agent Output
class KPI(BaseModel):
    """Key Performance Indicator."""
    metric: str = Field(description="Metric name")
    target: str = Field(description="Target value")
    timeframe: str = Field(description="Timeframe for achievement")


class BrandPlanOutput(BaseModel):
    """Output from BrandPlanAgent."""
    executive_summary: str = Field(description="Executive summary")
    market_analysis: str = Field(description="Market analysis section")
    strategy: str = Field(description="Strategy section")
    tactics: List[str] = Field(description="Tactical initiatives")
    kpis: List[KPI] = Field(description="Key performance indicators")
    budget_allocation: Dict[str, float] = Field(description="Budget allocation by channel")
    timeline: str = Field(description="Implementation timeline")


# Scenario Agent Output
class DefensiveTactic(BaseModel):
    """Defensive tactic for scenario."""
    tactic: str = Field(description="Name/title of the tactic")
    description: str = Field(description="Detailed description")
    implementation_difficulty: str = Field(description="Difficulty level (easy, medium, hard)")
    expected_impact: str = Field(description="Expected impact (high, medium, low)")


class ScenarioOutput(BaseModel):
    """Output from ScenarioAgent."""
    scenario: str = Field(description="The what-if scenario analyzed")
    impact_analysis: str = Field(description="Detailed impact analysis")
    risk_level: str = Field(description="Overall risk level (critical, high, medium, low)")
    defensive_tactics: List[DefensiveTactic] = Field(description="Three defensive tactics")
    recommended_action: str = Field(description="Immediate recommended action")
    confidence_score: float = Field(default=0.85, description="Confidence in the analysis (0-1)", ge=0, le=1)


# Validator Agent Output
class SuggestedEdit(BaseModel):
    """Suggested edit for content."""
    section: str = Field(description="Section or part to edit")
    original: str = Field(description="Original text")
    suggested: str = Field(description="Suggested replacement")
    reason: str = Field(description="Reason for the edit")


class ValidatorOutput(BaseModel):
    """Output from ValidatorAgent."""
    confidence_score: float = Field(description="Confidence score 0-1", ge=0, le=1)
    explanation: str = Field(description="Explanation of confidence score")
    strengths: List[str] = Field(description="Strengths of the content")
    weaknesses: List[str] = Field(description="Weaknesses or concerns")
    suggested_edits: List[SuggestedEdit] = Field(description="Suggested improvements")
    validation_status: str = Field(description="Status (approved, needs_revision, rejected)")


# Insight Discovery Agent Output
class DiscoveredInsight(BaseModel):
    """A discovered insight."""
    title: str = Field(description="Insight title")
    description: str = Field(description="Detailed description")
    source: str = Field(description="Data source or reasoning")
    novelty_score: float = Field(description="How novel/surprising (0-1)", ge=0, le=1)
    actionability: str = Field(description="How actionable (high, medium, low)")


class InsightDiscoveryOutput(BaseModel):
    """Output from InsightDiscoveryAgent."""
    discovered_insights: List[DiscoveredInsight] = Field(description="List of discovered insights")
    data_sources_analyzed: List[str] = Field(description="Data sources that were analyzed")
    summary: str = Field(description="Summary of discoveries")
    recommended_next_steps: List[str] = Field(description="Recommended actions based on insights")


# Common input models
class BrandData(BaseModel):
    """Brand data input."""
    brand_id: Optional[str] = None
    name: str
    company: str
    therapeutic_area: str
    market_share: Optional[float] = None
    additional_context: Optional[str] = None


class CompetitorData(BaseModel):
    """Competitor data input."""
    name: str
    company: str
    market_share: Optional[float] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None


class AnalyzerInput(BaseModel):
    """Input for AnalyzerAgent."""
    brand: BrandData
    competitors: List[CompetitorData]
    market_context: Optional[str] = None


class StrategyInput(BaseModel):
    """Input for StrategyAgent."""
    brand: BrandData
    analyzer_output: Optional[str] = None  # JSON string of AnalyzerOutput


class BrandPlanInput(BaseModel):
    """Input for BrandPlanAgent."""
    brand: BrandData
    strategy_output: Optional[str] = None  # JSON string of StrategyOutput
    budget: Optional[float] = None
    timeframe: Optional[str] = "12 months"
    strategic_goals: Optional[str] = None


class ScenarioInput(BaseModel):
    """Input for ScenarioAgent."""
    brand: BrandData
    scenario_question: str = Field(description="The what-if question to analyze")
    current_context: Optional[str] = None


class ValidatorInput(BaseModel):
    """Input for ValidatorAgent."""
    content_type: str = Field(description="Type of content (brand_plan, insight, strategy, etc.)")
    content: str = Field(description="The content to validate")
    validation_criteria: Optional[List[str]] = None


class InsightDiscoveryInput(BaseModel):
    """Input for InsightDiscoveryAgent."""
    brand: BrandData
    data_sources: Optional[List[str]] = None
    focus_areas: Optional[List[str]] = None
