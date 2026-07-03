# FASE 0: SETUP BÁSICO

**Duração:** Dias 1-3 (3-5 dias)  
**Objetivo:** Preparar ambiente e credenciais  
**Status:** ⏳ TODO

---

## ✅ Checklist de Execução

### 1️⃣ Definir Cliente de Teste

**Prazo:** Dia 1

- [ ] Escolher cliente:
  - [ ] Próprio negócio, OU
  - [ ] Amigo/conhecido que topa testar, OU
  - [ ] Dados fictícios pra testes iniciais
  
- [ ] Coletar informações:
  - [ ] Nome do cliente: ________________
  - [ ] Nicho: ________________
  - [ ] Orçamento mensal estimado: R$ ________
  - [ ] Objetivo (leads/vendas/awareness): ________________

- [ ] Meta Ads:
  - [ ] Business Account ID: ________________
  - [ ] Consegue autenticar: ✅ SIM / ❌ NÃO
  - [ ] Campanhas ativas: ______ (mínimo 2)

- [ ] Google Ads:
  - [ ] Customer ID: ________________
  - [ ] Consegue autenticar: ✅ SIM / ❌ NÃO
  - [ ] Campanhas ativas: ______ (mínimo 2)

---

### 2️⃣ Preparar Ambiente Dev

**Prazo:** Dias 1-2

#### Git
- [ ] Git instalado: `git --version`
- [ ] Git configurado:
  ```bash
  git config --global user.name "Seu Nome"
  git config --global user.email "seu@email.com"
  ```

#### Docker
- [ ] Docker instalado: `docker --version`
- [ ] Docker Desktop rodando (se Mac/Windows)

#### Node.js
- [ ] Node 18+ instalado: `node --version` (deve ser v18+)
- [ ] npm funcionando: `npm --version`

#### Python
- [ ] Python 3.9+ instalado: `python --version`
- [ ] pip funcionando: `pip --version`

#### Pasta do Projeto
- [ ] Pasta criada: `/ADS-CORE-MVP`
- [ ] Git repo inicializado:
  ```bash
  cd ADS-CORE-MVP
  git init
  git add .
  git commit -m "Initial commit: ADS CORE MVP structure"
  ```

#### Editor
- [ ] VS Code instalado (recomendado)
- [ ] Extensões úteis:
  - [ ] Python
  - [ ] Pylance
  - [ ] REST Client
  - [ ] Thunder Client (pra testar APIs)

---

### 3️⃣ Criar Credenciais & Contas

**Prazo:** Dias 1-3

#### Supabase (Banco de Dados)
- [ ] Conta criada: https://supabase.com
- [ ] Projeto criado
- [ ] Credenciais coletadas:
  - [ ] URL: `https://xxxxx.supabase.co`
  - [ ] Key: `eyJhbGc...`
  - [ ] Senha do banco: ________________

#### Claude API (Anthropic)
- [ ] Conta criada: https://console.anthropic.com
- [ ] API Key gerada:
  - [ ] Key: `sk-ant-...`
  - [ ] Quota verificada (bills/usage)

#### Meta Ads (Facebook/Instagram)
- [ ] Facebook Developer account criado
- [ ] App criado em https://developers.facebook.com
- [ ] Business Account conectada
- [ ] Access token gerado:
  - [ ] Token: ________________
  - [ ] Business Account ID: ________________
  - [ ] App ID: ________________
  - [ ] App Secret: ________________

**Como pegar:**
```
Meta → Developers → Meus Aplicativos → Settings → Basic
```

#### Google Ads
- [ ] Google Cloud Console account
- [ ] Google Ads API habilitada
- [ ] Service account criado
- [ ] Credenciais baixadas (JSON)
- [ ] Refresh token gerado:
  - [ ] Developer Token: ________________
  - [ ] Customer ID: ________________
  - [ ] Refresh Token: ________________

**Tutorial:** https://developers.google.com/google-ads/api/docs/first-call/overview

#### Ideogram (Geração de Imagens - Opcional MVP)
- [ ] Conta criada: https://ideogram.ai
- [ ] API Key gerada:
  - [ ] Key: ________________

---

### 4️⃣ Configurar .env

**Prazo:** Dia 3

```bash
# Copiar arquivo
cp .env.example .env

# Abrir e preencher:
# - SUPABASE_URL
# - SUPABASE_KEY
# - CLAUDE_API_KEY
# - META_ACCESS_TOKEN
# - META_BUSINESS_ACCOUNT_ID
# - GOOGLE_ADS_DEVELOPER_TOKEN
# - GOOGLE_ADS_CUSTOMER_ID
# etc...
```

**Verificação:**
```bash
# Testar que .env tá sendo lido
cat .env
# Verificar que não tá no git
cat .gitignore | grep .env
# Deve estar lá
```

---

### 5️⃣ n8n Preparado

**Prazo:** Dia 2-3

Escolha uma opção:

#### Opção A: Docker Local (Recomendado para MVP)
```bash
docker run -it -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=seu_usuario \
  -e N8N_BASIC_AUTH_PASSWORD=sua_senha \
  n8nio/n8n
```

- [ ] n8n rodando em http://localhost:5678
- [ ] Usuário/senha configurados

#### Opção B: Cloud (n8n.cloud)
- [ ] Conta criada
- [ ] Workspace pronto

---

## ✅ Validação Final FASE 0

Quando todos os checkboxes acima estão ✅:

- [ ] Cliente de teste definido
- [ ] Ambiente dev completo
- [ ] Todas as credenciais coletadas
- [ ] .env preenchido
- [ ] n8n funcionando
- [ ] Pronto pra FASE 1

---

## 🚀 Próximo Passo

Quando tudo acima for ✅:

1. Abra `../phase_1/CHECKLIST.md`
2. Comece FASE 1: Conectar APIs

---

## 📝 Anotações

```
Cliente Teste:
_________________________________

Credenciais Coletadas:
- Supabase: ✅ ❌
- Claude: ✅ ❌
- Meta: ✅ ❌
- Google Ads: ✅ ❌
- Ideogram: ✅ ❌ (opcional)

Ambiente Setup:
- Git: ✅ ❌
- Docker: ✅ ❌
- Node.js: ✅ ❌
- Python: ✅ ❌
- n8n: ✅ ❌

Bloqueadores:
_________________________________

Data Início: 2026-07-03
Data Fim Planejada: 2026-07-05
Data Fim Real: ______________
```

---

**Última atualização:** 2026-07-03
