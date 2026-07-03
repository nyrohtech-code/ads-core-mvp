-- ============================================================================
-- ADS CORE MVP - Supabase Schema
-- ============================================================================

-- Criar extensões
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================================================
-- 1. CLIENTS (Clientes)
-- ============================================================================

CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    niche TEXT,
    timezone TEXT DEFAULT 'America/Sao_Paulo',
    budget_monthly DECIMAL(10, 2),
    objective TEXT, -- 'leads', 'sales', 'awareness'
    status TEXT DEFAULT 'active', -- 'active', 'paused', 'churn'
    account_manager_id UUID,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE clients ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- 2. AD_ACCOUNTS (Contas de Anúncio)
-- ============================================================================

CREATE TABLE ad_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id),
    platform TEXT NOT NULL, -- 'meta', 'google', 'tiktok'
    account_id TEXT NOT NULL,
    access_token TEXT, -- Encrypted in production
    refresh_token TEXT,
    status TEXT DEFAULT 'active',
    last_synced TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(platform, account_id)
);

ALTER TABLE ad_accounts ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- 3. CAMPAIGNS (Campanhas)
-- ============================================================================

CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id),
    ad_account_id UUID NOT NULL REFERENCES ad_accounts(id),
    platform TEXT NOT NULL,
    platform_campaign_id TEXT,
    name TEXT NOT NULL,
    objective TEXT, -- 'SALES', 'LEADS', 'AWARENESS'
    status TEXT DEFAULT 'ACTIVE', -- 'ACTIVE', 'PAUSED', 'ARCHIVED'
    budget_daily DECIMAL(10, 2),
    budget_monthly DECIMAL(10, 2),
    kpi_target_roas DECIMAL(5, 2),
    kpi_target_cpa DECIMAL(10, 2),
    kpi_margin_error DECIMAL(5, 2) DEFAULT 10,
    audience_json JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_performance_sync TIMESTAMP
);

ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
CREATE INDEX idx_campaigns_client_id ON campaigns(client_id);
CREATE INDEX idx_campaigns_platform ON campaigns(platform);

-- ============================================================================
-- 4. CREATIVES (Criativos/Anúncios)
-- ============================================================================

CREATE TABLE creatives (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID NOT NULL REFERENCES campaigns(id),
    type TEXT, -- 'image', 'video', 'carousel'
    hook TEXT,
    script TEXT,
    copy TEXT,
    cta TEXT,
    asset_url TEXT,
    performance_score DECIMAL(3, 2),
    status TEXT DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE creatives ENABLE ROW LEVEL SECURITY;
CREATE INDEX idx_creatives_campaign_id ON creatives(campaign_id);

-- ============================================================================
-- 5. PERFORMANCE_LOGS (Histórico de Performance)
-- ============================================================================

CREATE TABLE performance_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID NOT NULL REFERENCES campaigns(id),
    date DATE NOT NULL,
    spend DECIMAL(10, 2),
    impressions BIGINT,
    clicks BIGINT,
    conversions BIGINT,
    purchases BIGINT,
    revenue DECIMAL(12, 2),
    ctr DECIMAL(5, 2),
    cpc DECIMAL(10, 2),
    cpa DECIMAL(10, 2),
    roas DECIMAL(5, 2),
    conversion_rate DECIMAL(5, 2),
    synced_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(campaign_id, date)
);

ALTER TABLE performance_logs ENABLE ROW LEVEL SECURITY;
CREATE INDEX idx_performance_logs_campaign_id ON performance_logs(campaign_id);
CREATE INDEX idx_performance_logs_date ON performance_logs(date);

-- ============================================================================
-- 6. AUTOMATION_RULES (Regras de Automação)
-- ============================================================================

CREATE TABLE automation_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID NOT NULL REFERENCES campaigns(id),
    type TEXT NOT NULL, -- 'pause', 'scale', 'reduce_bid', 'change_creative'
    condition JSONB NOT NULL, -- {"metric": "roas", "operator": "<", "value": 2.0}
    action JSONB NOT NULL, -- {"type": "pause"} ou {"type": "scale", "factor": 1.2}
    frequency TEXT DEFAULT 'daily', -- 'daily', 'hourly'
    enabled BOOLEAN DEFAULT TRUE,
    last_executed TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE automation_rules ENABLE ROW LEVEL SECURITY;
