"""Main API routes for the application."""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime
import asyncio
import json

from db.repositories import BrandRepository, NewsRepository
from agents.analyzer_agent import analyzer_agent
from agents.strategy_agent import strategy_agent
from agents.brand_plan_agent import brand_plan_agent
from agents.scenario_agent import scenario_agent
from agents.validator_agent import validator_agent
from services.news_service import news_service

from agents.models.outputs import (
    BrandData, CompetitorData, AnalyzerInput,
    StrategyInput, BrandPlanInput, ScenarioInput, ValidatorInput
)
from core.config import settings

router = APIRouter()


# Request/Response Models
class AnalyzeRequest(BaseModel):
    """Request for analysis endpoint."""
    include_competitors: bool = True


class GeneratePlanRequest(BaseModel):
    """Request for plan generation."""
    budget: Optional[float] = None
    timeframe: str = "12 months"
    strategic_goals: Optional[str] = None


class ScenarioRequest(BaseModel):
    """Request for scenario analysis."""
    brand_id: Optional[str] = None
    brand_name: Optional[str] = None
    scenario_question: str
    current_context: Optional[str] = None


class ValidateRequest(BaseModel):
    """Request for content validation."""
    content_type: str
    content: str
    validation_criteria: Optional[List[str]] = None


# Demo mode cached responses
DEMO_CACHE: Dict[str, Any] = {}


def get_demo_response(cache_key: str, generator_func):
    """Get cached demo response or generate and cache it."""
    if settings.DEMO_MODE:
        if cache_key not in DEMO_CACHE:
            DEMO_CACHE[cache_key] = generator_func()
        return DEMO_CACHE[cache_key]
    return None


@router.get("/brands")
async def list_brands() -> List[Dict[str, Any]]:
    """
    List all brands in the system.

    Returns basic info for all pharmaceutical brands being tracked.
    """
    try:
        brands = BrandRepository.get_all_brands()
        return brands
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch brands: {str(e)}")


