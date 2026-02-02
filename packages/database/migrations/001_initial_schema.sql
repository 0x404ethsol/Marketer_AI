-- MARKETER_AI Initial Database Schema
-- Run this in Supabase SQL Editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================
-- ORGANIZATIONS
-- ============================================
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    plan TEXT DEFAULT 'free' CHECK (plan IN ('free', 'starter', 'pro', 'enterprise')),
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- USERS
-- ============================================
CREATE TABLE users (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    organization_id UUID REFERENCES organizations(id),
    role TEXT DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- BRANDS
-- ============================================
CREATE TABLE brands (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) NOT NULL,
    name TEXT NOT NULL,

    -- Brand DNA (from discovery)
    description TEXT,
    problem_solved TEXT,
    unfair_advantage TEXT,

    -- Target Audience
    target_demographics JSONB DEFAULT '{}',
    target_psychographics JSONB DEFAULT '{}',
    pain_points TEXT[],

    -- Brand Personality
    personality_traits TEXT[] DEFAULT '{}',
    tone_of_voice TEXT,

    -- Visual Identity
    primary_color TEXT,
    secondary_color TEXT,
    accent_color TEXT,
    fonts JSONB DEFAULT '{}',

    -- Assets
    logo_url TEXT,
    brand_assets JSONB DEFAULT '[]',

    -- Positioning (April Dunford methodology)
    competitive_alternatives TEXT[],
    unique_attributes JSONB DEFAULT '[]',
    value_propositions JSONB DEFAULT '[]',
    best_fit_customers TEXT,
    market_category TEXT,

    -- ICP Scoring
    icp_criteria JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- CAMPAIGNS
-- ============================================
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    brand_id UUID REFERENCES brands(id) NOT NULL,
    organization_id UUID REFERENCES organizations(id) NOT NULL,

    name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'planning', 'active', 'paused', 'completed')),

    -- Campaign Strategy
    objective TEXT CHECK (objective IN ('awareness', 'traffic', 'conversions', 'leads', 'app_install')),
    target_platforms TEXT[] DEFAULT '{}',
    start_date DATE,
    end_date DATE,
    budget DECIMAL(10, 2),

    -- Psychology Strategy
    primary_trigger TEXT,
    hook_formula TEXT,
    emotional_journey JSONB DEFAULT '{}',
    mental_models_used TEXT[] DEFAULT '{}',

    -- Generated Content
    scripts JSONB DEFAULT '[]',
    hooks JSONB DEFAULT '[]',

    -- Metrics
    metrics JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- GENERATED VIDEOS
-- ============================================
CREATE TABLE generated_videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID REFERENCES campaigns(id),
    organization_id UUID REFERENCES organizations(id) NOT NULL,

    name TEXT NOT NULL,
    platform TEXT NOT NULL CHECK (platform IN ('tiktok', 'instagram_reels', 'youtube_shorts', 'youtube', 'linkedin')),

    -- Video Specs
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    duration_seconds DECIMAL(10, 2),
    fps INTEGER DEFAULT 30,

    -- Source
    remotion_code TEXT,
    script TEXT,
    word_timings JSONB DEFAULT '[]',

    -- Output
    video_url TEXT,
    thumbnail_url TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),

    -- Metadata
    generation_metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- AGENT CREWS
-- ============================================
CREATE TABLE agent_crews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) NOT NULL,

    crew_type TEXT NOT NULL CHECK (crew_type IN ('content', 'video', 'leadgen', 'campaign', 'analytics')),
    name TEXT NOT NULL,

    -- Configuration
    agents JSONB DEFAULT '[]',
    skills_loaded TEXT[] DEFAULT '{}',
    config JSONB DEFAULT '{}',

    -- Status
    status TEXT DEFAULT 'idle' CHECK (status IN ('idle', 'running', 'paused', 'completed', 'error')),
    current_task TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- AGENT SESSIONS
-- ============================================
CREATE TABLE agent_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crew_id UUID REFERENCES agent_crews(id) NOT NULL,
    user_id UUID REFERENCES users(id) NOT NULL,

    messages JSONB DEFAULT '[]',
    context JSONB DEFAULT '{}',

    -- Outputs
    generated_outputs JSONB DEFAULT '[]',

    -- Metrics
    tokens_used INTEGER DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- LEADS
