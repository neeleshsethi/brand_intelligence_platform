-- News Intelligence Schema
-- Adds news_articles and brand_news_relevance tables for real-time market intelligence
-- Schema: brand_planning

SET search_path TO brand_planning, public;

-- News articles table (many-to-many with brands)
CREATE TABLE IF NOT EXISTS brand_planning.news_articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    content TEXT,
    url TEXT UNIQUE NOT NULL,
    source VARCHAR(255) NOT NULL, -- e.g., 'FiercePharma', 'BioPharma Dive'
    published_at TIMESTAMP WITH TIME ZONE NOT NULL,
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Article classification
    article_type VARCHAR(100) NOT NULL, -- 'brand_specific', 'competitor', 'therapeutic_area', 'market_wide', 'regulatory'
    sentiment VARCHAR(50), -- 'positive', 'negative', 'neutral'

    -- Extracted entities (stored as arrays for quick filtering)
    mentioned_brands TEXT[] DEFAULT '{}', -- Array of brand names mentioned
    mentioned_companies TEXT[] DEFAULT '{}', -- Array of companies mentioned
    therapeutic_areas TEXT[] DEFAULT '{}', -- Array of therapeutic areas
    topics TEXT[] DEFAULT '{}', -- Array of topics: 'pricing', 'clinical_trial', 'fda_approval', 'tariff', etc.

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Junction table linking news to brands with relevance scores
CREATE TABLE IF NOT EXISTS brand_planning.brand_news_relevance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand_id UUID NOT NULL REFERENCES brand_planning.brands(id) ON DELETE CASCADE,
    news_article_id UUID NOT NULL REFERENCES brand_planning.news_articles(id) ON DELETE CASCADE,

    -- Relevance scoring
    relevance_score DECIMAL(3, 2) CHECK (relevance_score >= 0 AND relevance_score <= 1) NOT NULL,
    relevance_reason VARCHAR(255) NOT NULL, -- 'direct_mention', 'competitor_mention', 'therapeutic_area', 'market_context'
    priority VARCHAR(50) NOT NULL, -- 'high', 'medium', 'low'

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Ensure one article can only be linked once per brand
    UNIQUE(brand_id, news_article_id)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_news_articles_published_at ON brand_planning.news_articles(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_articles_fetched_at ON brand_planning.news_articles(fetched_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_articles_url ON brand_planning.news_articles(url);
CREATE INDEX IF NOT EXISTS idx_news_articles_type ON brand_planning.news_articles(article_type);
CREATE INDEX IF NOT EXISTS idx_news_articles_sentiment ON brand_planning.news_articles(sentiment);

-- GIN indexes for array columns (faster array searches)
CREATE INDEX IF NOT EXISTS idx_news_articles_mentioned_brands ON brand_planning.news_articles USING GIN(mentioned_brands);
CREATE INDEX IF NOT EXISTS idx_news_articles_therapeutic_areas ON brand_planning.news_articles USING GIN(therapeutic_areas);
CREATE INDEX IF NOT EXISTS idx_news_articles_topics ON brand_planning.news_articles USING GIN(topics);

-- Indexes for junction table
CREATE INDEX IF NOT EXISTS idx_brand_news_brand_id ON brand_planning.brand_news_relevance(brand_id);
CREATE INDEX IF NOT EXISTS idx_brand_news_article_id ON brand_planning.brand_news_relevance(news_article_id);
CREATE INDEX IF NOT EXISTS idx_brand_news_priority ON brand_planning.brand_news_relevance(priority);
CREATE INDEX IF NOT EXISTS idx_brand_news_relevance_score ON brand_planning.brand_news_relevance(relevance_score DESC);

-- Composite index for common query pattern
CREATE INDEX IF NOT EXISTS idx_brand_news_brand_priority ON brand_planning.brand_news_relevance(brand_id, priority, relevance_score DESC);

-- Add updated_at trigger for news_articles
CREATE TRIGGER update_news_articles_updated_at BEFORE UPDATE ON brand_planning.news_articles
    FOR EACH ROW EXECUTE FUNCTION brand_planning.update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE brand_planning.news_articles IS 'News articles from various pharmaceutical industry sources';
COMMENT ON TABLE brand_planning.brand_news_relevance IS 'Many-to-many relationship linking news articles to brands with relevance scores';
COMMENT ON COLUMN brand_planning.news_articles.article_type IS 'Classification: brand_specific, competitor, therapeutic_area, market_wide, regulatory';
COMMENT ON COLUMN brand_planning.news_articles.mentioned_brands IS 'Array of brand names mentioned in the article';
COMMENT ON COLUMN brand_planning.brand_news_relevance.relevance_score IS 'Score 0-1 indicating how relevant this article is to the specific brand';
COMMENT ON COLUMN brand_planning.brand_news_relevance.priority IS 'Priority level: high (requires immediate attention), medium, low';

-- Grant permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON brand_planning.news_articles TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON brand_planning.brand_news_relevance TO authenticated;
GRANT SELECT, INSERT, DELETE ON brand_planning.news_articles TO anon;
GRANT SELECT, INSERT, DELETE ON brand_planning.brand_news_relevance TO anon;

RESET search_path;
