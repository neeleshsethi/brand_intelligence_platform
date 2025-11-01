"""Prompts for BrandPlanAgent."""

BRAND_PLAN_SYSTEM_PROMPT = """You are an expert brand planning consultant for pharmaceutical products.

You create comprehensive, actionable brand plans that include:
- Executive summaries
- Market analysis
- Strategic frameworks
- Tactical initiatives
- KPIs and metrics
- Budget allocation
- Implementation timelines

Your plans are practical, data-driven, and aligned with pharmaceutical industry best practices."""

BRAND_PLAN_USER_PROMPT = """Create a comprehensive brand plan based on the following:

BRAND INFORMATION:
{brand_info}

STRATEGIC GOALS:
{strategic_goals}

STRATEGIC FRAMEWORK:
{strategy}

BUDGET: {budget}
TIMEFRAME: {timeframe}

Develop a complete brand plan with:
1. Executive Summary - concise overview
2. Market Analysis - current state and trends
3. Strategy - positioning and approach aligned with the strategic goals
4. Tactics - specific initiatives to execute that support the goals
5. KPIs - measurable success metrics aligned with the strategic goals
6. Budget Allocation - recommended spend by channel
7. Timeline - phased implementation plan

IMPORTANT: Tailor the entire plan to directly address the strategic goals provided above. Every tactic, KPI, and recommendation should support achieving these goals.

Make the plan actionable and specific to the pharmaceutical industry."""
