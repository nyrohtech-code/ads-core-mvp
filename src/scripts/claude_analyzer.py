#!/usr/bin/env python3
"""
FASE 3: Claude AI Analyzer
Análise de dados de ads e geração de ações automáticas usando Claude
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

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
# PROMPT DO CLAUDE (CÉREBRO)
# ============================================================================

CLAUDE_ANALYZER_PROMPT = """Você é um sistema de análise automática de campanhas de publicidade.

Recebeu dados de performance de campanhas Meta e Google Ads.

Sua tarefa:
1. Analisar os dados (ROAS, CPA, CTR, etc)
2. Identificar campanhas que precisam de ação
3. Retornar um JSON com decisões

REGRAS DE DECISÃO:
- ROAS < 2.0: PAUSE (investimento perdido)
- ROAS 2.0-2.5: REDUCE_BID (margem baixa)
- ROAS 2.5-3.5: KEEP (normal)
- ROAS > 3.5: SCALE_20 (está bom, aumentar 20%)
- CPA acima da média: PAUSE ou REDUCE
- CTR muito baixo (<1%): CHANGE_CREATIVE
- Campanhas pausadas: DELETE_INACTIVE (se tá parada há dias)

RETORNAR SEMPRE EM JSON:
{
  "analysis_timestamp": "ISO timestamp",
  "total_campaigns": número,
  "decisions": [
    {
      "campaign_id": "id",
      "campaign_name": "nome",
      "current_roas": número,
      "current_cpa": número,
      "action": "SCALE_20 | REDUCE_BID | PAUSE | CHANGE_CREATIVE | KEEP",
      "reasoning": "explicação breve",
      "priority": "HIGH | MEDIUM | LOW"
    }
  ],
  "summary": "resumo executivo em 1-2 frases"
}

Seja conciso e sempre retorne JSON válido."""

# ============================================================================
# DADOS DE TESTE
# ============================================================================

SAMPLE_CAMPAIGNS_DATA = {
    "campaigns": [
        {
            "id": "campaign_001",
            "name": "E-commerce - Black Friday",
            "platform": "meta",
            "status": "ACTIVE",
            "budget_daily": 1000,
            "metrics": {
                "spend": 28500,
                "impressions": 125000,
                "clicks": 3750,
                "conversions": 125,
                "revenue": 85000,
                "ctr": 3.0,
                "cpc": 7.6,
                "cpa": 228,
                "roas": 2.98,
                "conversion_rate": 3.33,
            },
        },
        {
            "id": "campaign_002",
            "name": "SaaS - Lead Gen",
            "platform": "meta",
            "status": "ACTIVE",
            "budget_daily": 500,
            "metrics": {
                "spend": 12000,
                "impressions": 45000,
                "clicks": 2250,
                "conversions": 45,
                "revenue": 22500,
                "ctr": 5.0,
                "cpc": 5.33,
                "cpa": 266.67,
                "roas": 1.875,
                "conversion_rate": 2.0,
            },
        },
        {
            "id": "google_campaign_001",
            "name": "Search - Product Launch",
            "platform": "google",
            "status": "ACTIVE",
            "budget_daily": 2000,
            "metrics": {
                "spend": 42000,
                "impressions": 350000,
                "clicks": 8750,
                "conversions": 175,
                "revenue": 105000,
                "ctr": 2.5,
                "cpc": 4.8,
                "cpa": 240,
                "roas": 2.5,
                "conversion_rate": 2.0,
            },
        },
        {
            "id": "google_campaign_002",
            "name": "Shopping - E-commerce",
            "platform": "google",
            "status": "ACTIVE",
            "budget_daily": 1500,
            "metrics": {
                "spend": 38000,
                "impressions": 125000,
                "clicks": 6250,
                "conversions": 312,
                "revenue": 156000,
                "ctr": 5.0,
                "cpc": 6.08,
                "cpa": 121.79,
                "roas": 4.1,
                "conversion_rate": 4.99,
            },
        },
    ]
}


# ============================================================================
# CLASSE DE ANÁLISE
# ============================================================================


class ClaudeAnalyzer:
    """Analyzer de campanhas usando Claude"""

    def __init__(self, use_dummy: bool = True):
        self.use_dummy = use_dummy
        self.analyzed_at = datetime.now()

    def format_data_for_claude(self, campaigns: List[Dict]) -> str:
        """Formatar dados para enviar pro Claude"""
        formatted = "DADOS DE CAMPANHAS PARA ANÁLISE:\n\n"

        for campaign in campaigns:
            formatted += f"Campanha: {campaign['name']}\n"
            formatted += f"  ID: {campaign['id']}\n"
            formatted += f"  Plataforma: {campaign['platform']}\n"
            formatted += f"  Status: {campaign['status']}\n"
            formatted += f"  Métricas:\n"

            metrics = campaign.get("metrics", {})
            formatted += f"    - ROAS: {metrics.get('roas', 0):.2f}x\n"
            formatted += f"    - CPA: R$ {metrics.get('cpa', 0):.2f}\n"
            formatted += f"    - CTR: {metrics.get('ctr', 0):.2f}%\n"
            formatted += f"    - CPC: R$ {metrics.get('cpc', 0):.2f}\n"
            formatted += f"    - Conversões: {metrics.get('conversions', 0)}\n"
            formatted += f"    - Spend: R$ {metrics.get('spend', 0):.2f}\n"
            formatted += f"    - ROAS: {metrics.get('roas', 0):.2f}x\n"
            formatted += "\n"

        return formatted

    def analyze_with_claude(self, campaigns: List[Dict]) -> Dict:
        """Analisar campanhas com Claude"""
        logger.info("🧠 Analyzing campaigns with Claude...")

        # Formatar dados
        formatted_data = self.format_data_for_claude(campaigns)

        # Criar prompt completo
        full_prompt = f"""{CLAUDE_ANALYZER_PROMPT}

