#!/usr/bin/env python3
"""
🚀 ADS CORE MVP - Flask API Server
Serve dados de campanhas com fallback pra dummy data
"""

import os
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Carregar env vars
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
# FLASK APP
# ============================================================================

app = Flask(__name__)
app.json.sort_keys = False


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "✅ ADS CORE MVP está rodando!",
        "version": "0.1",
        "timestamp": datetime.now().isoformat(),
        "mode": "DEMO (usando dummy data)",
        "endpoints": {
            "GET /": "Health check",
            "GET /campaigns": "Lista todas as campanhas",
            "GET /campaigns/<id>": "Detalhe de uma campanha",
            "GET /performance": "Performance de todas as campanhas",
            "GET /performance/<id>": "Performance de uma campanha",
            "GET /status": "Status do sistema",
        }
    }), 200


@app.route("/campaigns", methods=["GET"])
def get_campaigns():
    """Retorna todas as campanhas"""
    logger.info("📋 GET /campaigns - Retornando campanhas dummy")

    campaigns = DUMMY_CAMPAIGNS_DATA["campaigns"]

    # Adicionar performance data
    for campaign in campaigns:
        campaign_id = campaign["id"]
        perf = DUMMY_PERFORMANCE_DATA.get(campaign_id, {})

        # Calcular métricas
        spend = perf.get("spend", 0)
        conversions = perf.get("conversions", 0)
        clicks = perf.get("clicks", 0)
        impressions = perf.get("impressions", 0)
        revenue = perf.get("revenue", 0)

        campaign["metrics"] = {
            "spend": spend,
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "revenue": revenue,
            "roas": round(revenue / spend, 2) if spend > 0 else 0,
            "cpa": round(spend / conversions, 2) if conversions > 0 else 0,
            "ctr": round((clicks / impressions) * 100, 2) if impressions > 0 else 0,
            "cpc": round(spend / clicks, 2) if clicks > 0 else 0,
        }

    return jsonify({
        "success": True,
        "count": len(campaigns),
        "data": campaigns,
        "timestamp": datetime.now().isoformat(),
    }), 200


@app.route("/campaigns/<campaign_id>", methods=["GET"])
def get_campaign(campaign_id):
    """Retorna detalhes de uma campanha específica"""
    logger.info(f"📋 GET /campaigns/{campaign_id}")

    campaigns = DUMMY_CAMPAIGNS_DATA["campaigns"]
    campaign = next((c for c in campaigns if c["id"] == campaign_id), None)

    if not campaign:
        return jsonify({
            "error": f"Campanha {campaign_id} não encontrada",
            "success": False,
        }), 404

    # Adicionar performance data
    perf = DUMMY_PERFORMANCE_DATA.get(campaign_id, {})
    spend = perf.get("spend", 0)
    conversions = perf.get("conversions", 0)
    clicks = perf.get("clicks", 0)
    impressions = perf.get("impressions", 0)
    revenue = perf.get("revenue", 0)

    campaign["metrics"] = {
        "spend": spend,
        "impressions": impressions,
        "clicks": clicks,
        "conversions": conversions,
        "revenue": revenue,
        "roas": round(revenue / spend, 2) if spend > 0 else 0,
        "cpa": round(spend / conversions, 2) if conversions > 0 else 0,
        "ctr": round((clicks / impressions) * 100, 2) if impressions > 0 else 0,
        "cpc": round(spend / clicks, 2) if clicks > 0 else 0,
    }

    return jsonify({
        "success": True,
        "data": campaign,
        "timestamp": datetime.now().isoformat(),
    }), 200


@app.route("/performance", methods=["GET"])
def get_performance():
    """Retorna performance de todas as campanhas"""
    logger.info("📊 GET /performance")

    performance_data = {}
    for campaign_id, metrics in DUMMY_PERFORMANCE_DATA.items():
        spend = metrics.get("spend", 0)
        conversions = metrics.get("conversions", 0)
        clicks = metrics.get("clicks", 0)
        impressions = metrics.get("impressions", 0)
        revenue = metrics.get("revenue", 0)

        performance_data[campaign_id] = {
            **metrics,
            "roas": round(revenue / spend, 2) if spend > 0 else 0,
            "cpa": round(spend / conversions, 2) if conversions > 0 else 0,
            "ctr": round((clicks / impressions) * 100, 2) if impressions > 0 else 0,
            "cpc": round(spend / clicks, 2) if clicks > 0 else 0,
        }

    return jsonify({
        "success": True,
        "count": len(performance_data),
        "data": performance_data,
        "timestamp": datetime.now().isoformat(),
    }), 200


@app.route("/performance/<campaign_id>", methods=["GET"])
def get_campaign_performance(campaign_id):
    """Retorna performance de uma campanha específica"""
    logger.info(f"📊 GET /performance/{campaign_id}")

    metrics = DUMMY_PERFORMANCE_DATA.get(campaign_id)

    if not metrics:
        return jsonify({
            "error": f"Performance para campanha {campaign_id} não encontrada",
            "success": False,
        }), 404

    spend = metrics.get("spend", 0)
    conversions = metrics.get("conversions", 0)
    clicks = metrics.get("clicks", 0)
    impressions = metrics.get("impressions", 0)
    revenue = metrics.get("revenue", 0)

    return jsonify({
        "success": True,
        "campaign_id": campaign_id,
        "data": {
            **metrics,
            "roas": round(revenue / spend, 2) if spend > 0 else 0,
            "cpa": round(spend / conversions, 2) if conversions > 0 else 0,
            "ctr": round((clicks / impressions) * 100, 2) if impressions > 0 else 0,
            "cpc": round(spend / clicks, 2) if clicks > 0 else 0,
        },
        "timestamp": datetime.now().isoformat(),
    }), 200


@app.route("/status", methods=["GET"])
def get_status():
    """Retorna status do sistema"""
    logger.info("📊 GET /status")

    return jsonify({
        "success": True,
        "system": {
            "status": "✅ Healthy",
            "mode": "DEMO (dummy data)",
            "campaigns_available": len(DUMMY_CAMPAIGNS_DATA["campaigns"]),
            "has_meta_token": bool(os.getenv("META_ACCESS_TOKEN")),
            "has_google_token": bool(os.getenv("GOOGLE_ADS_CUSTOMER_ID")),
            "has_claude_key": bool(os.getenv("CLAUDE_API_KEY")),
            "has_supabase": bool(os.getenv("SUPABASE_URL")),
        },
        "timestamp": datetime.now().isoformat(),
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint não encontrado",
        "success": False,
    }), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"❌ Erro interno: {error}")
    return jsonify({
        "error": "Erro interno do servidor",
        "success": False,
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("NODE_ENV") != "production"

    logger.info(f"🚀 Iniciando ADS CORE MVP em porta {port} (debug={debug})")
    app.run(host="0.0.0.0", port=port, debug=debug)
