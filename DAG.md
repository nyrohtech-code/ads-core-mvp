# DAG DE EXECUÇÃO - ADS CORE MVP

**Versão:** 1.0  
**Data:** 2026-07-03  
**Timeline Total:** 6-7 semanas

---

## 🎯 DAG VISUAL COMPLETO

```
FASE 0 (Setup: Dias 1-3)
    ↓
FASE 1 (Conectar APIs: Dias 3-9) [PARALELO: Meta MCP, Google MCP, Supabase]
    ↓
FASE 2 (Puxar Dados: Dias 9-15) [PARALELO: Scripts + n8n Workflow 1]
    ↓
FASE 3 (Cérebro Claude: Dias 15-19)
    ↓
FASE 4 (Executar Ações: Dias 19-26)
    ↓
FASE 5 (Criativos: Dias 26-31)
    ↓
FASE 6 (Validação Cliente Real: Dias 31-38) ← CRÍTICO
    ↓
FASE 7 (Dashboard: Dias 38-45) [pode começar paralelo com fase 6]
    ↓
FASE 8 (Multi-tenant: Dias 45-52)
    ↓
FASE 9 (Billing: Dias 52-56)
    ↓
FASE 10 (Polish: Dias 56-63)
    ↓
🚀 LAUNCH MVP
```

---

## 📋 FASE 0: SETUP BÁSICO (Dias 1-3)

### Objetivo
Preparar ambiente e credenciais para começar

### Tasks
**Task 0.1: Definir Cliente de Teste**
- [ ] Escolher cliente real (seu ou conhecido)
- [ ] Pegar Meta Business Account ID
- [ ] Pegar Google Ads Customer ID
- [ ] Ter 2-3 campanhas ativas pra testar
- [ ] Ter acesso às credenciais

**Task 0.2: Preparar Ambiente Dev**
- [ ] Instalar: Git, Docker, Node.js 18+, Python 3.9+
- [ ] Criar `.env` com variáveis (vide .env.example)
- [ ] Criar pasta do projeto (já feito)
- [ ] Inicializar git repo

**Task 0.3: Contas & Credenciais**
- [ ] Supabase: criar conta + projeto
- [ ] Claude: API key (Anthropic)
- [ ] Meta: Developer account + app + token
- [ ] Google Ads: API key + credentials.json
- [ ] Ideogram: API key (opcional para MVP)
- [ ] n8n: preparar (Docker ou cloud)

### Entregáveis
- ✅ `.env` preenchido com todas as credenciais
- ✅ Ambiente dev funcionando
- ✅ Cliente de teste confirmado
- ✅ Acesso a todas as APIs

### Documentação
- Vide: `phase_0/CHECKLIST.md`

---

## 🔌 FASE 1: CONECTAR APIs (Dias 3-9) - PARALELO

### Objetivo
Integrar MCPs e validar que conseguem se conectar com as plataformas

### Tasks (RODAM EM PARALELO)

**Task 1.1: Meta Ads MCP Setup**
```
Repo: https://github.com/pipeboard-co/meta-ads-mcp
Ação:
  1. git clone pipeboard-co/meta-ads-mcp
  2. npm install
  3. Configurar token Meta
  4. Testar: consegue listar campanhas?
  
Entregável: MCP funcional, rodando local
```

**Task 1.2: Google Ads MCP Setup**
```
Repo: https://github.com/cohnen/mcp-google-ads
Ação:
  1. git clone cohnen/mcp-google-ads
  2. npm install / python setup
  3. Configurar credenciais Google
  4. Testar: consegue listar campanhas?

Entregável: MCP funcional, rodando local
```

**Task 1.3: Supabase Setup**
```
Ação:
  1. Criar projeto no Supabase (ou local)
  2. Criar tabelas:
     - clients
     - campaigns
     - creatives
     - performance_logs
     - ai_decisions
  3. Configurar RLS (row-level security)
  4. Testar: consegue inserir/ler dados?

Entregável: DB rodando, schema pronto
Vide: config/supabase_schema.sql
```

### Validação FASE 1
- ✅ Meta MCP conecta e retorna dados
- ✅ Google MCP conecta e retorna dados
- ✅ Supabase rodando, tabelas criadas
- ✅ Consegue fazer operações CRUD em cada um

### Timeline
- 5-7 dias (paralelo = menos tempo)

### Documentação
- Vide: `phase_1/CHECKLIST.md` + `docs/MCP_SETUP.md`