@router.post("/analyze/{brand_id}")
async def analyze_brand(brand_id: str, request: AnalyzeRequest = AnalyzeRequest()) -> Dict[str, Any]:
    """
    Run AnalyzerAgent + StrategyAgent for a brand.

    Returns:
    - Market analysis (insights, gaps, opportunities)
    - SWOT analysis
    - Competitive positioning
    - Strategic recommendations
    """
    try:
        # Check demo mode cache
        cache_key = f"analyze_{brand_id}"
        demo_response = get_demo_response(cache_key, lambda: None)
        if demo_response:
            return demo_response

        # Fetch brand from database
        brand = BrandRepository.get_brand_by_id(brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail=f"Brand {brand_id} not found")

        # Get competitors if requested
        competitors = []
        if request.include_competitors:
            all_brands = BrandRepository.get_all_brands()
            competitors = [
                CompetitorData(
                    name=b["name"],
                    company=b["company"],
                    market_share=b.get("market_share")
                )
                for b in all_brands
                if b["id"] != brand_id and b["therapeutic_area"] == brand["therapeutic_area"]
            ]

        # Create brand data
        brand_data = BrandData(
            brand_id=brand["id"],
            name=brand["name"],
            company=brand["company"],
            therapeutic_area=brand["therapeutic_area"],
            market_share=brand.get("market_share")
        )

        # Fetch recent news for context
        news_articles = []
        try:
            from services.news_service import news_service
            from core.config import settings

            # Only fetch if TAVILY_API_KEY is set
            if settings.TAVILY_API_KEY:
                # Get competitor names for comprehensive search
                competitor_names = [c.name for c in competitors[:3]]

                # Fetch comprehensive news
                all_articles = news_service.fetch_comprehensive_news(
                    brand_name=brand["name"],
                    therapeutic_area=brand["therapeutic_area"],
                    competitors=competitor_names,
                    days=30
                )

                # Get existing news from database
                existing_news = NewsRepository.get_brand_news(brand_id, days=30)
                existing_urls = {n.get("news_articles", {}).get("url") for n in existing_news}

                # Process and store new articles
                for article in all_articles[:15]:  # Limit to top 15
                    if article["url"] not in existing_urls:
                        # Analyze sentiment
                        article["sentiment"] = news_service.analyze_sentiment(
                            f"{article['title']} {article.get('content', '')[:500]}"
                        )

                        # Extract entities
                        entities = news_service.extract_entities(
                            article["title"],
                            article.get("content", "")
                        )

                        # Store article
                        article_db = {
                            "title": article["title"],
                            "content": article.get("content", ""),
                            "url": article["url"],
                            "source": article["source"],
                            "published_at": article["published_at"],
                            "article_type": article["article_type"],
                            "sentiment": article["sentiment"],
                            "mentioned_brands": entities["mentioned_brands"],
                            "mentioned_companies": entities["mentioned_companies"],
                            "therapeutic_areas": entities["therapeutic_areas"],
                            "topics": entities["topics"]
                        }
                        stored_article = NewsRepository.create_news_article(article_db)

                        # Link to brand
                        link_data = {
                            "brand_id": brand_id,
                            "news_article_id": stored_article["id"],
                            "relevance_score": article["relevance_score"],
                            "relevance_reason": article["relevance_reason"],
                            "priority": article["priority"]
                        }
                        NewsRepository.create_brand_news_link(link_data)

                    # Add to context list
                    news_articles.append(article)

        except Exception as e:
            # If news fetching fails, continue without it
            print(f"Warning: Failed to fetch news: {e}")
            news_articles = []

        # Run Analyzer with news context
        analyzer_input = AnalyzerInput(
            brand=brand_data,
            competitors=competitors
        )
        analyzer_result = await analyzer_agent.analyze(analyzer_input, news_articles=news_articles)

        # Run Strategy
        strategy_input = StrategyInput(
            brand=brand_data,
            analyzer_output=json.dumps(analyzer_result.model_dump())
        )
        strategy_result = await strategy_agent.strategize(strategy_input)

        # Combine results
        result = {
            "brand": brand,
            "analysis": analyzer_result.model_dump(),
            "strategy": strategy_result.model_dump(),
            "timestamp": "generated_now"
        }

        # Persist insights to database
        saved_insight_ids = []
        for insight in analyzer_result.key_insights:
            insight_data = {
                "brand_id": brand_id,
                "type": insight.category,
                "content": insight.description,
                "confidence_score": 0.85,  # Default confidence for analyzer insights
                "ai_reasoning": f"Generated from competitive analysis. Impact level: {insight.impact}",
                "human_validated": False
            }
            saved_insight = BrandRepository.create_insight(insight_data)
            saved_insight_ids.append(saved_insight["id"])

        result["saved_insight_ids"] = saved_insight_ids

        # Cache for demo mode
        if settings.DEMO_MODE:
            DEMO_CACHE[cache_key] = result

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/generate-plan/{brand_id}")
async def generate_brand_plan(
    brand_id: str,
    request: GeneratePlanRequest = GeneratePlanRequest()
) -> Dict[str, Any]:
    """
    Generate complete brand plan using BrandPlanAgent.

    Returns comprehensive brand plan with:
    - Executive summary
    - Market analysis
    - Strategy and tactics
    - KPIs and metrics
    - Budget allocation
    - Timeline
    """
    try:
        # Check demo mode cache
        cache_key = f"plan_{brand_id}_{request.budget}_{request.timeframe}"
        demo_response = get_demo_response(cache_key, lambda: None)
        if demo_response:
            return demo_response

        # Fetch brand from database
        brand = BrandRepository.get_brand_by_id(brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail=f"Brand {brand_id} not found")

        # Create brand data
        brand_data = BrandData(
            brand_id=brand["id"],
            name=brand["name"],
            company=brand["company"],
            therapeutic_area=brand["therapeutic_area"],
            market_share=brand.get("market_share")
        )

        # Run BrandPlanAgent
        plan_input = BrandPlanInput(
            brand=brand_data,
            budget=request.budget,
            timeframe=request.timeframe,
            strategic_goals=request.strategic_goals
        )
        plan_result = await brand_plan_agent.create_plan(plan_input)

        # Format result
        result = {
            "brand": brand,
            "plan": plan_result.model_dump(),
            "metadata": {
                "budget": request.budget,
                "timeframe": request.timeframe,
                "timestamp": "generated_now"
            }
        }

        # Save to database with auto-incrementing version
        existing_plans = BrandRepository.get_brand_plans(brand_id)
        next_version = max([p.get("version", 0) for p in existing_plans], default=0) + 1

        plan_data = {
            "brand_id": brand_id,
            "plan_json": plan_result.model_dump(),
            "version": next_version
        }
        saved_plan = BrandRepository.create_brand_plan(plan_data)
        result["saved_plan_id"] = saved_plan["id"]

        # Cache for demo mode
        if settings.DEMO_MODE:
            DEMO_CACHE[cache_key] = result

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan generation failed: {str(e)}")


