@echo off
REM ============================================================================
REM ADS CORE MVP - Demo Local Script
REM Sobe Docker Compose + n8n + PostgreSQL + React Frontend
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo 🚀 INICIANDO ADS CORE MVP - MODO DEMO
echo ============================================================================
echo.

REM Mudar pra pasta do projeto
cd /d "%~dp0"
if errorlevel 1 (
    echo ❌ Erro: Nao conseguiu mudar pra pasta do projeto
    pause
    exit /b 1
)

echo 📦 Iniciando containers Docker (n8n, PostgreSQL, Redis, Adminer)...
echo.
docker-compose up -d

if errorlevel 1 (
    echo ❌ Erro ao rodar docker-compose. Verifique se Docker esta instalado.
    pause
    exit /b 1
)

echo.
echo ✅ Containers iniciados! Aguardando stabilizacao (30 segundos)...
timeout /t 30 /nobreak

echo.
echo ============================================================================
echo 📊 STATUS DOS CONTAINERS
echo ============================================================================
docker-compose ps
echo.

echo.
echo ============================================================================
echo 🎯 ACESSOS DISPONIVEIS
echo ============================================================================
echo.
echo 📋 n8n (Workflows):
echo    URL: http://localhost:5678
echo    Usuario: admin
echo    Senha: changeme
echo.
echo 🗄️  Adminer (Banco de Dados):
echo    URL: http://localhost:8080
echo    Usuario: postgres
echo    Senha: postgres
echo    Servidor: postgres
echo    Banco: ads_core_db
echo.
echo 💾 PostgreSQL:
echo    Host: localhost:5432
echo    Usuario: postgres
echo    Senha: postgres
echo.
echo 🔴 Redis:
echo    Host: localhost:6379
echo.

echo.
echo ============================================================================
echo 🎨 INICIANDO FRONTEND REACT
echo ============================================================================
echo.

cd src\frontend

REM Verificar se node_modules existe
if not exist "node_modules" (
    echo 📥 Instalando dependencias npm (primeira vez)...
    call npm install
    if errorlevel 1 (
        echo ❌ Erro ao instalar npm. Verifique sua conexao.
        pause
        exit /b 1
    )
)

echo.
echo 🎬 Iniciando React Dev Server...
echo 💻 Dashboard estara disponivel em: http://localhost:3000
echo.
call npm start

pause
