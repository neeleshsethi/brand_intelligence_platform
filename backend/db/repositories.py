"""Database repositories for accessing data."""

from typing import List, Optional, Dict, Any
from db.supabase_client import get_table
from core.config import settings


# Mock data for DEMO/MOCK mode
# Note: This includes both Pfizer brands and key competitors for competitive analysis
MOCK_BRANDS = [
    # Pfizer Brands
    {
        "id": "b1a2c3d4-e5f6-7890-abcd-ef1234567890",
        "name": "Paxlovid",
        "company": "Pfizer",
        "therapeutic_area": "COVID-19 Antiviral",
        "market_share": 65.4,
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T10:00:00Z"
    },
    {
        "id": "d3c4e5f6-a7b8-9012-cdef-123456789012",
        "name": "Eliquis",
        "company": "Pfizer/Bristol Myers Squibb",
        "therapeutic_area": "Anticoagulant (Blood Thinner)",
        "market_share": 42.3,
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T10:00:00Z"
    },
    # Competitor Brands (for competitive analysis)
    {
        "id": "c2b3d4e5-f6a7-8901-bcde-f12345678901",
        "name": "Lagevrio",
        "company": "Merck",
        "therapeutic_area": "COVID-19 Antiviral",
        "market_share": 34.6,
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T10:00:00Z"
    },
    {
        "id": "e4d5f6a7-b8c9-0123-def1-234567890123",
        "name": "Xarelto",
        "company": "Johnson & Johnson/Bayer",
        "therapeutic_area": "Anticoagulant (Blood Thinner)",
        "market_share": 38.7,
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T10:00:00Z"
    }
]


class BrandRepository:
    """Repository for brand operations."""

    @staticmethod
    def get_all_brands() -> List[Dict[str, Any]]:
        """Get all brands."""
        if settings.MOCK_MODE:
            return MOCK_BRANDS
        response = get_table("brands").select("*").order("name").execute()
        return response.data

    @staticmethod
    def get_brand_by_id(brand_id: str) -> Optional[Dict[str, Any]]:
        """Get brand by ID."""
        if settings.MOCK_MODE:
            for brand in MOCK_BRANDS:
                if brand["id"] == brand_id:
                    return brand
            return None
        response = get_table("brands").select("*").eq("id", brand_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def get_brand_insights(brand_id: str) -> List[Dict[str, Any]]:
        """Get all insights for a brand."""
        response = (
            get_table("insights")
            .select("*")
            .eq("brand_id", brand_id)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data

    @staticmethod
    def get_brand_plans(brand_id: str) -> List[Dict[str, Any]]:
        """Get all plans for a brand."""
        response = (
            get_table("brand_plans")
            .select("*")
            .eq("brand_id", brand_id)
            .order("version", desc=True)
            .execute()
        )
        return response.data

    @staticmethod
    def create_insight(insight_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new insight."""
        response = get_table("insights").insert(insight_data).execute()
        return response.data[0]

    @staticmethod
    def create_brand_plan(plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new brand plan."""
        response = get_table("brand_plans").insert(plan_data).execute()
        return response.data[0]