@router.post("/scenario")
async def analyze_scenario(request: ScenarioRequest) -> Dict[str, Any]:
    """
    Run ScenarioAgent to analyze what-if scenarios.

    Returns:
    - Impact analysis
    - Risk level assessment
    - 3 defensive tactics
    - Recommended immediate action
    """
    try:
        # Check demo mode cache
        cache_key = f"scenario_{request.scenario_question[:50]}"
        demo_response = get_demo_response(cache_key, lambda: None)
        if demo_response:
            return demo_response

        # Get brand data
        brand_data = None
        if request.brand_id:
            brand = BrandRepository.get_brand_by_id(request.brand_id)
            if brand:
                brand_data = BrandData(
                    brand_id=brand["id"],
                    name=brand["name"],
                    company=brand["company"],
                    therapeutic_area=brand["therapeutic_area"],
                    market_share=brand.get("market_share")
                )
            else:
                raise HTTPException(status_code=404, detail=f"Brand {request.brand_id} not found")
        elif request.brand_name:
            # Use provided brand name
            brand_data = BrandData(
                name=request.brand_name,
                company="Unknown",
                therapeutic_area="Unknown"
            )
        else:
            raise HTTPException(status_code=400, detail="Either brand_id or brand_name required")

        if not brand_data:
            raise HTTPException(status_code=400, detail="Brand data could not be loaded")

        # Run ScenarioAgent
        scenario_input = ScenarioInput(
            brand=brand_data,
            scenario_question=request.scenario_question,
            current_context=request.current_context
        )
        scenario_result = await scenario_agent.analyze_scenario(scenario_input)

        # Format result
        result = {
            "scenario": scenario_result.model_dump(),
            "timestamp": "generated_now"
        }

        # Cache for demo mode
        if settings.DEMO_MODE:
            DEMO_CACHE[cache_key] = result

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scenario analysis failed: {str(e)}")


