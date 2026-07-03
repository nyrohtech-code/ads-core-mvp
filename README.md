# ADS CORE MVP - Sistema Autônomo de Gestão de Campanhas

**Status:** Iniciando Desenvolvimento  
**Timeline:** 6-7 semanas  
**Objetivo:** MVP funcional + 2 clientes reais rodando  

---

## 📋 Visão Geral

Sistema completo para automação de campanhas Meta Ads e Google Ads usando Claude AI + n8n + MCPs.

### O que o sistema faz:
1. **Puxar dados** de campanhas (24/7 automático)
2. **Claude analisa** performance (ROAS, CPA, CTR)
3. **Toma decisões** (pausar, escalar, trocar criativo)
4. **Executa ações** nas plataformas automaticamente
5. **Gera criativos** quando necessário (Ideogram)
6. **Dashboard** mostra tudo em tempo real

---

## 🎯 Resultado Esperado

- **Antes:** Gerenciar ads manualmente (20h/semana)
- **Depois:** Sistema automático (1h/semana monitoramento)

---

## 📁 Estrutura do Projeto

```
ADS-CORE-MVP/
├── DAG.md                          # Plano de execução completo
├── README.md                       # Este arquivo
├── PHASE_CHECKLIST.md              # Checklist por fase
├── .env.example                    # Variáveis de ambiente
├── docker-compose.yml              # Infra (n8n, Supabase local)
│
├── /docs/                          # Documentação
│   ├── SETUP.md                    # Como setup tudo
│   ├── MCP_SETUP.md                # Setup de MCPs
│   ├── N8N_WORKFLOWS.md            # Workflows n8n
│   ├── CLAUDE_PROMPTS.md           # Prompts do Claude
│   ├── DATABASE.md                 # Schema Supabase
│   └── TESTING.md                  # Como testar
│
├── /src/                           # Código
│   ├── /scripts/
│   │   ├── sync_meta_ads.py        # Puxar dados Meta
│   │   ├── sync_google_ads.py      # Puxar dados Google
│   │   ├── claude_analyzer.py      # Claude analisa
│   │   ├── executor.py             # Executa ações
│   │   └── creative_generator.py   # Gera criativos
│   │
│   ├── /frontend/                  # Next.js app
│   │   ├── pages/
│   │   ├── components/
│   │   └── lib/
│   │
│   └── /n8n/
│       ├── workflow_1_sync.json     # Workflow: puxar dados
│       ├── workflow_2_execute.json  # Workflow: executar ações
│       └── workflow_3_creative.json # Workflow: criar criativos
│
├── /config/                        # Configuração
│   ├── supabase_schema.sql         # Schema do banco
│   ├── mcp_config.json             # Config MCPs
│   └── prompts.json                # Prompts do Claude
│
├── /phase_0/                       # FASE 0: Setup
│   └── CHECKLIST.md
│
├── /phase_1/                       # FASE 1: Conectar APIs
│   ├── CHECKLIST.md
│   └── TEST.md
│
├── /phase_2/                       # FASE 2: Puxar dados
│   ├── CHECKLIST.md
│   └── TEST.md
│
├── ... (fases 3-10)
│
└── /notes/                         # Anotações & learnings
    └── daily_progress.md
```

---

## 🚀 Quick Start (30 min)

### 1. Clone/Setup inicial
```bash
cd ADS-CORE-MVP
cp .env.example .env
# Edite .env com suas credenciais
```

### 2. Veja o plano
```bash
cat DAG.md
```

### 3. Comece com FASE 0
```bash
cat phase_0/CHECKLIST.md
```

---

## 📊 Status das Fases

| Fase | Nome | Status | Timeline |
|---|---|---|---|
| 0 | Setup Básico | ⏳ TODO | Dia 1-3 |
| 1 | Conectar APIs | ⏳ TODO | Dia 3-9 |
| 2 | Puxar Dados | ⏳ TODO | Dia 9-15 |
| 3 | Cérebro Claude | ⏳ TODO | Dia 15-19 |
| 4 | Execução | ⏳ TODO | Dia 19-26 |
| 5 | Criativos | ⏳ TODO | Dia 26-31 |
| 6 | Validação | ⏳ TODO | Dia 31-38 |
| 7 | Dashboard | ⏳ TODO | Dia 38-45 |
| 8 | Multi-tenant | ⏳ TODO | Dia 45-52 |
| 9 | Billing | ⏳ TODO | Dia 52-56 |
| 10 | Polish | ⏳ TODO | Dia 56-63 |

---

## 🔑 Recursos Principais

### Repos que você vai usar:
- [Pipeboard meta-ads-mcp](https://github.com/pipeboard-co/meta-ads-mcp) - MCP Meta
- [mcp-google-ads](https://github.com/cohnen/mcp-google-ads) - MCP Google
- [Claude Ads](https://github.com/AgriciDaniel/claude-ads) - Prompts & skills
- [n8n](https://github.com/n8n-io/n8n) - Orquestração
- [AgenticAds](https://github.com/Shree2604/Agentic-Ads) - Geração de criativos

### APIs & Ferramentas:
- Claude API (Anthropic)
- Meta Ads API
- Google Ads API
- Supabase (PostgreSQL)
- n8n
- Ideogram API

---

## 📞 Contato & Suporte

**Projeto:** GESTÃO ADS - Sistema Autônomo  
**Versão:** MVP 0.1  
**Data de Início:** 2026-07-03  

---

**Próximo passo:** Leia [DAG.md](./DAG.md) para ver o plano completo.