---

## 📊 FASE 2: PUXAR DADOS (Dias 9-15)

### Objetivo
Criar scripts e workflows para puxar dados automaticamente

### Tasks

**Task 2.1: Script de Sync Meta Ads**
```
Arquivo: src/scripts/sync_meta_ads.py

Ação:
  1. Script Python que:
     - Conecta via Meta MCP
     - Puxar: spend, leads, conversões, CTR, CPC
     - Puxar últimas 24h de cada campanha
     - Salvar no Supabase
  2. Testar rodando 1x com dados reais
  
Entregável: sync_meta_ads.py funcional
```

**Task 2.2: Script de Sync Google Ads**
```
Arquivo: src/scripts/sync_google_ads.py

Ação:
  1. Script Python que:
     - Conecta via Google MCP
     - Puxar mesmos dados que Meta
     - Salvar no Supabase
  2. Testar rodando 1x

Entregável: sync_google_ads.py funcional
```

**Task 2.3: n8n Workflow 1 - SYNC**
```
Arquivo: src/n8n/workflow_1_sync.json

Ação:
  1. Criar workflow n8n:
     - Trigger: Cron 24h (ex: 06:00 UTC)
     - Executa: sync_meta_ads.py
     - Executa: sync_google_ads.py
     - Log: quando rodou, se teve erro
  2. Testar: rodar 1x manualmente
  
Entregável: Workflow JSON pronto pra importar
Vide: docs/N8N_WORKFLOWS.md
```

### Validação FASE 2
- ✅ Dados sendo puxados de Meta (24h)
- ✅ Dados sendo puxados de Google (24h)
- ✅ Tudo salvando no Supabase
- ✅ Workflow roda automaticamente

### Timeline
- 5-7 dias

### Documentação
- Vide: `phase_2/CHECKLIST.md` + `docs/N8N_WORKFLOWS.md`

---

## 🧠 FASE 3: CÉREBRO CLAUDE (Dias 15-19)

### Objetivo
Criar prompts que fazem Claude analisar dados e tomar decisões

### Tasks

**Task 3.1: Criar Prompt Principal**
```
Arquivo: config/prompts.json

Ação:
  1. Pegar prompts de:
     - github.com/AgriciDaniel/claude-ads
     - github.com/hayesti54-eng/ai-media-buying-skills
  2. Adaptar pro seu case
  3. Prompt faz Claude:
     - Receber dados de ads (spend, leads, ROAS, CPA)
     - Analisar performance
     - Retornar JSON com ações:
       {
         "pause": ["campaign_id_1"],
         "scale": ["campaign_id_2"],
         "adjust_budget": [{"campaign_id": "x", "new_budget": 1500}],
         "reasoning": "..."
       }
  4. Testar manualmente com dados reais
  
Entregável: prompt.json funcional
Vide: docs/CLAUDE_PROMPTS.md
```

**Task 3.2: Script Python que chama Claude**
```
Arquivo: src/scripts/claude_analyzer.py

Ação:
  1. Script que:
     - Pega dados do Supabase
     - Monta mensagem com prompt
     - Chama Claude API
     - Recebe JSON de ações
     - Retorna estruturado
  2. Testar: rodar 1x com dados reais
  
Entregável: claude_analyzer.py funcional
```

### Validação FASE 3
- ✅ Claude entende dados de ads
- ✅ Retorna ações válidas (pause, scale, etc)
- ✅ JSON estruturado corretamente
- ✅ Prompts fazem sentido com dados reais

### Timeline
- 3-4 dias

### Documentação
- Vide: `phase_3/CHECKLIST.md` + `docs/CLAUDE_PROMPTS.md`

---

## ⚡ FASE 4: EXECUÇÃO (Dias 19-26)

### Objetivo
Fazer o sistema realmente executar ações nas plataformas

### Tasks

**Task 4.1: Script de Execução**
```
Arquivo: src/scripts/executor.py

Ação:
  1. Script que:
     - Recebe JSON de Claude (ações)
     - Para PAUSE: chama Meta/Google MCP
     - Para SCALE: incrementa budget via API
     - Para ADJUST: faz mudanças específicas
     - Registra tudo no log
  2. Testar: executar 1 ação real (em sandbox)
  
Entregável: executor.py funcional
```