CREATE INDEX idx_automation_rules_campaign_id ON automation_rules(campaign_id);

-- ============================================================================
-- 7. AI_DECISIONS (Decisões da IA)
-- ============================================================================

CREATE TABLE ai_decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID NOT NULL REFERENCES campaigns(id),
    decision_type TEXT, -- 'PAUSE', 'SCALE', 'REDUCE_BID', 'CHANGE_CREATIVE', 'KEEP'
    reasoning TEXT,
    priority TEXT, -- 'HIGH', 'MEDIUM', 'LOW'
    status TEXT DEFAULT 'PENDING', -- 'PENDING', 'APPROVED', 'EXECUTED', 'REJECTED'
    approved_by UUID,
    approved_at TIMESTAMP,
    executed_at TIMESTAMP,
    decision_json JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE ai_decisions ENABLE ROW LEVEL SECURITY;
CREATE INDEX idx_ai_decisions_campaign_id ON ai_decisions(campaign_id);
CREATE INDEX idx_ai_decisions_status ON ai_decisions(status);

-- ============================================================================
-- 8. EXECUTION_LOG (Log de Execução)
-- ============================================================================

CREATE TABLE execution_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    decision_id UUID REFERENCES ai_decisions(id),
    campaign_id UUID REFERENCES campaigns(id),
    action_type TEXT,
    status TEXT, -- 'SUCCESS', 'FAILED', 'PENDING'
    error_message TEXT,
    details JSONB,
    executed_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE execution_log ENABLE ROW LEVEL SECURITY;
CREATE INDEX idx_execution_log_campaign_id ON execution_log(campaign_id);
CREATE INDEX idx_execution_log_status ON execution_log(status);

-- ============================================================================
-- 9. TESTS (A/B Tests)
-- ============================================================================

CREATE TABLE tests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID NOT NULL REFERENCES campaigns(id),
    test_type TEXT, -- 'creative', 'audience', 'bid_strategy'
    variant_a_id UUID REFERENCES creatives(id),
    variant_b_id UUID REFERENCES creatives(id),
    start_date DATE,
    end_date DATE,
    status TEXT DEFAULT 'RUNNING', -- 'RUNNING', 'COMPLETE', 'INCONCLUSIVE'
    winner TEXT, -- 'A', 'B', 'INCONCLUSIVE'
    impact_percentage DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE tests ENABLE ROW LEVEL SECURITY;
CREATE INDEX idx_tests_campaign_id ON tests(campaign_id);

-- ============================================================================
-- Row Level Security (RLS) Policies
-- ============================================================================

-- Clientes (ainda sem multi-tenant completo, mas estruturado)
CREATE POLICY "Enable all for now" ON clients FOR ALL USING (true);
CREATE POLICY "Enable all for now" ON ad_accounts FOR ALL USING (true);
CREATE POLICY "Enable all for now" ON campaigns FOR ALL USING (true);
CREATE POLICY "Enable all for now" ON creatives FOR ALL USING (true);
CREATE POLICY "Enable all for now" ON performance_logs FOR ALL USING (true);
CREATE POLICY "Enable all for now" ON automation_rules FOR ALL USING (true);
CREATE POLICY "Enable all for now" ON ai_decisions FOR ALL USING (true);
CREATE POLICY "Enable all for now" ON execution_log FOR ALL USING (true);
CREATE POLICY "Enable all for now" ON tests FOR ALL USING (true);

-- ============================================================================
-- Triggers (Atualizar updated_at automaticamente)
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ad_accounts_updated_at BEFORE UPDATE ON ad_accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Sample Data (para testes)
-- ============================================================================

INSERT INTO clients (name, niche, budget_monthly, objective)
VALUES
    ('Cliente Teste 1', 'e-commerce', 5000.00, 'sales'),
    ('Cliente Teste 2', 'saas', 3000.00, 'leads'),
    ('Cliente Teste 3', 'local', 2000.00, 'awareness');
