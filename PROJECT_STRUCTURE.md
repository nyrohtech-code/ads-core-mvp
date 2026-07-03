# PROJECT STRUCTURE - ADS CORE MVP

**Documentação completa da estrutura de pastas e arquivos.**

---

## 📁 Árvore Completa

```
ADS-CORE-MVP/
│
├── 📄 README.md                    ← Comece aqui! Visão geral do projeto
├── 📄 DAG.md                       ← Plano de execução completo (7 semanas)
├── 📄 PHASE_CHECKLIST.md           ← Acompanhamento de progresso
├── 📄 PROJECT_STRUCTURE.md         ← Este arquivo
├── 📄 ATTRIBUTION.md               ← Créditos dos projetos open source
├── 📄 .gitignore                   ← Git ignore completo
├── 📄 .env.example                 ← Template de credenciais
├── 📄 docker-compose.yml           ← Setup Docker (n8n, PostgreSQL, Redis)
│
├── 📂 docs/                        ← Documentação técnica
│   ├── 📄 SETUP.md                 ← Setup passo a passo
│   ├── 📄 MCP_SETUP.md             ← Setup de MCPs (Meta, Google)
│   ├── 📄 N8N_WORKFLOWS.md         ← Como criar workflows
│   ├── 📄 CLAUDE_PROMPTS.md        ← Prompts e skills
│   ├── 📄 DATABASE.md              ← Schema Supabase
│   └── 📄 TESTING.md               ← Como testar
│
├── 📂 src/                         ← Código fonte
│   ├── 📂 scripts/                 ← Scripts Python/JS
│   │   ├── sync_meta_ads.py        ← FASE 2: Puxar dados Meta
│   │   ├── sync_google_ads.py      ← FASE 2: Puxar dados Google
│   │   ├── claude_analyzer.py      ← FASE 3: Analisar com Claude
│   │   ├── executor.py             ← FASE 4: Executar ações
│   │   ├── creative_generator.py   ← FASE 5: Gerar criativos
│   │   └── verify_setup.sh         ← Script de verificação
│   │
│   ├── 📂 mcp/                     ← Model Context Protocols
│   │   ├── meta-ads-mcp/           ← Pipeboard Meta MCP (clone)
│   │   └── mcp-google-ads/         ← Google Ads MCP (clone)
│   │
│   ├── 📂 frontend/                ← Next.js app (FASE 7)
│   │   ├── pages/
│   │   │   ├── index.js            ← Dashboard
│   │   │   ├── login.js            ← Login
│   │   │   ├── campaigns.js        ← Campanhas
│   │   │   └── timeline.js         ← Timeline de ações
│   │   ├── components/
│   │   ├── lib/
│   │   ├── styles/
│   │   └── package.json
│   │
│   └── 📂 n8n/                     ← Workflows n8n
│       ├── workflow_1_sync.json    ← FASE 2: Puxar dados (cron 24h)
│       ├── workflow_2_execute.json ← FASE 4: Executar ações
│       └── workflow_3_creative.json← FASE 5: Gerar criativos
│
├── 📂 config/                      ← Arquivos de configuração
│   ├── 📄 supabase_schema.sql      ← Schema do banco de dados
│   ├── 📄 mcp_config.json          ← Configuração de MCPs
│   ├── 📄 prompts.json             ← Prompts do Claude
│   └── 📄 n8n_config.json          ← Configuração n8n
│
├── 📂 phase_0/                     ← FASE 0: Setup Básico
│   └── 📄 CHECKLIST.md             ← Checklist da fase
│
├── 📂 phase_1/                     ← FASE 1: Conectar APIs
│   ├── 📄 CHECKLIST.md
│   └── 📄 TEST.md
│
├── 📂 phase_2/                     ← FASE 2: Puxar Dados
│   ├── 📄 CHECKLIST.md
│   └── 📄 TEST.md
│
├── 📂 phase_3/                     ← FASE 3: Cérebro Claude
│   ├── 📄 CHECKLIST.md
│   └── 📄 TEST.md
│
├── 📂 phase_4/                     ← FASE 4: Execução
│   ├── 📄 CHECKLIST.md
│   └── 📄 TEST.md
│
├── 📂 phase_5/                     ← FASE 5: Criativos
│   ├── 📄 CHECKLIST.md
│   └── 📄 TEST.md
│
├── 📂 phase_6/                     ← FASE 6: Validação ⭐
│   └── 📄 CHECKLIST.md
│
├── 📂 phase_7/                     ← FASE 7: Dashboard
│   ├── 📄 CHECKLIST.md
│   └── 📄 DESIGN.md
│
├── 📂 phase_8/                     ← FASE 8: Multi-tenant
│   └── 📄 CHECKLIST.md
│
├── 📂 phase_9/                     ← FASE 9: Billing
│   └── 📄 CHECKLIST.md
│
├── 📂 phase_10/                    ← FASE 10: Polish
│   └── 📄 CHECKLIST.md
│
└── 📂 notes/                       ← Anotações & Learnings
    ├── 📄 daily_progress.md        ← Log de progresso diário
    ├── 📄 learnings.md             ← Insights durante desenvolvimento
    └── 📄 bugs_found.md            ← Bugs e soluções
```

