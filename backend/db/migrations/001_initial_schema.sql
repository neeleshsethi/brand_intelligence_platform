-- Initial schema for Pfizer AI Brand Planning
-- Schema: brand_planning
-- Tables: brands, insights, brand_plans

-- IMPORTANT: Enable UUID extension FIRST
-- Supabase typically has this enabled by default, but we ensure it's available
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Alternative: Use gen_random_uuid() which is built-in to Postgres 13+
-- This is Supabase's recommended approach and doesn't require uuid-ossp

-- Create dedicated schema
CREATE SCHEMA IF NOT EXISTS brand_planning;

-- Set search path to include our schema
SET search_path TO brand_planning, public;

-- Brands table
CREATE TABLE IF NOT EXISTS brand_planning.brands (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    therapeutic_area VARCHAR(255) NOT NULL,
    market_share DECIMAL(5, 2) CHECK (market_share >= 0 AND market_share <= 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insights table
CREATE TABLE IF NOT EXISTS brand_planning.insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand_id UUID NOT NULL REFERENCES brand_planning.brands(id) ON DELETE CASCADE,
    type VARCHAR(100) NOT NULL, -- e.g., 'market_research', 'competitor_analysis', 'messaging'
    content TEXT NOT NULL,
    confidence_score DECIMAL(3, 2) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    ai_reasoning TEXT,
    human_validated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Brand plans table
CREATE TABLE IF NOT EXISTS brand_planning.brand_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand_id UUID NOT NULL REFERENCES brand_planning.brands(id) ON DELETE CASCADE,
    plan_json JSONB NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(brand_id, version)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_insights_brand_id ON brand_planning.insights(brand_id);
CREATE INDEX IF NOT EXISTS idx_insights_type ON brand_planning.insights(type);
CREATE INDEX IF NOT EXISTS idx_insights_created_at ON brand_planning.insights(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_brand_plans_brand_id ON brand_planning.brand_plans(brand_id);
CREATE INDEX IF NOT EXISTS idx_brand_plans_version ON brand_planning.brand_plans(version DESC);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION brand_planning.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at
CREATE TRIGGER update_brands_updated_at BEFORE UPDATE ON brand_planning.brands
    FOR EACH ROW EXECUTE FUNCTION brand_planning.update_updated_at_column();

CREATE TRIGGER update_insights_updated_at BEFORE UPDATE ON brand_planning.insights
    FOR EACH ROW EXECUTE FUNCTION brand_planning.update_updated_at_column();

CREATE TRIGGER update_brand_plans_updated_at BEFORE UPDATE ON brand_planning.brand_plans
    FOR EACH ROW EXECUTE FUNCTION brand_planning.update_updated_at_column();

-- Add comments for documentation
COMMENT ON SCHEMA brand_planning IS 'Pfizer AI Brand Planning application schema';
COMMENT ON TABLE brand_planning.brands IS 'Pharmaceutical brands being tracked and analyzed';
COMMENT ON TABLE brand_planning.insights IS 'AI-generated insights about brands with confidence scores';
COMMENT ON TABLE brand_planning.brand_plans IS 'Brand planning strategies stored as JSON with versioning';

-- Grant permissions for Supabase API access
-- Grant usage on the schema
GRANT USAGE ON SCHEMA brand_planning TO anon;
GRANT USAGE ON SCHEMA brand_planning TO authenticated;

-- Grant permissions on all tables
-- anon: read, insert, delete (for API access and seeding)
GRANT SELECT, INSERT, DELETE ON ALL TABLES IN SCHEMA brand_planning TO anon;
-- authenticated: full permissions for write operations
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA brand_planning TO authenticated;

-- Grant permissions on sequences (needed for auto-increment IDs)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA brand_planning TO authenticated;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA brand_planning GRANT SELECT, INSERT, DELETE ON TABLES TO anon;
ALTER DEFAULT PRIVILEGES IN SCHEMA brand_planning GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA brand_planning GRANT USAGE, SELECT ON SEQUENCES TO authenticated;

-- Reset search path
RESET search_path;
