#!/usr/bin/env python3
"""
FASE 5: Creative Generator
REFATORADO: Usa Shree2604 Agentic-Ads + Ad Factory Agent (peças prontas)
Gera criativos + vídeos automaticamente quando performance cai
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Importar wrappers das peças prontas
try:
    from integrations.mcp_wrappers import CreativeGeneratorWrapper, AdFactoryAgentWrapper
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ============================================================================
# PROMPT PARA GERAR CRIATIVOS
# ============================================================================

CREATIVE_GENERATION_PROMPT = """Você é um diretor criativo de performance ads.

Recebeu dados de uma campanha com performance baixa (CTR ou CPA acima do esperado).

Gere 5 variações de criativos DIFERENTES com:
1. Hook chamativo
2. Copy persuasivo
3. CTA claro
4. Ângulo de abordagem

FORMATOS:
- 2 variações tipo UGC (user-generated content)
- 1 variação tipo Depoimento/Testimonial
- 1 variação tipo Problema-Solução
- 1 variação tipo Curiosidade/Contraste

RETORNAR JSON:
{
  "campaign_id": "id",
  "creative_count": 5,
  "timestamp": "ISO",
  "creatives": [
    {
      "id": "creative_001",
      "type": "ugc",
      "hook": "...",
      "copy": "...",
      "cta": "...",
      "angle": "...",
      "image_prompt": "..."
    }
  ]
}"""

# ============================================================================
# DADOS DE TESTE
# ============================================================================

UNDERPERFORMING_CAMPAIGNS = {
    "campaigns": [
        {
            "id": "campaign_002",
            "name": "SaaS - Lead Gen",
            "platform": "meta",
            "current_roas": 1.88,
            "current_ctr": 5.0,
            "current_cpa": 266.67,
            "issue": "ROAS abaixo da meta, CTR alto mas conversão baixa",
        }
    ]
}

# ============================================================================
# CLASSE CREATIVE GENERATOR
# ============================================================================

class CreativeGenerator:
    """Gera criativos + vídeos usando Agentic-Ads e Ad Factory (peças prontas)"""

    def __init__(self):
        self.generated_at = datetime.now()

        # Inicializar Creative Generator (Shree2604)
        if HAS_MCP:
            try:
                self.creative_gen = CreativeGeneratorWrapper(
                    api_key=os.getenv("CLAUDE_API_KEY", ""),
                    model="claude-3-opus"
                )
                self.ad_factory = AdFactoryAgentWrapper(
                    api_key=os.getenv("RUNWAYML_API_KEY", ""),
                    provider="runwayml"
                )
                self.use_mcp = True
                logger.info("✅ Agentic-Ads + Ad Factory loaded successfully")
            except Exception as e:
                logger.warning(f"⚠️ Failed to load MCPs: {e} - using fallback")
                self.creative_gen = None
                self.ad_factory = None
                self.use_mcp = False
        else:
            self.use_mcp = False
            self.creative_gen = None
            self.ad_factory = None

    def generate_creatives_for_campaign(self, campaign: Dict) -> Dict:
        """Gerar criativos + vídeos para uma campanha usando peças prontas"""
        logger.info(f"\n🎨 Gerando criativos para {campaign['name']}...")

        campaign_id = campaign["id"]
        product_desc = campaign.get("name", "Produto")

        # Tentar usar Agentic-Ads primeiro
        if self.use_mcp and self.creative_gen:
            try:
                logger.info("📡 Using Shree2604 Agentic-Ads...")
                creatives = self.creative_gen.generate_creatives(
                    product_desc=product_desc,
                    num_variations=5,
                    styles=["UGC", "Testimonial", "Problem-Solution", "Curiosity"]
                )
                if creatives:
                    logger.info(f"✅ Generated {len(creatives)} creatives via Agentic-Ads")
                    creative_results = self._format_creatives(campaign_id, creatives)
                else:
                    creative_results = self._generate_dummy_creatives(campaign_id)
            except Exception as e:
                logger.warning(f"⚠️ Agentic-Ads failed: {e} - using fallback")
                creative_results = self._generate_dummy_creatives(campaign_id)
        else:
            creative_results = self._generate_dummy_creatives(campaign_id)

        # Tentar gerar vídeos com Ad Factory
        video_results = []
        if self.use_mcp and self.ad_factory:
            try:
                logger.info("📹 Using Ad Factory for video generation...")
                videos = self.ad_factory.generate_video_ads(
                    campaign_id=campaign_id,
                    style="product_showcase",
                    duration=15,
                    num_videos=3
                )
                if videos:
                    logger.info(f"✅ Generated {len(videos)} video ads via Ad Factory")
                    video_results = videos
            except Exception as e:
                logger.warning(f"⚠️ Ad Factory failed: {e} - skipping video generation")

        return {
            "campaign_id": campaign_id,
            "campaign_name": campaign["name"],
            "static_creatives_count": len(creative_results),
            "video_ads_count": len(video_results),
            "generated_at": self.generated_at.isoformat(),
            "static_creatives": creative_results,
            "video_ads": video_results,
        }

    def _format_creatives(self, campaign_id: str, creatives: List[Dict]) -> List[Dict]:
        """Format creatives from Agentic-Ads"""
        formatted = []
        for idx, creative in enumerate(creatives, 1):
            formatted.append({
                "id": f"{campaign_id}_creative_{idx:03d}",
                "type": creative.get("type", "ugc"),
                "hook": creative.get("hook", ""),
                "copy": creative.get("copy", ""),
                "cta": creative.get("cta", ""),
                "angle": creative.get("angle", ""),
                "image_prompt": creative.get("image_prompt", "")
            })
        return formatted

    def _generate_dummy_creatives(self, campaign_id: str) -> List[Dict]:
        """Gerar criativos dummy para teste"""
        creatives = [
            {
                "id": f"{campaign_id}_creative_001",
                "type": "ugc",
                "hook": "Você está desperdiçando dinheiro em marketing?",
                "copy": "Descobre como aumentar suas conversões sem gastar mais",
                "cta": "Veja agora",
                "angle": "Fear of missing out",
                "image_prompt": "Professional showing conversion metrics going up, casual style, bright colors"
            },
            {
                "id": f"{campaign_id}_creative_002",
                "type": "ugc",
                "hook": "3 erros que toda empresa comete (e como corrigir)",
                "copy": "Framework simples que 500+ empresas usam todo mês",
                "cta": "Descobrir agora",
                "angle": "Educational value",
                "image_prompt": "Laptop showing analytics dashboard, minimalist design, trending aesthetic"
            },
            {
                "id": f"{campaign_id}_creative_003",
                "type": "testimonial",
                "hook": "Triplicou suas conversões? Veja como ele fez...",
                "copy": "CEO de startup conta sua história de sucesso (e você pode replicar)",
                "cta": "Veja o case",
                "angle": "Social proof",
                "image_prompt": "Happy founder with team in background, professional headshot, warm lighting"
            },
            {
                "id": f"{campaign_id}_creative_004",
                "type": "problem_solution",
                "hook": "ANTES: Time gastando 20h/semana em tarefas repetitivas",
                "copy": "DEPOIS: Automação inteligente que libera tempo pro que importa",
                "cta": "Começar teste grátis",
                "angle": "Efficiency gain",
                "image_prompt": "Before/after split showing stressed vs relaxed team member, clean design"
            },
            {
                "id": f"{campaign_id}_creative_005",
                "type": "curiosity",
                "hook": "Big tech companies pagam milhões por esse simples truque",
                "copy": "Agora você consegue usar grátis (técnica revelada abaixo)",
                "cta": "Desbloquear técnica",
                "angle": "Scarcity/Exclusivity",
                "image_prompt": "Mysterious sealed envelope or locked door, modern illustration, trending"
            }
        ]

        logger.info(f"✅ {len(creatives)} criativos gerados")
        return creatives

    def run_generation(self) -> Dict:
        """Executar geração de criativos"""
        logger.info("=" * 70)
        logger.info("🎨 STARTING CREATIVE GENERATION (FASE 5)")
        logger.info("=" * 70)

        campaigns = UNDERPERFORMING_CAMPAIGNS["campaigns"]
        results = []

        for campaign in campaigns:
            result = self.generate_creatives_for_campaign(campaign)
            results.append(result)

        logger.info("\n" + "=" * 70)
        logger.info("📊 GENERATION SUMMARY")
        logger.info("=" * 70)

        # FIX: Corrigir acesso às chaves corretas (Gemini bug report)
        total_creatives = sum(
            r.get("static_creatives_count", 0) + r.get("video_ads_count", 0)
            for r in results
        )
        logger.info(f"✅ {total_creatives} criativos gerados para {len(campaigns)} campanhas")

        return {
            "generation_timestamp": self.generated_at.isoformat(),
            "campaigns_processed": len(campaigns),
            "total_creatives_generated": total_creatives,
            "results": results,
        }


def main():
    """Executar geração"""
    generator = CreativeGenerator()
    result = generator.run_generation()

    with open("creative_generation_result.json", "w") as f:
        json.dump(result, f, indent=2)

    logger.info(f"\n✅ Resultado salvo em: creative_generation_result.json\n")
    return result


if __name__ == "__main__":
    main()
