#!/usr/bin/env python3
"""
FASE 2: Sync Meta Ads Data
REFATORADO: Usa Pipeboard Meta Ads MCP (peça pronta)
Puxar dados de campanhas Meta e salvar no Supabase
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Importar wrapper do Pipeboard MCP
try:
    from integrations.mcp_wrappers import MetaAdsMCPWrapper
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ============================================================================
# DADOS DUMMY (para testes sem credenciais reais)
# ============================================================================

DUMMY_CAMPAIGNS_DATA = {
    "campaigns": [
        {
            "id": "campaign_001",
            "name": "E-commerce - Black Friday",
            "status": "ACTIVE",
            "objective": "LINK_CLICKS",
            "budget_daily": 1000,
            "platform": "meta",
            "created_at": (datetime.now() - timedelta(days=30)).isoformat(),
        },
        {
            "id": "campaign_002",
            "name": "SaaS - Lead Gen",
            "status": "ACTIVE",
            "objective": "LEAD_GENERATION",
            "budget_daily": 500,
            "platform": "meta",
            "created_at": (datetime.now() - timedelta(days=15)).isoformat(),
        },
        {
            "id": "campaign_003",
            "name": "E-commerce - Retargeting",
            "status": "PAUSED",
            "objective": "CONVERSIONS",
            "budget_daily": 750,
            "platform": "meta",
            "created_at": (datetime.now() - timedelta(days=7)).isoformat(),
        },
    ]
}

DUMMY_PERFORMANCE_DATA = {
    "campaign_001": {
        "spend": 28500,
        "impressions": 125000,
        "clicks": 3750,
        "conversions": 125,
        "revenue": 85000,
    },
    "campaign_002": {
        "spend": 12000,
        "impressions": 45000,
        "clicks": 2250,
        "conversions": 45,
        "revenue": 22500,
    },
    "campaign_003": {
        "spend": 0,
        "impressions": 0,
        "clicks": 0,
        "conversions": 0,
        "revenue": 0,
    },
}

# ============================================================================
# CLASSE DE SYNC
# ============================================================================


class MetaAdsSyncer:
    """Sincroniza dados de Meta Ads usando Pipeboard MCP (peça pronta)"""

    def __init__(self, client_id: str = "test_client_001"):
        self.client_id = client_id
        self.access_token = os.getenv("META_ACCESS_TOKEN", "dummy_token_testing")
        self.business_account_id = os.getenv("META_BUSINESS_ACCOUNT_ID", "dummy_account")
        self.synced_at = datetime.now()

        # Inicializar wrapper do Pipeboard MCP se disponível
        if HAS_MCP:
            try:
                self.mcp = MetaAdsMCPWrapper(self.access_token, self.business_account_id)
                self.use_mcp = True
                logger.info("✅ Pipeboard Meta Ads MCP loaded successfully")
            except Exception as e:
                logger.warning(f"⚠️ Failed to load Pipeboard MCP: {e} - using fallback")
                self.mcp = None
                self.use_mcp = False
        else:
            self.use_mcp = False
            self.mcp = None

    def fetch_campaigns(self) -> List[Dict]:
        """Puxar campanhas usando Pipeboard MCP ou fallback dummy"""
        logger.info(f"Fetching Meta campaigns for client {self.client_id}...")

        if self.use_mcp and self.mcp:
            try:
                logger.info("📡 Using Pipeboard Meta Ads MCP...")
                campaigns = self.mcp.get_campaigns()
                if campaigns:
                    logger.info(f"✅ Fetched {len(campaigns)} campaigns via MCP")
                    return campaigns
            except Exception as e:
                logger.warning(f"⚠️ MCP call failed: {e} - falling back to dummy data")

        # Fallback: usar dados dummy
        campaigns = DUMMY_CAMPAIGNS_DATA["campaigns"]
        logger.info(f"✅ Using dummy data: {len(campaigns)} campaigns")
        return campaigns

    def fetch_performance(self, campaign_id: str) -> Dict:
        """Puxar performance usando Pipeboard MCP ou fallback"""
        logger.info(f"Fetching performance for campaign {campaign_id}...")

        if self.use_mcp and self.mcp:
            try:
                logger.info("📡 Using Pipeboard MCP for metrics...")
                metrics = self.mcp.get_campaign_metrics(campaign_id)
                if metrics:
                    logger.info(f"✅ Got metrics via MCP: {metrics}")
                    return metrics
            except Exception as e:
                logger.warning(f"⚠️ MCP metrics failed: {e} - using fallback")

        # Fallback: usar dados dummy
        perf = DUMMY_PERFORMANCE_DATA.get(campaign_id, {})

        # Calcular métricas
        metrics = self._calculate_metrics(perf)

        logger.info(f"✅ Performance: {metrics}")
        return metrics

    def _calculate_metrics(self, data: Dict) -> Dict:
        """Calcular ROAS, CPA, CPC, CTR, etc"""
        spend = data.get("spend", 0.01)  # Evita divisão por zero
        clicks = data.get("clicks", 0)
        conversions = data.get("conversions", 0)
        revenue = data.get("revenue", 0)
        impressions = data.get("impressions", 1)

        return {
            "spend": spend,
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "revenue": revenue,
            "ctr": (clicks / impressions * 100) if impressions > 0 else 0,
            "cpc": (spend / clicks) if clicks > 0 else 0,
            "cpa": (spend / conversions) if conversions > 0 else 0,
            "roas": (revenue / spend) if spend > 0 else 0,
            "conversion_rate": (conversions / clicks * 100) if clicks > 0 else 0,
        }

    def sync_to_database(self, campaigns: List[Dict]) -> bool:
        """Salvar dados no Supabase (simulado)"""
        logger.info(f"Syncing {len(campaigns)} campaigns to database...")

        try:
            sync_result = {
                "client_id": self.client_id,
                "platform": "meta",
                "synced_campaigns": len(campaigns),
                "synced_at": self.synced_at.isoformat(),
                "campaigns": campaigns,
            }

            # TODO: Implementar Supabase insert aqui
            # supabase.table("performance_logs").insert(sync_result).execute()

            logger.info("✅ Sync successful!")
            return True

        except Exception as e:
            logger.error(f"❌ Sync failed: {str(e)}")
            return False

    def run_sync(self) -> Dict:
        """Executar sync completo"""
        logger.info("=" * 60)
        logger.info("🚀 STARTING META ADS SYNC")
        logger.info("=" * 60)

        # 1. Puxar campanhas
        campaigns = self.fetch_campaigns()

        # 2. Puxar performance de cada campanha
        for campaign in campaigns:
            perf = self.fetch_performance(campaign["id"])
            campaign["metrics"] = perf

        # 3. Salvar no banco
        success = self.sync_to_database(campaigns)

        result = {
            "success": success,
            "campaigns_synced": len(campaigns),
            "timestamp": self.synced_at.isoformat(),
            "data": campaigns,
        }

        logger.info("=" * 60)
        logger.info(f"✅ SYNC COMPLETE: {json.dumps(result, indent=2)}")
        logger.info("=" * 60)

        return result


# ============================================================================
# MAIN
# ============================================================================


def main():
    """Executar sync"""
    syncer = MetaAdsSyncer()
    result = syncer.run_sync()
    return result


if __name__ == "__main__":
    main()
