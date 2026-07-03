#!/usr/bin/env python3
"""
⏱️ Rate Limiter Module
Controla requisições pra Google Ads e Meta Ads APIs
Evita throttling e banimentos temporários
"""

import time
import logging
from typing import Callable, Any
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Rate limiter para APIs externas
    Implementa backoff exponencial
    """

    def __init__(self, requests_per_minute: int = 60, api_name: str = "API"):
        self.requests_per_minute = requests_per_minute
        self.api_name = api_name
        self.request_times = []
        self.backoff_until = None

    def wait_if_needed(self):
        """Aguarda se necessário antes de fazer request"""
        now = datetime.now()

        # Se está em backoff, aguardar
        if self.backoff_until and now < self.backoff_until:
            wait_seconds = (self.backoff_until - now).total_seconds()
            logger.warning(
                f"⏳ {self.api_name} em backoff. Aguardando {wait_seconds:.1f}s"
            )
            time.sleep(wait_seconds)
            self.backoff_until = None
            self.request_times = []

        # Limpar requisições antigas (> 60 segundos)
        self.request_times = [
            t for t in self.request_times
            if (now - t).total_seconds() < 60
        ]

        # Verificar limite
        if len(self.request_times) >= self.requests_per_minute:
            # Ativar backoff exponencial
            backoff_seconds = min(60, len(self.request_times) * 2)
            self.backoff_until = now + timedelta(seconds=backoff_seconds)
            logger.warning(
                f"⚠️ Rate limit atingido em {self.api_name}. "
                f"Backoff de {backoff_seconds}s"
            )
            self.wait_if_needed()

        self.request_times.append(now)

    def rate_limit(self, func: Callable) -> Callable:
        """Decorator para rate limiting"""
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            self.wait_if_needed()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Se for erro de rate limit, ativar backoff
                if "rate limit" in str(e).lower() or "quota" in str(e).lower():
                    self.backoff_until = datetime.now() + timedelta(minutes=5)
                    logger.error(f"Rate limit error: {e}. Backoff ativado.")
                raise
        return wrapper


# ============================================================================
# RATE LIMITERS POR API
# ============================================================================

GOOGLE_ADS_LIMITER = RateLimiter(
    requests_per_minute=60,  # Google Ads: 60 req/min para Basic Access
    api_name="Google Ads"
)

META_ADS_LIMITER = RateLimiter(
    requests_per_minute=100,  # Meta: ~100 req/min (limite flexível)
    api_name="Meta Ads"
)


# ============================================================================
# DECORATOR DE USO
# ============================================================================

def rate_limited_google_ads(func: Callable) -> Callable:
    """Decorator para rate limiting em Google Ads"""
    return GOOGLE_ADS_LIMITER.rate_limit(func)


def rate_limited_meta_ads(func: Callable) -> Callable:
    """Decorator para rate limiting em Meta Ads"""
    return META_ADS_LIMITER.rate_limit(func)


# ============================================================================
# EXEMPLO DE USO
# ============================================================================
"""
from rate_limiter import rate_limited_google_ads

@rate_limited_google_ads
def fetch_google_campaigns():
    # Faz requisição - será rate limited automaticamente
    return google_client.get_campaigns()

# Usar em loop seguro
for campaign_id in campaign_ids:
    data = fetch_google_campaigns()  # Respeita rate limits automaticamente
"""
