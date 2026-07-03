# SETUP COMPLETO - ADS CORE MVP

**Este guia detalha como setup cada componente do sistema.**

---

## 📋 Índice

1. [Ambiente Dev](#ambiente-dev)
2. [Supabase](#supabase)
3. [Claude API](#claude-api)
4. [Meta Ads MCP](#meta-ads-mcp)
5. [Google Ads MCP](#google-ads-mcp)
6. [n8n](#n8n)
7. [Verificação Final](#verificação-final)

---

## 🖥️ Ambiente Dev

### Requisitos
- macOS / Linux / Windows 10+
- 10GB de espaço livre
- Conexão internet estável

### Instalar Ferramentas

#### Git
```bash
# macOS
brew install git

# Ubuntu/Debian
sudo apt-get install git

# Windows
# Download: https://git-scm.com/
```

Verificar:
```bash
git --version
# git version 2.x.x
```

#### Docker
```bash
# macOS/Windows
# Download: https://www.docker.com/products/docker-desktop/

# Linux (Ubuntu/Debian)
sudo apt-get install docker.io docker-compose
```

Verificar:
```bash
docker --version
# Docker version 20.x.x
docker ps
# (deve funcionar sem sudo se setup correto)
```

#### Node.js 18+
```bash
# Using nvm (recomendado)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18

# Ou download direto
# https://nodejs.org/
```

Verificar:
```bash
node --version
# v18.x.x ou maior

npm --version
# 9.x.x ou maior
```

#### Python 3.9+
```bash
# macOS
brew install python@3.9

# Ubuntu/Debian
sudo apt-get install python3.9 python3-pip

# Windows
# Download: https://www.python.org/
```

Verificar:
```bash
python3 --version
# Python 3.9.x ou maior

pip3 --version
# pip 21.x.x ou maior
```

#### VS Code (Opcional mas Recomendado)
```bash
# macOS
brew install --cask visual-studio-code

# Ou download: https://code.visualstudio.com/
```

Extensões recomendadas:
- Python
- Pylance
- REST Client
- Thunder Client
- Git Graph

---

## 🗄️ Supabase

### Criar Projeto

1. Ir para https://supabase.com
2. Sign Up / Login
3. "New Project"
4. Escolher:
   - **Name:** `ads-core-mvp`
   - **Database Password:** Gerar senha forte (salvar!)
   - **Region:** Escolher próximo a você (ex: São Paulo)
5. Criar

### Coletar Credenciais

Na dashboard do projeto:

```
Settings → API → URL
Copiar: https://xxxxx.supabase.co
```

```
Settings → API → anon public
Copiar: eyJhbGci...
```

```
Settings → Database → Password
(A senha que você criou ao iniciar)
```

Adicionar ao `.env`:
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGci...
SUPABASE_DB_PASSWORD=sua_senha
```

### Criar Tabelas

```sql
-- Copiar todo esse SQL do arquivo:
-- config/supabase_schema.sql
-- E rodar na console do Supabase (SQL Editor)
```

Verificar:
```bash
# Depois de rodar SQL, verificar que tabelas foram criadas
# Supabase Dashboard → Table Editor
# Deve ter: clients, campaigns, creatives, performance_logs, ai_decisions
```

---

## 🤖 Claude API

### Criar Conta & Chave

1. Ir para https://console.anthropic.com
2. Sign Up / Login
3. "API Keys" (menu esquerdo)
4. "Create Key"
5. Nome: `ads-core-mvp`
6. Copiar

Adicionar ao `.env`:
```
CLAUDE_API_KEY=sk-ant-xxxxx...
```

### Verificar Acesso

```bash
# Testar depois (FASE 3)
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $CLAUDE_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Olá"}]
  }'
```

---

## 📱 Meta Ads MCP

### Setup Inicial

1. Ir para https://developers.facebook.com
2. "My Apps" → "Create App"
3. App Name: `ads-core-mvp`
4. App Type: `Business`
5. Criar

### Gerar Access Token

No app criado:
```
Settings → Basic → Copy App ID, App Secret
```

Usar esse comando para gerar token:
```bash
# Substituir {APP_ID} e {APP_SECRET}
curl -X GET "https://graph.facebook.com/oauth/access_token?client_id={APP_ID}&client_secret={APP_SECRET}&grant_type=client_credentials"
```

Resposta terá:
```json
{
  "access_token": "EAAGxxxxx...",
  "token_type": "bearer"
}
```

### Coletar Credenciais

```
Business Account ID:
  Facebook → Settings → Business Settings → Info → ID
```

Adicionar ao `.env`:
```
META_ACCESS_TOKEN=EAAGxxxxx...
META_BUSINESS_ACCOUNT_ID=123456789
META_APP_ID=seu_app_id
META_APP_SECRET=seu_app_secret
```

### Instalar MCP

```bash
cd src/mcp
git clone https://github.com/pipeboard-co/meta-ads-mcp.git
cd meta-ads-mcp
npm install
```

Testar:
```bash
# Ver se MCP consegue conectar
# Faz depois na FASE 1
```

---

## 🔍 Google Ads MCP

### Criar Service Account

1. Ir para https://console.cloud.google.com
2. Criar novo projeto: `ads-core-mvp`
3. Habilitar "Google Ads API"
4. Criar "Service Account"
   - Email: `ads-core@ads-core-mvp.iam.gserviceaccount.com`
   - Role: `Editor`
5. Criar JSON key (Download)

### Conectar Google Ads

1. Ir para https://ads.google.com
2. Tools & Settings → Linked Accounts → Linked Google Cloud
3. Link a service account (copiar email do passo anterior)

### Gerar Refresh Token

```bash
# Isso é mais complexo, vide documentação Google:
# https://developers.google.com/google-ads/api/docs/first-call/overview
```

Basicamente:
1. Auth flow OAuth pra ter refresh token
2. Salvar refresh token

Adicionar ao `.env`:
```
GOOGLE_ADS_DEVELOPER_TOKEN=ABCDEFGHIJKLMNOPQRSTUVWxyz
GOOGLE_ADS_CLIENT_ID=seu_client_id.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=seu_client_secret
GOOGLE_ADS_REFRESH_TOKEN=1//0xxxxx...
GOOGLE_ADS_CUSTOMER_ID=1234567890
```

### Instalar MCP

```bash
cd src/mcp
git clone https://github.com/cohnen/mcp-google-ads.git
cd mcp-google-ads
npm install
```

---

## 🚀 n8n

### Docker Setup (Recomendado)

```bash
# Criar volume pra persistência
docker volume create n8n_data

# Rodar container
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=seu_usuario \
  -e N8N_BASIC_AUTH_PASSWORD=sua_senha \
  -e DB_TYPE=postgresql \
  -e DB_POSTGRESDB_HOST=host.docker.internal \
  -e DB_POSTGRESDB_PORT=5432 \
  -e DB_POSTGRESDB_DATABASE=n8n \
  -e DB_POSTGRESDB_USER=n8n_user \
  -e DB_POSTGRESDB_PASSWORD=n8n_password \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```

Ou mais simples:
```bash
docker run -it -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=seu_usuario \
  -e N8N_BASIC_AUTH_PASSWORD=sua_senha \
  n8nio/n8n
```

### Acessar

Ir para: http://localhost:5678

Login com credenciais que você criou

### Cloud Setup (Alternativa)

1. Ir para https://n8n.cloud
2. Sign Up
3. Workspace pronto pra usar

---

## ✅ Verificação Final

Rodar esse script pra verificar se tudo tá conectado:

```bash
#!/bin/bash

echo "🔍 Verificando Setup..."

# 1. Verificar ambiente
echo "✓ Node.js:" $(node --version)
echo "✓ Python:" $(python3 --version)
echo "✓ Docker:" $(docker --version)

# 2. Verificar .env
if [ -f .env ]; then
  echo "✓ .env encontrado"
  # Verificar se tá preenchido (não mostrar valores)
  if grep -q "CLAUDE_API_KEY" .env; then
    echo "  ✓ CLAUDE_API_KEY configurado"
  fi
  if grep -q "SUPABASE_URL" .env; then
    echo "  ✓ SUPABASE_URL configurado"
  fi
else
  echo "✗ .env não encontrado!"
fi

# 3. Verificar se MCPs tão clonados
if [ -d "src/mcp/meta-ads-mcp" ]; then
  echo "✓ Meta MCP clonado"
else
  echo "✗ Meta MCP não clonado"
fi

if [ -d "src/mcp/mcp-google-ads" ]; then
  echo "✓ Google MCP clonado"
else
  echo "✗ Google MCP não clonado"
fi

# 4. Verificar n8n
if docker ps | grep -q n8n; then
  echo "✓ n8n container rodando"
else
  echo "⚠ n8n container não está rodando"
fi

# 5. Verificar Supabase
echo ""
echo "📋 Próximos passos:"
echo "  1. Verifique que Supabase tá rodando (dashboard online)"
echo "  2. Verifique que Claude API key está válida"
echo "  3. Verifique que Meta/Google credenciais estão corretos"
echo "  4. Comece FASE 1!"

echo ""
echo "✅ Setup verificado!"
```

Salvar em `scripts/verify_setup.sh` e rodar:

```bash
chmod +x scripts/verify_setup.sh
./scripts/verify_setup.sh
```

---

## 🆘 Troubleshooting

### Docker não roda
```bash
# Verificar se Docker tá instalado
docker --version

# Se não tá, instalar: https://docker.com

# No Linux, pode precisar:
sudo usermod -aG docker $USER
# Depois fazer logout e login novamente
```

### Python não encontrado
```bash
# Pode ser python vs python3
python3 --version
pip3 --version

# Se ainda não funcionar:
# macOS: brew install python@3.9
# Linux: sudo apt-get install python3.9
```

### Supabase connection error
```bash
# Verificar credenciais em .env
# Verificar URL: deve ser https://xxxxx.supabase.co
# Verificar que projeto está "Active" no dashboard
```

### n8n não abre
```bash
# Verificar que container está rodando
docker ps | grep n8n

# Se não, reiniciar
docker start n8n

# Ou logs
docker logs n8n
```

---

## 📝 Anotações Finais

- Todas as credenciais devem estar em `.env` (nunca commit!)
- `.env` já tá em `.gitignore`
- Depois de setup, vá pra `../phase_0/CHECKLIST.md`
- Qualquer dúvida, Google é seu amigo 🔍

---

**Última atualização:** 2026-07-03
