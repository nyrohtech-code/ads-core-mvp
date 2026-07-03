# 🚀 Railway Demo Mode - SEM CHAVES

Sistema vai rodar com **DADOS DUMMY** automaticamente quando não tiver env vars configuradas.

---

## ✅ Status Atual

- ✅ Código em GitHub: `nyrohtech-code/ads-core-mvp`
- ✅ Dockerfile criado e commitado
- ✅ Railway project criado: `joyful-wholeness`
- ⏳ Build status: **Aguardando você conferir**

---

## 🎯 Próximas Ações

### 1️⃣ Acesse Railway
```
https://railway.app/project/67062713-96e8-4978-a254-6dc1ce0e880a
```

### 2️⃣ Verifique o Build
- Clique em **"Deployments"**
- Veja se tem um build em progresso ou se completou
- Se tiver erro, veja o log

### 3️⃣ NÃO Configure Env Vars Por Enquanto!
**DEIXE EM BRANCO.** O sistema vai:
- ✅ Usar dados DUMMY de campanhas
- ✅ Usar dados DUMMY de performance
- ✅ Retornar JSON válido sem precisar de tokens

### 4️⃣ Teste a API
Após deploy bem-sucedido, a Railway vai dar uma URL pública (tipo):
```
https://ads-core-mvp-prod-xxxx.railway.app
```

Acesse:
```
GET https://ads-core-mvp-prod-xxxx.railway.app/
```

Deve retornar dados dummy das campanhas.

---

## 📊 O Que o Sistema Faz em Demo Mode

### Campanhas Carregadas (Dummy):
1. **Black Friday** - E-commerce (ACTIVE, LINK_CLICKS)
2. **Lead Gen** - SaaS (ACTIVE, LEAD_GENERATION)  
3. **Retargeting** - E-commerce (PAUSED, CONVERSIONS)

### Performance Fake (Associado):
- Campaign 001: $28.5k spent, 125k impressions, 125 conversions, $85k revenue
- Campaign 002: $12k spent, 45k impressions, 45 conversions, $22.5k revenue
- Campaign 003: $0 spent (paused)

### Métricas Calculadas:
- ROAS (Return on Ad Spend)
- CPA (Cost Per Acquisition)
- CTR (Click Through Rate)
- CPC (Cost Per Click)

---

## 🔍 Como Conferir Se Tá Funcionando

Após deployment, acesse Railway e:

1. **Veja os logs:**
   ```
   [INFO] Iniciando Meta Ads Sync...
   [INFO] Usando DUMMY_CAMPAIGNS_DATA (sem credenciais)
   [INFO] 3 campanhas carregadas
   [INFO] Performance data processado
   [INFO] Dados salvos no Supabase
   ```

2. **Teste a rota:**
   ```
   curl https://ads-core-mvp-prod-xxxx.railway.app/campaigns
   ```
   Retorna JSON com as 3 campanhas dummy.

---

## ⚠️ Limitações (Até Colocar Chaves)

- ❌ Não sincroniza dados REAIS do Meta Ads
- ❌ Não sincroniza dados REAIS do Google Ads
- ❌ Não gera criatives de VERDADE
- ❌ Claude não otimiza campanhas REAIS
- ✅ MAS: Estrutura tá 100% pronta pra receber chaves depois

---

## 🔐 Quando Quiser Ativar Chaves

Basta:

1. Ir em Railway > Variáveis > Add
2. Colocar:
   - `META_ACCESS_TOKEN=xxx`
   - `GOOGLE_ADS_CUSTOMER_ID=xxx`
   - `CLAUDE_API_KEY=xxx`
   - `SUPABASE_URL=xxx`
   - `SUPABASE_KEY=xxx`

3. Sistema vai automaticamente:
   - Detectar que as chaves existem
   - Usar APIs REAIS em vez de dummy data
   - Sincronizar campanhas de VERDADE

---

## 📝 Checklist

- [ ] Acesso Railway e vejo o projeto
- [ ] Build completou com sucesso
- [ ] Deployments mostra "Deployed"
- [ ] URL pública foi gerada
- [ ] Acesso a URL e vejo JSON de campanhas
- [ ] Logs mostram "DUMMY_CAMPAIGNS_DATA"

---

**Tá pronto pra visualizar! Só conferir lá na Railway.** ✨