@router.post("/validate")
async def validate_content(request: ValidateRequest) -> Dict[str, Any]:
    """
    Run ValidatorAgent to validate AI-generated content.

    Returns:
    - Confidence score (0-1)
    - Explanation
    - Strengths and weaknesses
    - Suggested edits
    - Validation status
    """
    try:
        # Check demo mode cache
        cache_key = f"validate_{request.content_type}_{request.content[:50]}"
        demo_response = get_demo_response(cache_key, lambda: None)
        if demo_response:
            return demo_response

        # Run ValidatorAgent
        validator_input = ValidatorInput(
            content_type=request.content_type,
            content=request.content,
            validation_criteria=request.validation_criteria
        )
        validation_result = await validator_agent.validate(validator_input)

        # Format result
        result = {
            "validation": validation_result.model_dump(),
            "timestamp": "generated_now"
        }

        # Cache for demo mode
        if settings.DEMO_MODE:
            DEMO_CACHE[cache_key] = result

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@router.get("/insights")
async def get_insights(
    brand_id: Optional[str] = None,
    validated: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """
    Get insights, optionally filtered by brand and validation status.

    Query params:
    - brand_id: Filter by brand
    - validated: Filter by human_validated status
    """
    try:
        if brand_id:
            insights = BrandRepository.get_brand_insights(brand_id)
        else:
            # For now, require brand_id (could expand to all insights later)
            raise HTTPException(status_code=400, detail="brand_id parameter required")

        # Filter by validation status if specified
        if validated is not None:
            insights = [i for i in insights if i.get("human_validated") == validated]

        return insights

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch insights: {str(e)}")


@router.patch("/insights/{insight_id}/validate")
async def validate_insight(insight_id: str) -> Dict[str, Any]:
    """
    Mark an insight as human-validated.
    """
    try:
        # Update insight validation status
        updated_insight = BrandRepository.validate_insight(insight_id)

        if not updated_insight:
            raise HTTPException(status_code=404, detail=f"Insight {insight_id} not found")

        return {
            "insight": updated_insight,
            "message": "Insight validated successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to validate insight: {str(e)}")


@router.get("/news/{brand_id}")
async def get_brand_news(
    brand_id: str,
    refresh: bool = False,
    limit: int = 15
) -> Dict[str, Any]:
    """
    Get news articles relevant to a brand.

    Query params:
    - refresh: Force fetch fresh news from Tavily
    - limit: Maximum number of articles to return
    """
    try:
        # Check if refresh needed or no cached news
        if refresh or True:  # Always fetch for now (can add caching logic later)
            # Fetch brand details
            brand = BrandRepository.get_brand_by_id(brand_id)
            if not brand:
                raise HTTPException(status_code=404, detail=f"Brand {brand_id} not found")

            # Get competitors
            all_brands = BrandRepository.get_all_brands()
            competitors = [
                b["name"] for b in all_brands
                if b["id"] != brand_id and b["therapeutic_area"] == brand["therapeutic_area"]
            ]

            # Fetch comprehensive news
            articles = news_service.fetch_comprehensive_news(
                brand_name=brand["name"],
                therapeutic_area=brand["therapeutic_area"],
                competitors=competitors[:3],  # Top 3 competitors
                days=30
            )

            # Process and store each article
            stored_articles = []
            for article in articles:
                # Analyze sentiment
                article["sentiment"] = news_service.analyze_sentiment(
                    f"{article['title']} {article['content'][:300]}"
                )

                # Extract entities
                entities = news_service.extract_entities(
                    f"{article['title']} {article['content']}"
                )
                article.update(entities)

                # Determine therapeutic areas
                if brand["therapeutic_area"].lower() in article["content"].lower():
                    article["therapeutic_areas"] = [brand["therapeutic_area"]]
                else:
                    article["therapeutic_areas"] = []

                # Store article
                article_db = {
                    "title": article["title"],
                    "content": article["content"],
                    "url": article["url"],
                    "source": article["source"],
                    "published_at": article["published_at"],
                    "article_type": article["article_type"],
                    "sentiment": article["sentiment"],
                    "mentioned_brands": article.get("mentioned_brands", []),
                    "mentioned_companies": article.get("mentioned_companies", []),
                    "therapeutic_areas": article.get("therapeutic_areas", []),
                    "topics": article.get("topics", [])
                }

                stored_article = NewsRepository.create_news_article(article_db)

                # Calculate priority
                priority = "high" if article["article_type"] in ["brand_specific", "competitor"] else "medium"
                if article["article_type"] == "market_wide":
                    priority = "low"

                # Link to brand
                link_data = {
                    "brand_id": brand_id,
                    "news_article_id": stored_article["id"],
                    "relevance_score": article.get("base_relevance", 0.5),
                    "relevance_reason": article["article_type"],
                    "priority": priority
                }
                NewsRepository.create_brand_news_link(link_data)

                # Also link mentioned brands
                for mentioned_brand in article.get("mentioned_brands", []):
                    other_brands = [b for b in all_brands if b["name"].lower() == mentioned_brand.lower()]
                    for other_brand in other_brands:
                        if other_brand["id"] != brand_id:
                            other_link = {
                                "brand_id": other_brand["id"],
                                "news_article_id": stored_article["id"],
                                "relevance_score": 0.7,
                                "relevance_reason": "mentioned_in_article",
                                "priority": "medium"
                            }
                            NewsRepository.create_brand_news_link(other_link)

                stored_articles.append({**stored_article, "priority": priority, "relevance_score": article.get("base_relevance", 0.5)})

        # Fetch stored news for brand
        news_data = NewsRepository.get_brand_news(brand_id, limit=limit)

        # Format response
        articles_list = []
        for item in news_data:
            news_article = item.get("news_articles", {})
            articles_list.append({
                "id": news_article.get("id"),
                "title": news_article.get("title"),
                "content": news_article.get("content"),
                "url": news_article.get("url"),
                "source": news_article.get("source"),
                "published_at": news_article.get("published_at"),
                "article_type": news_article.get("article_type"),
                "sentiment": news_article.get("sentiment"),
                "topics": news_article.get("topics", []),
                "relevance_score": item.get("relevance_score"),
                "priority": item.get("priority")
            })

        high_priority_count = len([a for a in articles_list if a["priority"] == "high"])

        return {
            "brand_id": brand_id,
            "articles": articles_list[:limit],
            "total_count": len(articles_list),
            "high_priority_count": high_priority_count,
            "last_updated": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")


# WebSocket for real-time updates
class ConnectionManager:
    """Manage WebSocket connections."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


@router.websocket("/ws/progress")
async def websocket_progress(websocket: WebSocket):
    """
    WebSocket endpoint for real-time processing updates.

    Simulates progress updates during agent processing.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Wait for client message
            data = await websocket.receive_text()
            message = json.loads(data)

            # Simulate processing steps
            if message.get("action") == "analyze":
                steps = [
                    {"step": "Fetching brand data", "progress": 10},
                    {"step": "Analyzing market landscape", "progress": 30},
                    {"step": "Evaluating competitors", "progress": 50},
                    {"step": "Generating insights", "progress": 70},
                    {"step": "Developing strategy", "progress": 90},
                    {"step": "Complete", "progress": 100}
                ]

                for step_data in steps:
                    await manager.send_message(step_data, websocket)
                    await asyncio.sleep(0.3 if settings.DEMO_MODE else 0.8)

            elif message.get("action") == "generate_plan":
                steps = [
                    {"step": "Loading brand context", "progress": 15},
                    {"step": "Analyzing market position", "progress": 30},
                    {"step": "Developing strategic framework", "progress": 50},
                    {"step": "Creating tactical initiatives", "progress": 70},
                    {"step": "Calculating KPIs and budget", "progress": 85},
                    {"step": "Complete", "progress": 100}
                ]

                for step_data in steps:
                    await manager.send_message(step_data, websocket)
                    await asyncio.sleep(0.3 if settings.DEMO_MODE else 1.0)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket)
