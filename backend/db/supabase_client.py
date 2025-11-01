from supabase import create_client, Client, ClientOptions
from core.config import settings


class SupabaseClient:
    """Supabase database client with schema support."""

    _instance: Client = None
    SCHEMA = "brand_planning"

    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client instance."""
        if cls._instance is None:
            cls._instance = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
        return cls._instance

    @classmethod
    def get_table(cls, table_name: str):
        """Get a table reference with schema."""
        client = cls.get_client()
        # Use the brand_planning schema for table queries
        return client.schema(cls.SCHEMA).table(table_name)


# Convenience function
def get_supabase() -> Client:
    """Get Supabase client instance."""
    return SupabaseClient.get_client()


# Convenience function for table access
def get_table(table_name: str):
    """Get a table reference with brand_planning schema."""
    return SupabaseClient.get_table(table_name)
