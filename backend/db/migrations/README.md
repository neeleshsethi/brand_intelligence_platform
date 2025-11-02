# Database Migrations

## Running Migrations in Supabase

### Step 1: Access Supabase SQL Editor
1. Go to your Supabase project dashboard
2. Click on **SQL Editor** in the left sidebar
3. Click **+ New query**

### Step 2: Run Migration 002 (News Intelligence)

Copy and paste the entire contents of `002_news_intelligence.sql` into the SQL editor and click **Run**.

This will create:
- `news_articles` table - Stores news articles with extracted entities
- `brand_news_relevance` table - Links articles to brands (many-to-many)
- All necessary indexes for fast queries
- Proper permissions for API access

### Verify Migration Success

Run this query to verify tables were created:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'brand_planning'
ORDER BY table_name;
```

You should see:
- brands
- brand_news_relevance ← NEW
- brand_plans
- insights
- news_articles ← NEW

## Migration Details

### news_articles Table Schema
- Stores articles from multiple sources (FiercePharma, BioPharma Dive, etc.)
- Includes extracted entities (brands, companies, therapeutic areas, topics)
- Uses array columns for efficient filtering
- Unique constraint on URL prevents duplicates

### brand_news_relevance Table Schema
- Junction table for many-to-many relationship
- Each article can link to multiple brands
- Each link has its own relevance score (0-1)
- Priority levels: high, medium, low
- Tracks WHY an article is relevant (direct_mention, competitor_mention, etc.)

## Next Steps After Migration

1. Tables are ready ✅
2. Next: Add Tavily API integration
3. Next: Build news fetching service
4. Next: Create API endpoints

## Rollback (if needed)

To rollback this migration:

```sql
DROP TABLE IF EXISTS brand_planning.brand_news_relevance CASCADE;
DROP TABLE IF EXISTS brand_planning.news_articles CASCADE;
```
