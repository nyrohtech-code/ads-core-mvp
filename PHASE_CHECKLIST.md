# PHASE CHECKLIST - Acompanhamento de Progresso

**Projeto:** ADS CORE MVP  
**Data Início:** 2026-07-03  
**Timeline:** 6-7 semanas  

---

## 📊 VISÃO GERAL DO PROGRESSO

```
FASE 0: Setup Básico                          [         ] 0%
FASE 1: Conectar APIs                         [         ] 0%
FASE 2: Puxar Dados                           [         ] 0%
FASE 3: Cérebro Claude                        [         ] 0%
FASE 4: Execução                              [         ] 0%
FASE 5: Criativos                             [         ] 0%
FASE 6: Validação Cliente Real                [         ] 0%
FASE 7: Dashboard                             [         ] 0%
FASE 8: Multi-tenant                          [         ] 0%
FASE 9: Billing                               [         ] 0%
FASE 10: Polish                               [         ] 0%
────────────────────────────────────────────────────────
TOTAL PROGRESSO                               [         ] 0%
```

---

## ✅ FASE 0: SETUP BÁSICO (Dias 1-3)

**Status:** ⏳ TODO | 🟡 IN PROGRESS | ✅ DONE

### Task 0.1: Definir Cliente de Teste
- [ ] Escolher cliente real
- [ ] Meta Business Account ID coletado
- [ ] Google Ads Customer ID coletado
- [ ] 2-3 campanhas ativas para teste
- [ ] Acesso às credenciais confirmado

**Responsável:** Thomas  
**Data Início:** 2026-07-03  
**Data Fim Planejada:** 2026-07-04  
**Status:** ⏳ TODO

---

### Task 0.2: Preparar Ambiente Dev
- [ ] Git instalado e configurado
- [ ] Docker instalado
- [ ] Node.js 18+ instalado
- [ ] Python 3.9+ instalado
- [ ] Pasta do projeto criada ✅
- [ ] Git repo inicializado

**Responsável:** Thomas  
**Data Início:** 2026-07-03  
**Data Fim Planejada:** 2026-07-04  
**Status:** ⏳ TODO

---

### Task 0.3: Contas & Credenciais
- [ ] Supabase: conta criada + projeto
- [ ] Claude API key obtida
- [ ] Meta Developer app criado + token
- [ ] Google Ads API key + credentials.json
- [ ] Ideogram API key (opcional)
- [ ] n8n preparado (Docker ou cloud)
- [ ] .env preenchido com dados reais
- [ ] .env.local gitignored

**Responsável:** Thomas  
**Data Início:** 2026-07-03  
**Data Fim Planejada:** 2026-07-05  
**Status:** ⏳ TODO

---

**FASE 0 COMPLETA?** ⏳ Quando todas as tasks estão ✅

---

## 🔌 FASE 1: CONECTAR APIs (Dias 3-9) - PARALELO

**Status:** ⏳ TODO | 🟡 IN PROGRESS | ✅ DONE

### Task 1.1: Meta Ads MCP Setup
- [ ] Repo clonado (pipeboard-co/meta-ads-mcp)
- [ ] npm install executado
- [ ] Token Meta configurado
- [ ] Teste: listar campanhas funciona
- [ ] MCP rodando em localhost
- [ ] Consegue puxar dados reais do cliente teste

**Responsável:** Thomas  
**Data Início:** 2026-07-05  
**Data Fim Planejada:** 2026-07-07  
**Status:** ⏳ TODO  
**Blocker:** Nenhum

---

### Task 1.2: Google Ads MCP Setup
- [ ] Repo clonado (cohnen/mcp-google-ads)
- [ ] Setup executado
- [ ] Credenciais Google configuradas
- [ ] Teste: listar campanhas funciona
- [ ] MCP rodando em localhost
- [ ] Consegue puxar dados reais do cliente teste

**Responsável:** Thomas  
**Data Início:** 2026-07-05  
**Data Fim Planejada:** 2026-07-07  
**Status:** ⏳ TODO  
**Blocker:** Nenhum

---

### Task 1.3: Supabase Setup
- [ ] Projeto Supabase criado
- [ ] Tabelas criadas (vide config/supabase_schema.sql):
  - [ ] clients
  - [ ] campaigns
  - [ ] creatives
  - [ ] performance_logs
  - [ ] ai_decisions