**Task 4.2: n8n Workflow 2 - EXECUÇÃO**
```
Arquivo: src/n8n/workflow_2_execute.json

Ação:
  1. Workflow que:
     - Trigger: Quando Claude gera decisões
     - Chama executor.py
     - Registra ações em Supabase
     - Notifica (Slack/email se erro)
  2. Testar: rodar 1x manualmente
  
Entregável: Workflow JSON
```

**Task 4.3: Integração Completa**
```
Ação:
  1. Conectar Workflow 1 (puxar dados) +
              Workflow 2 (executar)
  2. Flow completo:
     - Cron 24h: puxar dados
     - Claude analisa
     - Executa ações
     - Log tudo
  3. Testar: rodar loop 1x completo
  
Entregável: Loop automático funcionando
```

### Validação FASE 4
- ✅ Ações sendo executadas realmente nas APIs
- ✅ Log completo de tudo que foi feito
- ✅ Sem erros críticos
- ✅ Rollback funciona se precisa

### Timeline
- 5-7 dias

### Documentação
- Vide: `phase_4/CHECKLIST.md`

---

## 🎨 FASE 5: CRIATIVOS (Dias 26-31)

### Objetivo
Integrar geração automática de criativos quando performance cai

### Tasks

**Task 5.1: Script de Geração de Criativos**
```
Arquivo: src/scripts/creative_generator.py

Ação:
  1. Script que:
     - Recebe trigger de Claude (CTR baixo)
     - Claude gera prompt criativo
     - Chama Ideogram API
     - Ideogram retorna imagem
     - Sobe imagem via Meta MCP
     - Cria novo ad set com imagem
  2. Testar: gerar 1 criativo real
  
Entregável: creative_generator.py funcional
```

**Task 5.2: n8n Workflow 3 - CRIATIVOS**
```
Arquivo: src/n8n/workflow_3_creative.json

Ação:
  1. Workflow que:
     - Trigger: IF campaign.ctr < threshold
     - Chama creative_generator.py
     - Sobe novo ad
  2. Testar: rodar 1x
  
Entregável: Workflow JSON
```

### Validação FASE 5
- ✅ Criativos sendo gerados quando necessário
- ✅ Subindo nos ads reais
- ✅ Performance initial dos novos ads

### Timeline
- 3-4 dias

### Documentação
- Vide: `phase_5/CHECKLIST.md`

---

## 🧪 FASE 6: VALIDAÇÃO COM CLIENTE REAL (Dias 31-38)

### Objetivo (CRÍTICO)
Provar que o sistema funciona com dados reais, com cliente real

### Tasks

**Task 6.1: Deixar Rodar**
```
Ação:
  1. Sistema rodando 24/7 automaticamente
  2. Deixar por 3-5 dias
  3. Cliente acompanhando:
     - ROAS melhorou?
     - CPA caiu?
     - Ações da IA fizeram sentido?
     - Criativos ficaram bons?
  
Entregável: Dados reais de performance
```

**Task 6.2: Feedback & Ajustes**
```
Ação:
  1. Reunião com cliente
  2. Perguntar:
     - O que achou?
     - Tá vendo as ações?
     - Confia nas decisões?
     - Quer mudar algo?
  3. Ajustar prompts se precisa
  
Entregável: Feedback coletado
```

### Validação FASE 6
- ✅ Sistema rodou 3-5 dias sem erros críticos
- ✅ ROAS melhorou OU manteve
- ✅ Cliente validou
- ✅ Se não funcionar: volta debug (Fase 3/4)

### Timeline
- 7 dias

### Documentação
- Vide: `phase_6/CHECKLIST.md`

---

## 🎨 FASE 7: DASHBOARD (Dias 38-45)

### Objetivo
Criar interface visual para cliente acompanhar

### Tasks

**Task 7.1: Frontend com Next.js**
```
Arquivo: src/frontend/

Ação:
  1. Criar Next.js app com:
     - Página de login (Supabase auth)
     - Dashboard (cards: ROAS, CPA, spend, leads)
     - Página de campanhas (lista + drill-down)
     - Timeline de ações (log de tudo que IA fez)
  2. Conectar ao Supabase
  3. Testar: consegue ver dados?
  
Entregável: Frontend funcionando
```

### Validação FASE 7
- ✅ Frontend carregando dados do Supabase
- ✅ Isolamento multi-tenant básico
- ✅ Responsivo (desktop)

### Timeline
- 5-7 dias

### Documentação
- Vide: `phase_7/CHECKLIST.md`

---

