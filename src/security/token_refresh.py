#!/usr/bin/env python3
"""
🔄 OAuth2 Token Refresh Module
Renova tokens Google Ads que expiram a cada 1 hora
Implementa retry automático
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class GoogleAdsTokenManager:
    """
    Gerencia renovação automática de tokens OAuth2 do Google Ads
    """

    def __init__(self, client_id: str, client_secret: str, refresh_token: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = None
        self.token_expires_at = None

    def is_token_expired(self) -> bool:
        """Verifica se token expirou"""
        if not self.token_expires_at:
            return True
        return datetime.now() >= self.token_expires_at

    def refresh_access_token(self) -> str:
        """
        Renova o access token usando o refresh token
        Google Ads tokens expiram a cada 1 hora
        """
        try:
            import requests

            logger.info("🔄 Refrescando Google Ads access token...")

            # Endpoint OAuth2 do Google
            url = "https://oauth2.googleapis.com/token"

            payload = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
            }

            response = requests.post(url, json=payload)
            response.raise_for_status()

            data = response.json()
            self.access_token = data["access_token"]

            # Token expira em ~1 hora, renovar 5 min antes
            expires_in = data.get("expires_in", 3600)
            self.token_expires_at = datetime.now() + timedelta(
                seconds=expires_in - 300
            )

            logger.info(
                f"✅ Token refrescado. Expira em {self.token_expires_at}"
            )
            return self.access_token

        except Exception as e:
            logger.error(f"❌ Falha ao refrescar token: {e}")
            raise

    def get_valid_token(self) -> str:
        """
        Retorna token válido, refrescando se necessário
        """
        if self.is_token_expired():
            self.refresh_access_token()

        return self.access_token

    def auto_refresh_decorator(self, func):
        """
        Decorator que refrescar token automaticamente se expirar
        """
        def wrapper(*args, **kwargs):
            token = self.get_valid_token()
            # Passar token renovado para a função
            return func(*args, token=token, **kwargs)
        return wrapper


# ============================================================================
# EXEMPLO DE USO
# ============================================================================
"""
# Setup
token_manager = GoogleAdsTokenManager(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    refresh_token="YOUR_REFRESH_TOKEN"
)

# Usar com auto-refresh
@token_manager.auto_refresh_decorator
def fetch_campaigns(token):
    # Token é refrescado automaticamente se expirou
    headers = {"Authorization": f"Bearer {token}"}
    # ... fazer request com headers
    pass

# Rodar sem se preocupar com expiração
fetch_campaigns()  # Se token expirou, será refrescado automaticamente
"""