- [ ] RLS configurado
- [ ] CRUD funcionando
- [ ] Conexão string testada

**Responsável:** Thomas  
**Data Início:** 2026-07-05  
**Data Fim Planejada:** 2026-07-07  
**Status:** ⏳ TODO  
**Blocker:** Nenhum

---

**FASE 1 COMPLETA?** ⏳ Quando todas as tasks estão ✅

---

## 📊 FASE 2: PUXAR DADOS (Dias 9-15)

**Status:** ⏳ TODO | 🟡 IN PROGRESS | ✅ DONE

### Task 2.1: Script Sync Meta Ads
- [ ] Arquivo criado: src/scripts/sync_meta_ads.py
- [ ] Lê dados de Meta MCP
- [ ] Calcula métricas (ROAS, CPA, CTR, etc)
- [ ] Salva no Supabase
- [ ] Trata erros gracefully
- [ ] Teste 1x com dados reais

**Responsável:** Thomas  
**Data Início:** 2026-07-09  
**Data Fim Planejada:** 2026-07-11  
**Status:** ⏳ TODO

---

### Task 2.2: Script Sync Google Ads
- [ ] Arquivo criado: src/scripts/sync_google_ads.py
- [ ] Mesmo padrão que Meta
- [ ] Lê dados de Google MCP
- [ ] Salva no Supabase
- [ ] Teste 1x com dados reais

**Responsável:** Thomas  
**Data Início:** 2026-07-09  
**Data Fim Planejada:** 2026-07-11  
**Status:** ⏳ TODO

---

### Task 2.3: n8n Workflow 1 - Sync
- [ ] Workflow criado: src/n8n/workflow_1_sync.json
- [ ] Trigger: Cron 24h (ex: 06:00 UTC)
- [ ] Chama sync_meta_ads.py
- [ ] Chama sync_google_ads.py
- [ ] Logging automático
- [ ] Teste 1x manualmente
- [ ] Workflow exportado em JSON

**Responsável:** Thomas  
**Data Início:** 2026-07-11  
**Data Fim Planejada:** 2026-07-13  
**Status:** ⏳ TODO

---

**FASE 2 COMPLETA?** ⏳ Quando todas as tasks estão ✅

---

## 🧠 FASE 3: CÉREBRO CLAUDE (Dias 15-19)

**Status:** ⏳ TODO | 🟡 IN PROGRESS | ✅ DONE

### Task 3.1: Criar Prompt Principal
- [ ] Prompts coletados (de AgriciDaniel/claude-ads)
- [ ] Prompts coletados (de hayesti54-eng/ai-media-buying-skills)
- [ ] Adaptados pro seu case
- [ ] Arquivo config/prompts.json criado
- [ ] Claude entende dados: TESTADO
- [ ] Retorna JSON válido: TESTADO
- [ ] Teste manual com dados reais do cliente

**Responsável:** Thomas  
**Data Início:** 2026-07-15  
**Data Fim Planejada:** 2026-07-17  
**Status:** ⏳ TODO

---

### Task 3.2: Script Claude Analyzer
- [ ] Arquivo criado: src/scripts/claude_analyzer.py
- [ ] Conecta à Claude API
- [ ] Envia dados + prompt
- [ ] Recebe JSON de ações
- [ ] Retorna estruturado
- [ ] Teste 1x com dados reais

**Responsável:** Thomas  
**Data Início:** 2026-07-17  
**Data Fim Planejada:** 2026-07-19  
**Status:** ⏳ TODO

---

**FASE 3 COMPLETA?** ⏳ Quando todas as tasks estão ✅

---

## ⚡ FASE 4: EXECUÇÃO (Dias 19-26)

**Status:** ⏳ TODO | 🟡 IN PROGRESS | ✅ DONE

### Task 4.1: Script Executor
- [ ] Arquivo criado: src/scripts/executor.py
- [ ] Recebe ações de Claude
- [ ] Executa PAUSE via APIs
- [ ] Executa SCALE via APIs
- [ ] Registra tudo em log
- [ ] Teste 1x com ação real (sandbox se possível)

**Responsável:** Thomas  
**Data Início:** 2026-07-19  
**Data Fim Planejada:** 2026-07-21  
**Status:** ⏳ TODO

---

