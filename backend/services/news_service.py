"""News intelligence service using Tavily API."""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import re
from tavily import TavilyClient
from openai import OpenAI

from core.config import settings


class NewsService:
    """Service for fetching and processing pharmaceutical news."""

    def __init__(self):
        """Initialize Tavily and OpenAI clients."""
        self.tavily = TavilyClient(api_key=settings.TAVILY_API_KEY) if settings.TAVILY_API_KEY else None
        self.openai = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

    def fetch_brand_news(
        self,
        brand_name: str,
        therapeutic_area: str,
        days: int = 30,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch news specifically about this brand.

        Args:
            brand_name: Name of the pharmaceutical brand
            therapeutic_area: Therapeutic area (e.g., "anticoagulant")
            days: How many days back to search
            max_results: Maximum number of results

        Returns:
            List of article dictionaries with Tavily data
        """
        if not self.tavily:
            return []

        query = f'"{brand_name}" pharmaceutical news'

        try:
            response = self.tavily.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                days=days,
                include_domains=["fiercepharma.com", "biopharma-reporter.com", "endpts.com", "biopharmadive.com"]
            )

            articles = []
            for result in response.get("results", []):
                articles.append({
                    "title": result.get("title", ""),
                    "content": result.get("content", ""),
                    "url": result.get("url", ""),
                    "source": self._extract_source(result.get("url", "")),
                    "published_at": result.get("published_date", datetime.now().isoformat()),
                    "relevance_score": result.get("score", 0.5),
                    "article_type": "brand_specific",
                    "base_relevance": 1.0
                })

            return articles
        except Exception as e:
            print(f"Error fetching brand news: {str(e)}")
            return []

    def fetch_competitor_news(
        self,
        competitors: List[str],
        therapeutic_area: str,
        days: int = 30,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch news about competitor brands.

        Args:
            competitors: List of competitor brand names
            therapeutic_area: Therapeutic area
            days: How many days back to search
            max_results: Maximum number of results

        Returns:
            List of article dictionaries
        """
        if not self.tavily or not competitors:
            return []

        # Build query with competitor names
        competitor_query = " OR ".join([f'"{comp}"' for comp in competitors[:3]])  # Limit to top 3
        query = f"({competitor_query}) {therapeutic_area} pharmaceutical"

        try:
            response = self.tavily.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                days=days
            )

            articles = []
            for result in response.get("results", []):
                articles.append({
                    "title": result.get("title", ""),
                    "content": result.get("content", ""),
                    "url": result.get("url", ""),
                    "source": self._extract_source(result.get("url", "")),
                    "published_at": result.get("published_date", datetime.now().isoformat()),
                    "relevance_score": result.get("score", 0.5),
                    "article_type": "competitor",
                    "base_relevance": 0.8
                })

            return articles
        except Exception as e:
            print(f"Error fetching competitor news: {str(e)}")
            return []

    def fetch_therapeutic_area_news(
        self,
        therapeutic_area: str,
        days: int = 30,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch broader therapeutic area news.

        Args:
            therapeutic_area: Therapeutic area (e.g., "anticoagulant")
            days: How many days back to search
            max_results: Maximum number of results

        Returns:
            List of article dictionaries
        """
        if not self.tavily:
            return []

        query = f"{therapeutic_area} market pharmaceutical industry news"

        try:
            response = self.tavily.search(
                query=query,
                search_depth="basic",
                max_results=max_results,
                days=days
            )

            articles = []
            for result in response.get("results", []):
                articles.append({
                    "title": result.get("title", ""),
                    "content": result.get("content", ""),
                    "url": result.get("url", ""),
                    "source": self._extract_source(result.get("url", "")),
                    "published_at": result.get("published_date", datetime.now().isoformat()),
                    "relevance_score": result.get("score", 0.5),
                    "article_type": "therapeutic_area",
                    "base_relevance": 0.6
                })

            return articles
        except Exception as e:
            print(f"Error fetching therapeutic area news: {str(e)}")
            return []

    def fetch_market_wide_news(
        self,
        days: int = 30,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Fetch market-wide pharmaceutical industry news.

        Args:
            days: How many days back to search
            max_results: Maximum number of results

        Returns:
            List of article dictionaries
        """
        if not self.tavily:
            return []

        query = "pharmaceutical industry FDA regulation pricing policy drug approval"

        try:
            response = self.tavily.search(
                query=query,
                search_depth="basic",
                max_results=max_results,
                days=days
            )

            articles = []
            for result in response.get("results", []):
                articles.append({
                    "title": result.get("title", ""),
                    "content": result.get("content", ""),
                    "url": result.get("url", ""),
                    "source": self._extract_source(result.get("url", "")),
                    "published_at": result.get("published_date", datetime.now().isoformat()),
                    "relevance_score": result.get("score", 0.5),
                    "article_type": "market_wide",
                    "base_relevance": 0.4
                })

            return articles
        except Exception as e:
            print(f"Error fetching market-wide news: {str(e)}")
            return []

    def fetch_comprehensive_news(
        self,
        brand_name: str,
        therapeutic_area: str,
        competitors: Optional[List[str]] = None,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Fetch all types of news in one call.

        Args:
            brand_name: Primary brand name
            therapeutic_area: Therapeutic area
            competitors: List of competitor names
            days: How many days back

        Returns:
            Combined list of articles from all tiers
        """
        all_articles = []

        # Tier 1: Brand-specific (most important)
        brand_articles = self.fetch_brand_news(brand_name, therapeutic_area, days, max_results=10)
        all_articles.extend(brand_articles)

        # Tier 2: Competitor news
        if competitors:
            competitor_articles = self.fetch_competitor_news(competitors, therapeutic_area, days, max_results=10)
            all_articles.extend(competitor_articles)

        # Tier 3: Therapeutic area
        therapeutic_articles = self.fetch_therapeutic_area_news(therapeutic_area, days, max_results=10)
        all_articles.extend(therapeutic_articles)

        # Tier 4: Market-wide
        market_articles = self.fetch_market_wide_news(days, max_results=5)
        all_articles.extend(market_articles)

        # Deduplicate by URL
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article["url"] not in seen_urls:
                seen_urls.add(article["url"])
                unique_articles.append(article)

        return unique_articles

    def analyze_sentiment(self, article_text: str) -> str:
        """
        Analyze sentiment of article using OpenAI.

        Args:
            article_text: Article content to analyze

        Returns:
            Sentiment: 'positive', 'negative', or 'neutral'
        """
        if not self.openai:
            return "neutral"

        try:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Classify the sentiment of this pharmaceutical news article as positive, negative, or neutral from a business perspective. Respond with only one word."},
                    {"role": "user", "content": f"Title and content: {article_text[:500]}"}
                ],
                temperature=0,
                max_tokens=10
            )

            sentiment = response.choices[0].message.content.strip().lower()
            if sentiment in ["positive", "negative", "neutral"]:
                return sentiment
            return "neutral"
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            return "neutral"

    def extract_entities(self, article_text: str) -> Dict[str, List[str]]:
        """
        Extract entities (brands, companies, topics) from article.

        Args:
            article_text: Article content

        Returns:
            Dictionary with mentioned_brands, mentioned_companies, topics
        """
        # Simple regex-based extraction (could be enhanced with NER)
        brands_pattern = r'\b(Eliquis|Xarelto|Pradaxa|Paxlovid|Lagevrio|apixaban|rivaroxaban|dabigatran|nirmatrelvir)\b'
        companies_pattern = r'\b(Pfizer|Bristol Myers Squibb|Johnson & Johnson|Bayer|Merck|Boehringer Ingelheim|BMS|J&J)\b'
        topics_pattern = r'\b(pricing|price|approval|FDA|clinical trial|study|generic|patent|market share|revenue|sales|tariff|Medicare)\b'

        brands = list(set(re.findall(brands_pattern, article_text, re.IGNORECASE)))
        companies = list(set(re.findall(companies_pattern, article_text, re.IGNORECASE)))
        topics = list(set(re.findall(topics_pattern, article_text, re.IGNORECASE)))

        return {
            "mentioned_brands": brands,
            "mentioned_companies": companies,
            "topics": [t.lower() for t in topics]
        }

    def _extract_source(self, url: str) -> str:
        """Extract source name from URL."""
        if "fiercepharma" in url:
            return "FiercePharma"
        elif "biopharma" in url or "biopharmadive" in url:
            return "BioPharma Dive"
        elif "endpts" in url or "endpoints" in url:
            return "Endpoints News"
        elif "biopharma-reporter" in url:
            return "BioPharma Reporter"
        elif "reuters" in url:
            return "Reuters"
        elif "politico" in url:
            return "Politico"
        else:
            # Extract domain name
            match = re.search(r'https?://(?:www\.)?([^/]+)', url)
            return match.group(1) if match else "Unknown"


# Singleton instance
news_service = NewsService()