## 👥 FASE 8: MULTI-TENANT (Dias 45-52)

### Objetivo
Fazer sistema funcionar com múltiplos clientes isolados

### Tasks

**Task 8.1: Remover Hardcodes**
```
Ação:
  1. Todos os scripts: cliente_id dinâmico
  2. Credenciais: vêm do Supabase
  3. Workflows n8n: paramétricos
  
Entregável: Sistema genérico
```

**Task 8.2: Onboarding de Cliente Novo**
```
Ação:
  1. Fluxo de onboarding:
     - Cliente cria conta
     - Conecta Meta + Google (OAuth)
     - Sistema cria projeto no Supabase
     - Workflows rodam pra ele
  2. Testar com cliente 2
  
Entregável: 2 clientes rodando isolados
```

### Validação FASE 8
- ✅ Cliente 1 isolado de Cliente 2
- ✅ Dados não se misturam
- ✅ Workflows rodam independente

### Timeline
- 5-7 dias

### Documentação
- Vide: `phase_8/CHECKLIST.md`

---

## 💰 FASE 9: BILLING (Dias 52-56)

### Objetivo
Integrar pagamento

### Tasks

**Task 9.1: Stripe Setup**
```
Ação:
  1. Criar produtos no Stripe:
     - Starter: R$297
     - Pro: R$997
     - Agency: R$2000
  2. Integrar no frontend
  
Entregável: Checkout funcionando
```

**Task 9.2: Metering (Créditos)**
```
Ação:
  1. Contar:
     - Claude API calls
     - Ideogram calls
     - Workflows executados
  2. Descontar de créditos do cliente
  
Entregável: Sistema de uso funcionando
```

### Timeline
- 3-4 dias

### Documentação
- Vide: `phase_9/CHECKLIST.md`

---

## ✨ FASE 10: POLISH (Dias 56-63)

### Objetivo
Deixar pronto pra vender

### Tasks

**Task 10.1: Documentação**
- [ ] README pronto
- [ ] Guia de setup
- [ ] FAQ
- [ ] Video tutorial (opcional)

**Task 10.2: Segurança**
- [ ] Audit logs
- [ ] 2FA (Supabase)
- [ ] Rate limiting
- [ ] Validações

**Task 10.3: Performance**
- [ ] Otimizar queries
- [ ] Caching básico
- [ ] Erro handling robusto

**Task 10.4: Tests**
- [ ] Tests unitários (scripts)
- [ ] Tests integração (workflows)
- [ ] Teste de carga leve

### Timeline
- 5-7 dias

---

## 🎯 CHECKPOINTS CRÍTICOS

- **FASE 1 ✅:** MCPs conectados
- **FASE 2 ✅:** Dados sendo puxados
- **FASE 4 ✅:** Ações sendo executadas
- **FASE 6 ✅:** CLIENTE VALIDOU (se falhar, volta debug)
- **FASE 8 ✅:** 2 clientes rodam isolados
- **FASE 10 ✅:** Pronto pra vender

---

## 🚨 RISCOS & MITIGAÇÕES

| Risco | Probabilidade | Mitigation |
|---|---|---|
| MCP não funciona bem | 10% | Tem alternativas prontas |
| Claude entende errado dados | 20% | Testar com dados reais early |
| Cliente não quer participar | 30% | Use dados próprios pra teste |
| Prompts precisam muitos ajustes | 40% | Iteração rápida, não perfeccionismo |
| n8n não aguenta volume | 5% | Escalável, pronto pra isso |
| Supabase RLS complexo | 15% | Documentação existe, é padrão |

---

## ⏱️ TIMELINE RESUMIDA

- **Semana 1:** FASE 0-1 (Setup + MCPs)
- **Semana 2:** FASE 2-3 (Dados + Claude)
- **Semana 3:** FASE 4-5 (Execução + Criativos)
- **Semana 4:** FASE 6 (Validação CRÍTICA)
- **Semana 5:** FASE 7 (Dashboard)
- **Semana 6:** FASE 8 (Multi-tenant)
- **Semana 7:** FASE 9-10 (Billing + Polish)

**TOTAL: 7 semanas = MVP vendável**

---

## 📞 Próximos Passos

1. Leia `phase_0/CHECKLIST.md`
2. Comece FASE 0 hoje
3. Atualizar `daily_progress.md` com progresso
4. Seguir DAG sequencialmente

---

**Boa sorte! 🚀**