### Task 4.2: n8n Workflow 2 - Execução
- [ ] Workflow criado: src/n8n/workflow_2_execute.json
- [ ] Recebe ações de Claude
- [ ] Chama executor.py
- [ ] Registra no Supabase
- [ ] Notifica se erro
- [ ] Teste 1x manualmente

**Responsável:** Thomas  
**Data Início:** 2026-07-21  
**Data Fim Planejada:** 2026-07-23  
**Status:** ⏳ TODO

---

### Task 4.3: Integração Completa
- [ ] Workflow 1 (sync) + Workflow 2 (execute) integrados
- [ ] Loop automático 24/7 funcionando
- [ ] Teste COMPLETO 1x com tudo junto
- [ ] Documentação atualizada

**Responsável:** Thomas  
**Data Início:** 2026-07-23  
**Data Fim Planejada:** 2026-07-26  
**Status:** ⏳ TODO

---

**FASE 4 COMPLETA?** ⏳ Quando todas as tasks estão ✅

---

## 🎨 FASE 5: CRIATIVOS (Dias 26-31)

**Status:** ⏳ TODO | 🟡 IN PROGRESS | ✅ DONE

### Task 5.1: Script Creative Generator
- [ ] Arquivo criado: src/scripts/creative_generator.py
- [ ] Recebe trigger (CTR baixo)
- [ ] Claude gera prompt criativo
- [ ] Chama Ideogram API
- [ ] Sobe imagem via Meta MCP
- [ ] Cria novo ad
- [ ] Teste 1x com geração real

**Responsável:** Thomas  
**Data Início:** 2026-07-26  
**Data Fim Planejada:** 2026-07-28  
**Status:** ⏳ TODO

---

### Task 5.2: n8n Workflow 3 - Criativos
- [ ] Workflow criado: src/n8n/workflow_3_creative.json
- [ ] Trigger: IF performance.ctr < threshold
- [ ] Chama creative_generator.py
- [ ] Trata erros
- [ ] Teste 1x

**Responsável:** Thomas  
**Data Início:** 2026-07-28  
**Data Fim Planejada:** 2026-07-30  
**Status:** ⏳ TODO

---

**FASE 5 COMPLETA?** ⏳ Quando todas as tasks estão ✅

---

## 🧪 FASE 6: VALIDAÇÃO CLIENTE REAL (Dias 31-38) ⭐ CRÍTICO

**Status:** ⏳ TODO | 🟡 IN PROGRESS | ✅ DONE

### Task 6.1: Deixar Rodar
- [ ] Sistema 24/7 por 3-5 dias
- [ ] Cliente acompanhando
- [ ] ROAS medido
- [ ] CPA medido
- [ ] Ações da IA documentadas

**Responsável:** Thomas  
**Data Início:** 2026-07-31  
**Data Fim Planejada:** 2026-08-05  
**Status:** ⏳ TODO

---

### Task 6.2: Feedback & Validação
- [ ] Reunião com cliente
- [ ] Feedback coletado:
  - [ ] Confiança nas ações
  - [ ] Satisfação com criativos
  - [ ] Resultados observados
- [ ] Ajustes de prompts se necessário
- [ ] **DECISION: Passar pra FASE 7? SIM/NÃO**

**Responsável:** Thomas  
**Data Início:** 2026-08-05  
**Data Fim Planejada:** 2026-08-07  
**Status:** ⏳ TODO

---

**FASE 6 COMPLETA?** ⏳ ✅ APROVADO pelo cliente

---

## 🎨 FASE 7: DASHBOARD (Dias 38-45)

**Status:** ⏳ TODO | 🟡 IN PROGRESS | ✅ DONE

### Task 7.1: Frontend Next.js
- [ ] Pasta src/frontend criada
- [ ] Next.js app inicializado
- [ ] Página Login criada
- [ ] Página Dashboard criada
- [ ] Página Campanhas criada
- [ ] Página Timeline criada
- [ ] Conectado ao Supabase

**Responsável:** Thomas  
**Data Início:** 2026-08-07  
**Data Fim Planejada:** 2026-08-13  
**Status:** ⏳ TODO

---

**FASE 7 COMPLETA?** ⏳ Quando todas as tasks estão ✅

---

## 👥 FASE 8: MULTI-TENANT (Dias 45-52)

**Status:** ⏳ TODO | 🟡 IN PROGRESS | ✅ DONE

