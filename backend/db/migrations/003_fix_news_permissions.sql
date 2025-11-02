-- Fix permissions for news tables
-- Run this in Supabase SQL Editor

-- Grant permissions to authenticated and anon roles
GRANT SELECT, INSERT, UPDATE ON brand_planning.news_articles TO anon, authenticated;
GRANT SELECT, INSERT, UPDATE ON brand_planning.brand_news_relevance TO anon, authenticated;

-- Grant usage on sequences if any
GRANT USAGE ON ALL SEQUENCES IN SCHEMA brand_planning TO anon, authenticated;

-- Enable RLS but create permissive policies
ALTER TABLE brand_planning.news_articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE brand_planning.brand_news_relevance ENABLE ROW LEVEL SECURITY;

-- Create policies that allow all operations (for demo purposes)
-- In production, you'd want more restrictive policies

-- Policy for news_articles
DROP POLICY IF EXISTS "Allow all operations on news_articles" ON brand_planning.news_articles;
CREATE POLICY "Allow all operations on news_articles"
ON brand_planning.news_articles
FOR ALL
USING (true)
WITH CHECK (true);

-- Policy for brand_news_relevance
DROP POLICY IF EXISTS "Allow all operations on brand_news_relevance" ON brand_planning.brand_news_relevance;
CREATE POLICY "Allow all operations on brand_news_relevance"
ON brand_planning.brand_news_relevance
FOR ALL
USING (true)
WITH CHECK (true);
