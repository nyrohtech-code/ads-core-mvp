#!/usr/bin/env python3
"""
🔐 Token Security Module
Criptografa e descriptografa tokens de acesso em repouso
Usa pgsodium do Supabase para máxima segurança
"""

import os
import base64
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TokenCryptor:
    """Criptografa tokens de API antes de armazenar no banco"""

    @staticmethod
    def encrypt_token(token: str, encryption_key: str) -> str:
        """
        Criptografa token com chave simétrica

        Em produção, use a extensão pgsodium do Supabase:
        https://supabase.com/docs/guides/database/extensions/pgsodium
        """
        try:
            # TODO: Implementar com pgsodium (Supabase)
            # from supabase_cryptography import SupabaseCrypto
            # encrypted = SupabaseCrypto.encrypt(token, encryption_key)

            # Por enquanto, usar base64 como fallback (NOT PRODUCTION SAFE)
            logger.warning("⚠️ Usando base64 - implemente pgsodium em produção!")
            encoded = base64.b64encode(token.encode()).decode()
            return f"enc_{encoded}"

        except Exception as e:
            logger.error(f"❌ Encryption failed: {e}")
            raise

    @staticmethod
    def decrypt_token(encrypted_token: str, encryption_key: str) -> str:
        """
        Descriptografa token armazenado
        """
        try:
            if not encrypted_token.startswith("enc_"):
                logger.warning("⚠️ Token não parece criptografado")
                return encrypted_token

            # TODO: Implementar com pgsodium
            # from supabase_cryptography import SupabaseCrypto
            # decrypted = SupabaseCrypto.decrypt(encrypted_token, encryption_key)

            # Fallback: descodificar base64
            encoded = encrypted_token.replace("enc_", "")
            token = base64.b64decode(encoded).decode()
            return token

        except Exception as e:
            logger.error(f"❌ Decryption failed: {e}")
            raise


# ============================================================================
# SUPABASE SETUP (Produção)
# ============================================================================
"""
Para implementar criptografia de verdade em produção:

1. Ativar extensão pgsodium no Supabase:
   ```sql
   CREATE EXTENSION IF NOT EXISTS pgsodium;
   ```

2. Gerar chave de criptografia:
   ```sql
   SELECT pgsodium.crypto_secretbox_keygen();
   ```

3. Modificar schema da tabela ad_accounts:
   ```sql
   ALTER TABLE ad_accounts
   ADD COLUMN access_token_encrypted bytea;

   -- Criptografar tokens existentes
   UPDATE ad_accounts
   SET access_token_encrypted = pgsodium.crypto_secretbox(
       access_token::bytea,
       pgsodium.crypto_secretbox_keygen()
   );

   -- Dropar coluna original
   ALTER TABLE ad_accounts DROP COLUMN access_token;
   ```

4. Usar em Python:
   ```python
   from supabase import create_client

   supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

   # Descriptografar automaticamente
   response = supabase.rpc('get_decrypted_token', {
       'account_id': account_id
   }).execute()
   ```
"""
