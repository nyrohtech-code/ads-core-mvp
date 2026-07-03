#!/usr/bin/env python3
"""
👤 Human-in-the-Loop Approval Module
Requer aprovação humana antes de executar ações automaticamente
Implementa workflow de aprovação para ações de alto impacto
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)


class ApprovalStatus(Enum):
    """Status de aprovação"""
    PENDING = "PENDING"          # Aguardando aprovação
    APPROVED = "APPROVED"        # Aprovado, pronto pra executar
    REJECTED = "REJECTED"        # Rejeitado, não executar
    AUTO_APPROVED = "AUTO_APPROVED"  # Auto-aprovado (piloto automático)


class HumanApprovalWorkflow:
    """
    Workflow de aprovação humana para decisões automatizadas
    Usado quando Claude quer fazer ações de alto risco
    """

    def __init__(self, supabase_client=None):
        self.supabase = supabase_client
        self.pending_approvals = []

    def create_approval_request(
        self,
        decision_id: str,
        campaign_id: str,
        action: str,
        reason: str,
        priority: str,
        estimated_impact: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Cria uma requisição de aprovação
        Salva no banco com status PENDING
        """
        approval = {
            "decision_id": decision_id,
            "campaign_id": campaign_id,
            "action": action,  # PAUSE, SCALE_20, REDUCE_BID, etc
            "reason": reason,  # Por que Claude recomenda isso
            "priority": priority,  # HIGH, MEDIUM, LOW
            "estimated_impact": estimated_impact,  # {"cpa_reduction": "15%", ...}
            "status": ApprovalStatus.PENDING.value,
            "created_at": datetime.now().isoformat(),
            "approved_at": None,
            "approved_by": None,
            "approval_notes": None,
        }

        logger.info(
            f"📋 Approval request criado: {action} em {campaign_id} (Priority: {priority})"
        )

        # Salvar no Supabase
        if self.supabase:
            self.supabase.table("approval_requests").insert(approval).execute()

        self.pending_approvals.append(approval)
        return approval

    def approve_decision(
        self,
        decision_id: str,
        approved_by: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Aprova uma decisão e habilita execução
        """
        try:
            if self.supabase:
                self.supabase.table("ai_decisions").update({
                    "status": ApprovalStatus.APPROVED.value,
                    "approved_by": approved_by,
                    "approved_at": datetime.now().isoformat(),
                    "approval_notes": notes
                }).eq("id", decision_id).execute()

            logger.info(f"✅ Decisão {decision_id} aprovada por {approved_by}")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao aprovar: {e}")
            return False

    def reject_decision(
        self,
        decision_id: str,
        rejected_by: str,
        reason: str
    ) -> bool:
        """
        Rejeita uma decisão - não será executada
        """
        try:
            if self.supabase:
                self.supabase.table("ai_decisions").update({
                    "status": ApprovalStatus.REJECTED.value,
                    "rejected_by": rejected_by,
                    "rejection_reason": reason,
                    "rejected_at": datetime.now().isoformat()
                }).eq("id", decision_id).execute()

            logger.info(f"❌ Decisão {decision_id} rejeitada por {rejected_by}")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao rejeitar: {e}")
            return False

    def get_pending_approvals(self, client_id: str) -> list:
        """
        Retorna todas as aprovações pendentes do cliente
        Para exibir no dashboard
        """
        if self.supabase:
            response = self.supabase.table("ai_decisions").select(
                "*"
            ).eq("client_id", client_id).eq(
                "status", ApprovalStatus.PENDING.value
            ).execute()

            return response.data if response.data else []

        return self.pending_approvals

    def enable_auto_approval_mode(self, client_id: str, enabled: bool = True):
        """
        Habilita 'Piloto Automático'
        Apenas após sistema provar eficácia
        """
        logger.warning(
            f"⚠️ Auto-approval mode: {'ENABLED' if enabled else 'DISABLED'} "
            f"para cliente {client_id}"
        )

        # Salvar preferência no Supabase
        if self.supabase:
            self.supabase.table("clients").update({
                "auto_approval_enabled": enabled
            }).eq("id", client_id).execute()


# ============================================================================
# FLUXO RECOMENDADO
# ============================================================================
"""
FASE 1: MVP (Hoje - com human approval)
├─ Claude gera decisão (PAUSE, SCALE, etc)
├─ Sistema cria "approval request"
├─ Dashboard mostra "Aguardando sua aprovação"
├─ Gerente de tráfego clica "Aprovar"
└─ Ação é executada nas APIs

FASE 2: Piloto (Semanas 2-4)
├─ Executar ~50 ações aprovadas
├─ Medir taxa de sucesso
├─ Se >90% de sucesso, passar pra fase 3

FASE 3: Auto-Piloto (Semanas 4+)
├─ Habilitar auto_approval_enabled = true
├─ Ações são executadas sem aprovação
├─ Dashboard ainda mostra histórico pra auditoria
└─ Gerente pode desabilitar auto-pilot a qualquer momento
"""