-- ============================================
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) NOT NULL,
    campaign_id UUID REFERENCES campaigns(id),

    -- Contact Info
    email TEXT,
    phone TEXT,
    first_name TEXT,
    last_name TEXT,

    -- Company Info
    company_name TEXT,
    company_size TEXT,
    industry TEXT,
    job_title TEXT,

    -- Qualification (BANT/MEDDIC)
    bant_score JSONB DEFAULT '{}',
    meddic_score JSONB DEFAULT '{}',
    icp_fit TEXT CHECK (icp_fit IN ('A', 'B', 'C', 'D')),
    lead_score INTEGER DEFAULT 0,

    -- Pipeline
    stage TEXT DEFAULT 'new' CHECK (stage IN ('new', 'qualified', 'proposal', 'negotiation', 'won', 'lost')),
    deal_value DECIMAL(12, 2),
    probability INTEGER DEFAULT 0,
    expected_close_date DATE,

    -- Source
    source TEXT,
    utm_params JSONB DEFAULT '{}',

    -- Activity
    last_activity_at TIMESTAMPTZ,
    activities JSONB DEFAULT '[]',

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- SKILLS REGISTRY
-- ============================================
CREATE TABLE skills_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,
    slug TEXT UNIQUE NOT NULL,

    description TEXT,
    category TEXT,
    version TEXT,

    -- Content
    skill_content TEXT,
    references JSONB DEFAULT '[]',

    -- Usage
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMPTZ,

    -- Local path
    local_path TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- USAGE RECORDS (for billing)
-- ============================================
CREATE TABLE usage_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) NOT NULL,

    usage_type TEXT NOT NULL CHECK (usage_type IN ('agent_tokens', 'video_render', 'skill_execution', 'api_call')),
    quantity INTEGER NOT NULL,
    unit_cost DECIMAL(10, 6),

    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- INDEXES
-- ============================================
CREATE INDEX idx_campaigns_brand ON campaigns(brand_id);
CREATE INDEX idx_campaigns_org ON campaigns(organization_id);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_videos_campaign ON generated_videos(campaign_id);
CREATE INDEX idx_videos_status ON generated_videos(status);
CREATE INDEX idx_leads_org ON leads(organization_id);
CREATE INDEX idx_leads_stage ON leads(stage);
CREATE INDEX idx_leads_score ON leads(lead_score);
CREATE INDEX idx_leads_icp ON leads(icp_fit);
CREATE INDEX idx_sessions_crew ON agent_sessions(crew_id);
CREATE INDEX idx_usage_org ON usage_records(organization_id);
CREATE INDEX idx_usage_type ON usage_records(usage_type);

-- ============================================
-- ROW LEVEL SECURITY
-- ============================================
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE brands ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_videos ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_crews ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_records ENABLE ROW LEVEL SECURITY;

-- ============================================
-- RLS POLICIES
-- ============================================

-- Organizations: Users can view their own organization
CREATE POLICY "Users can view their organization" ON organizations
    FOR SELECT USING (id IN (SELECT organization_id FROM users WHERE id = auth.uid()));

-- Brands: Users can manage their org's brands
CREATE POLICY "Users can manage org brands" ON brands
    FOR ALL USING (organization_id IN (SELECT organization_id FROM users WHERE id = auth.uid()));

-- Campaigns: Users can manage their org's campaigns
CREATE POLICY "Users can manage org campaigns" ON campaigns
    FOR ALL USING (organization_id IN (SELECT organization_id FROM users WHERE id = auth.uid()));

-- Videos: Users can manage their org's videos
CREATE POLICY "Users can manage org videos" ON generated_videos
    FOR ALL USING (organization_id IN (SELECT organization_id FROM users WHERE id = auth.uid()));

-- Agent Crews: Users can manage their org's crews
CREATE POLICY "Users can manage org crews" ON agent_crews
    FOR ALL USING (organization_id IN (SELECT organization_id FROM users WHERE id = auth.uid()));

-- Agent Sessions: Users can view their own sessions
CREATE POLICY "Users can view own sessions" ON agent_sessions
    FOR ALL USING (user_id = auth.uid());

-- Leads: Users can manage their org's leads
CREATE POLICY "Users can manage org leads" ON leads
    FOR ALL USING (organization_id IN (SELECT organization_id FROM users WHERE id = auth.uid()));

-- Usage Records: Users can view their org's usage
CREATE POLICY "Users can view org usage" ON usage_records
    FOR SELECT USING (organization_id IN (SELECT organization_id FROM users WHERE id = auth.uid()));

-- ============================================
-- FUNCTIONS
-- ============================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to all tables with updated_at
CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_brands_updated_at BEFORE UPDATE ON brands FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_videos_updated_at BEFORE UPDATE ON generated_videos FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_crews_updated_at BEFORE UPDATE ON agent_crews FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON agent_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_leads_updated_at BEFORE UPDATE ON leads FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_skills_updated_at BEFORE UPDATE ON skills_registry FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