### Task 8.1: Remover Hardcodes
- [ ] Todos os scripts: cliente_id dinâmico
- [ ] Credenciais: vêm de .env ou Supabase
- [ ] Workflows: paramétricos

**Responsável:** Thomas  
**Data Início:** 2026-08-13  
**Data Fim Planejada:** 2026-08-15  
**Status:** ⏳ TODO

---

### Task 8.2: Onboarding de Cliente Novo
- [ ] Fluxo de signup criado
- [ ] OAuth Meta integrado
- [ ] OAuth Google integrado
- [ ] Projeto Supabase criado automaticamente
- [ ] Workflows iniciam automaticamente
- [ ] Teste com cliente 2

**Responsável:** Thomas  
**Data Início:** 2026-08-15  
**Data Fim Planejada:** 2026-08-20  
**Status:** ⏳ TODO

---

**FASE 8 COMPLETA?** ⏳ Quando 2 clientes rodando isolados

---

## 💰 FASE 9: BILLING (Dias 52-56)

**Status:** ⏳ TODO | 🟡 IN PROGRESS | ✅ DONE

### Task 9.1: Stripe Integration
- [ ] Produtos criados no Stripe
- [ ] Checkout integrado
- [ ] Subscriptions configuradas
- [ ] Teste de pagamento

**Responsável:** Thomas  
**Data Início:** 2026-08-20  
**Data Fim Planejada:** 2026-08-22  
**Status:** ⏳ TODO

---

### Task 9.2: Metering & Créditos
- [ ] Sistema de contagem criado
- [ ] Claude calls contadas
- [ ] Ideogram calls contadas
- [ ] Créditos sendo debitados
- [ ] Dashboard mostra uso

**Responsável:** Thomas  
**Data Início:** 2026-08-22  
**Data Fim Planejada:** 2026-08-24  
**Status:** ⏳ TODO

---

**FASE 9 COMPLETA?** ⏳ Quando billing rodando

---

## ✨ FASE 10: POLISH (Dias 56-63)

**Status:** ⏳ TODO | 🟡 IN PROGRESS | ✅ DONE

### Task 10.1: Documentação
- [ ] README finalizado
- [ ] Setup guide escrito
- [ ] FAQ criado
- [ ] Prompts documentados

**Responsável:** Thomas  
**Data Início:** 2026-08-24  
**Data Fim Planejada:** 2026-08-26  
**Status:** ⏳ TODO

---

### Task 10.2: Segurança
- [ ] Audit logs funcionando
- [ ] 2FA habilitado
- [ ] Rate limiting ativo
- [ ] Validações completas

**Responsável:** Thomas  
**Data Início:** 2026-08-24  
**Data Fim Planejada:** 2026-08-28  
**Status:** ⏳ TODO

---

### Task 10.3: Performance
- [ ] Queries otimizadas
- [ ] Caching básico
- [ ] Error handling robusto

**Responsável:** Thomas  
**Data Início:** 2026-08-28  
**Data Fim Planejada:** 2026-08-30  
**Status:** ⏳ TODO

---

### Task 10.4: Tests
- [ ] Tests unitários escritos
- [ ] Tests integração escritos
- [ ] Tudo passando
- [ ] CI/CD básico setup

**Responsável:** Thomas  
**Data Início:** 2026-08-30  
**Data Fim Planejada:** 2026-09-02  
**Status:** ⏳ TODO

---

**FASE 10 COMPLETA?** ⏳ Quando tudo está ✅ e pronto pra vender

---

## 🚀 LAUNCH

**Status:** ⏳ TODO  
**Data Planejada:** 2026-09-02  
**Revisão Final:** Sim

- [ ] Tudo testado
- [ ] Documentação completa
- [ ] 2 clientes satisfeitos
- [ ] Suporte mapeado
- [ ] Preço definido
- [ ] Landing page (opcional)

---

## 📝 NOTAS GERAIS

- Sempre atualize este arquivo com progresso real
- Se bloquear, documente na seção "Blocker"
- Datas são PLANEJADAS, pode mudar
- Prioridade: **FASE 6 (Validação) é crítica**
- Se falhar na FASE 6 → volta pra FASE 3/4 pra debug

---

**Última atualização:** 2026-07-03  
**Próximo review:** Daily (noites, antes de dormir)