---

## 📖 Guia de Navegação

### 🚀 Para Começar
1. Leia **README.md** (overview)
2. Leia **DAG.md** (plano completo)
3. Siga **phase_0/CHECKLIST.md** (setup)

### 📚 Para Entender Arquitetura
1. **DAG.md** - Entender fluxo
2. **config/supabase_schema.sql** - Banco de dados
3. **docs/MCP_SETUP.md** - Integração de APIs
4. **docs/N8N_WORKFLOWS.md** - Workflows

### 💻 Para Desenvolver
1. **src/scripts/** - Código Python
2. **src/mcp/** - MCPs (clonados)
3. **src/n8n/** - Workflows JSON
4. **src/frontend/** - Interface Next.js

### ✅ Para Acompanhar Progresso
1. **PHASE_CHECKLIST.md** - Status global
2. **notes/daily_progress.md** - Anotações diárias
3. **phase_X/CHECKLIST.md** - Checklist específico da fase

---

## 📝 Arquivos Importantes

### Configuração
| Arquivo | Propósito | Quando Preencher |
|---------|-----------|------------------|
| .env.example | Template de credenciais | FASE 0 |
| .env | Credenciais REAIS | FASE 0 (após exemplo) |
| docker-compose.yml | Setup Docker | FASE 0 (opcional) |
| .gitignore | Ignorar arquivos git | FASE 0 |

### Documentação
| Arquivo | Propósito | Quando Ler |
|---------|-----------|-----------|
| README.md | Overview | Primeira coisa! |
| DAG.md | Plano 7 semanas | Antes de começar |
| SETUP.md | Setup passo a passo | FASE 0 |
| ATTRIBUTION.md | Créditos | Anytime |

### Código
| Arquivo | Fase | Status |
|---------|------|--------|
| sync_meta_ads.py | 2 | TODO |
| sync_google_ads.py | 2 | TODO |
| claude_analyzer.py | 3 | TODO |
| executor.py | 4 | TODO |
| creative_generator.py | 5 | TODO |

---

## 🔄 Fluxo de Trabalho

```
1. Abrir PHASE_CHECKLIST.md
   ↓
2. Seguir fase atual
   ├─ Ler phase_X/CHECKLIST.md
   ├─ Executar tasks
   └─ Atualizar PHASE_CHECKLIST.md
   ↓
3. Documentar progresso
   └─ Escrever em notes/daily_progress.md
   ↓
4. Próxima fase
   └─ Ir pra phase_(X+1)/CHECKLIST.md
```

---

## 📊 Status Atual

```
Total Estrutura: ✅ 100% Pronta
Código Implementado: 🟡 2% (apenas templates)
Documentação: ✅ 100% Completa
Pronto pra Executar: ✅ SIM
```

---

## 🚨 Arquivos Críticos (NÃO DELETAR)

- ❌ **DAG.md** - Plano de execução
- ❌ **PHASE_CHECKLIST.md** - Acompanhamento
- ❌ **docs/SETUP.md** - Setup guia
- ❌ **.env.example** - Template credenciais
- ❌ **docker-compose.yml** - Setup infra

---

## 🔗 Referências Rápidas

### Próximo Passo Imediato
👉 Abrir `phase_0/CHECKLIST.md`

### Se Estiver Perdido
👉 Ler `DAG.md` seção "FASE X"

### Se Tiver Erro
👉 Procurar em `docs/TESTING.md`

### Se Tiver Dúvida
👉 Procurar no arquivo relevante:
- Credenciais → `.env.example`
- MCPs → `docs/MCP_SETUP.md`
- Workflows → `docs/N8N_WORKFLOWS.md`
- Database → `docs/DATABASE.md`
- Prompts → `docs/CLAUDE_PROMPTS.md`

---

**Última atualização:** 2026-07-03  
**Estrutura criada:** ✅ COMPLETA
