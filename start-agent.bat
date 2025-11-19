@echo off
setlocal enabledelayedexpansion
title Agent.exe - Claude Computer Control

echo ==========================================
echo   Agent.exe - Automatic Setup ^& Run
echo ==========================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM 1. Check Node.js
echo Verificando Node.js...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [91m✗[0m Node.js no esta instalado
    echo.
    echo Por favor instala Node.js desde: https://nodejs.org/
    echo Recomendamos la version LTS ^(v20 o superior^)
    echo.
    pause
    exit /b 1
)

REM Get Node.js version
for /f "tokens=1" %%v in ('node -v') do set NODE_VERSION=%%v
for /f "tokens=1 delims=.v" %%v in ("%NODE_VERSION%") do set NODE_MAJOR=%%v

if %NODE_MAJOR% lss 14 (
    echo [91m✗[0m Node.js %NODE_VERSION% es demasiado antiguo
    echo.
    echo Este proyecto requiere Node.js v14 o superior
    echo Tu version actual: %NODE_VERSION%
    echo.
    echo Por favor actualiza Node.js desde: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo [92m✓[0m Node.js encontrado: %NODE_VERSION%
echo.

REM 2. Check npm
echo Verificando npm...
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [91m✗[0m npm no esta instalado
    pause
    exit /b 1
)

for /f "tokens=1" %%v in ('npm -v') do set NPM_VERSION=%%v
echo [92m✓[0m npm encontrado: %NPM_VERSION%
echo.

REM 3. Create .env if not exists
echo Configurando archivo .env...
if not exist ".env" (
    echo [93m⚠[0m Archivo .env no encontrado, creando uno nuevo...
    (
        echo ANTHROPIC_API_KEY=
    ) > .env
    echo [92m✓[0m Archivo .env creado
    echo [93m⚠[0m IMPORTANTE: Debes configurar tu ANTHROPIC_API_KEY en el archivo .env o en la interfaz de la aplicacion
) else (
    echo [92m✓[0m Archivo .env ya existe
)
echo.

REM 4. Check and install dependencies
echo Verificando dependencias de Node.js...
if not exist "node_modules" (
    echo [93m⚠[0m Dependencias no encontradas, instalando...
    call npm install
    if %errorlevel% neq 0 (
        echo [91m✗[0m Error al instalar dependencias
        pause
        exit /b 1
    )
    echo [92m✓[0m Dependencias instaladas
) else (
    echo [92m✓[0m Dependencias encontradas
    REM Check if package.json is newer than node_modules
    for %%F in (package.json) do set PACKAGE_TIME=%%~tF
    for %%F in (node_modules) do set MODULES_TIME=%%~tF
    if "!PACKAGE_TIME!" gtr "!MODULES_TIME!" (
        echo [93m⚠[0m package.json se actualizo, reinstalando dependencias...
        call npm install
        echo [92m✓[0m Dependencias actualizadas
    )
)
echo.

REM 5. Clean broken symlinks (Windows specific)
echo Limpiando enlaces rotos...
if exist "src\node_modules" (
    if not exist "src\node_modules\*" (
        rmdir "src\node_modules" 2>nul
    )
)
if exist ".erb\node_modules" (
    if not exist ".erb\node_modules\*" (
        rmdir ".erb\node_modules" 2>nul
    )
)
echo [92m✓[0m Enlaces verificados
echo.

REM 6. Check port 1212
echo Verificando puerto 1212...
netstat -ano | findstr ":1212" >nul 2>nul
if %errorlevel% equ 0 (
    echo [93m⚠[0m Puerto 1212 ocupado, liberando...
    for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":1212"') do (
        taskkill /F /PID %%p >nul 2>nul
    )
    timeout /t 1 /nobreak >nul
    echo [92m✓[0m Puerto liberado
) else (
    echo [92m✓[0m Puerto disponible
)
echo.

REM 7. Start the application
echo ==========================================
echo   Iniciando Agent.exe...
echo ==========================================
echo.
echo [92m✓[0m La aplicacion se esta iniciando...
echo.
echo Presiona Ctrl+C para detener el agente
echo.

call npm start

if %errorlevel% neq 0 (
    echo.
    echo [91m✗[0m Error al iniciar la aplicacion
    pause
    exit /b 1
)
