"""FastAPI routes for agent orchestration."""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from agents.analyzer_agent import analyzer_agent
from agents.strategy_agent import strategy_agent
from agents.brand_plan_agent import brand_plan_agent
from agents.scenario_agent import scenario_agent
from agents.validator_agent import validator_agent
from agents.insight_discovery_agent import insight_discovery_agent

from agents.models.outputs import (
    AnalyzerInput, AnalyzerOutput,
    StrategyInput, StrategyOutput,
    BrandPlanInput, BrandPlanOutput,
    ScenarioInput, ScenarioOutput,
    ValidatorInput, ValidatorOutput,
    InsightDiscoveryInput, InsightDiscoveryOutput
)

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/analyzer", response_model=AnalyzerOutput)
async def run_analyzer(input_data: AnalyzerInput) -> AnalyzerOutput:
    """
    Run AnalyzerAgent to analyze brand and competitive landscape.

    Returns key insights, market gaps, and opportunities.
    """
    try:
        result = await analyzer_agent.analyze(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analyzer agent failed: {str(e)}")


@router.post("/strategy", response_model=StrategyOutput)
async def run_strategy(input_data: StrategyInput) -> StrategyOutput:
    """
    Run StrategyAgent to develop strategic framework.

    Returns SWOT analysis, competitive positioning, and strategic recommendations.
    """
    try:
        result = await strategy_agent.strategize(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Strategy agent failed: {str(e)}")


@router.post("/brand-plan", response_model=BrandPlanOutput)
async def run_brand_plan(input_data: BrandPlanInput) -> BrandPlanOutput:
    """
    Run BrandPlanAgent to create comprehensive brand plan.

    Returns complete brand plan with executive summary, market analysis, strategy, KPIs, etc.
    """
    try:
        result = await brand_plan_agent.create_plan(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brand plan agent failed: {str(e)}")


@router.post("/scenario", response_model=ScenarioOutput)
async def run_scenario(input_data: ScenarioInput) -> ScenarioOutput:
    """
    Run ScenarioAgent to analyze what-if scenarios.

    Returns impact analysis, risk level, and 3 defensive tactics.
    """
    try:
        result = await scenario_agent.analyze_scenario(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scenario agent failed: {str(e)}")


@router.post("/validator", response_model=ValidatorOutput)
async def run_validator(input_data: ValidatorInput) -> ValidatorOutput:
    """
    Run ValidatorAgent to validate AI-generated content.

    Returns confidence score, explanation, and suggested edits.
    """
    try:
        result = await validator_agent.validate(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validator agent failed: {str(e)}")


@router.post("/insight-discovery", response_model=InsightDiscoveryOutput)
async def run_insight_discovery(input_data: InsightDiscoveryInput) -> InsightDiscoveryOutput:
    """
    Run InsightDiscoveryAgent to discover novel insights.

    Returns "things you might not know" insights from market data.
    """
    try:
        result = await insight_discovery_agent.discover(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insight discovery agent failed: {str(e)}")


@router.get("/health")
async def agents_health() -> Dict[str, Any]:
    """Check health of all agents."""
    from core.config import settings

    return {
        "status": "healthy",
        "mock_mode": settings.MOCK_MODE,
        "agents": [
            "analyzer",
            "strategy",
            "brand_plan",
            "scenario",
            "validator",
            "insight_discovery"
        ]
    }