{formatted_data}

Analise os dados acima e retorne as ações em JSON."""

        logger.info("Enviando dados pra Claude...")

        if self.use_dummy:
            # Usar resposta dummy (simulada)
            logger.info("(Usando resposta simulada para teste)")
            decisions = self._generate_dummy_analysis(campaigns)
        else:
            # TODO: Chamar Claude API real aqui
            # decisions = self._call_claude_api(full_prompt)
            logger.warning("Claude API não configurada, usando dummy")
            decisions = self._generate_dummy_analysis(campaigns)

        return decisions

    def _generate_dummy_analysis(self, campaigns: List[Dict]) -> Dict:
        """Gerar análise simulada (para testes)"""
        decisions = []

        for campaign in campaigns:
            metrics = campaign.get("metrics", {})
            roas = metrics.get("roas", 0)
            cpa = metrics.get("cpa", 0)
            ctr = metrics.get("ctr", 0)

            # Aplicar regras simples
            if roas < 1.5:
                action = "PAUSE"
                reasoning = f"ROAS muito baixo ({roas:.2f}x), campanha não tá rentável"
                priority = "HIGH"
            elif roas < 2.0:
                action = "REDUCE_BID"
                reasoning = f"ROAS ({roas:.2f}x) abaixo do esperado, reduzir bids"
                priority = "MEDIUM"
            elif roas > 3.5:
                action = "SCALE_20"
                reasoning = f"ROAS excelente ({roas:.2f}x), escalar 20%"
                priority = "HIGH"
            elif ctr < 1.0:
                action = "CHANGE_CREATIVE"
                reasoning = f"CTR muito baixo ({ctr:.2f}%), trocar criativo"
                priority = "MEDIUM"
            else:
                action = "KEEP"
                reasoning = f"Performance normal, manter como está"
                priority = "LOW"

            decisions.append({
                "campaign_id": campaign["id"],
                "campaign_name": campaign["name"],
                "platform": campaign["platform"],
                "current_roas": round(roas, 2),
                "current_cpa": round(cpa, 2),
                "current_ctr": round(ctr, 2),
                "action": action,
                "reasoning": reasoning,
                "priority": priority,
            })

        return {
            "analysis_timestamp": self.analyzed_at.isoformat(),
            "total_campaigns": len(campaigns),
            "decisions": decisions,
            "summary": f"Análise de {len(campaigns)} campanhas. {sum(1 for d in decisions if d['action'] != 'KEEP')} requerem ação.",
        }

    def run_analysis(self) -> Dict:
        """Executar análise completa"""
        logger.info("=" * 70)
        logger.info("🧠 STARTING CLAUDE ANALYSIS")
        logger.info("=" * 70)

        # Usar dados de teste
        campaigns = SAMPLE_CAMPAIGNS_DATA["campaigns"]

        logger.info(f"📊 Analisando {len(campaigns)} campanhas...")

        # Análise
        result = self.analyze_with_claude(campaigns)

        logger.info("=" * 70)
        logger.info(f"✅ ANALYSIS COMPLETE")
        logger.info("=" * 70)

        # Log de decisões
        logger.info("\n📋 DECISÕES GERADAS:\n")
        for decision in result["decisions"]:
            logger.info(
                f"  {decision['campaign_name']}: "
                f"{decision['action']} "
                f"(ROAS: {decision['current_roas']}x, Priority: {decision['priority']})"
            )

        logger.info(f"\n📊 Resumo: {result['summary']}\n")

        return result


# ============================================================================
# MAIN
# ============================================================================


def main():
    """Executar análise"""
    analyzer = ClaudeAnalyzer(use_dummy=True)
    result = analyzer.run_analysis()

    # Salvar resultado em JSON
    with open("analysis_result.json", "w") as f:
        json.dump(result, f, indent=2)

    logger.info(f"✅ Resultado salvo em: analysis_result.json")

    return result


if __name__ == "__main__":
    main()
