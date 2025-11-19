#!/bin/bash

# Agent.exe - Setup and Run Script
# Este script configura automáticamente el entorno y ejecuta el agente

# No usar set -e para que no se cierre la terminal en caso de error

# Cambiar al directorio donde está el script
cd "$(dirname "$0")"

# Cargar conda si existe
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
    conda activate base 2>/dev/null || true
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
    conda activate base 2>/dev/null || true
fi

# Cargar nvm si existe
if [ -f "$HOME/.nvm/nvm.sh" ]; then
    source "$HOME/.nvm/nvm.sh"
fi

echo "=========================================="
echo "  Agent.exe - Automatic Setup & Run"
echo "=========================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# 1. Verificar Node.js
echo "Verificando Node.js..."
if ! command -v node &> /dev/null; then
    print_error "Node.js no está instalado"
    echo ""
    echo "Intentando instalar Node.js automáticamente..."
    
    # Intentar instalar con conda si está disponible
    if command -v conda &> /dev/null; then
        print_warning "Instalando Node.js 20 con conda..."
        conda install -c conda-forge nodejs=20 -y
        if [ $? -eq 0 ]; then
            print_status "Node.js instalado correctamente"
        else
            print_error "No se pudo instalar Node.js con conda"
            echo "Por favor instala Node.js manualmente desde https://nodejs.org/"
            read -p "Presiona Enter para cerrar..."
            exit 1
        fi
    else
        print_error "No se encontró conda para instalar Node.js automáticamente"
        echo "Por favor instala Node.js desde https://nodejs.org/"
        read -p "Presiona Enter para cerrar..."
        exit 1
    fi
fi

NODE_VERSION=$(node -v)
NODE_MAJOR_VERSION=$(node -v | cut -d'.' -f1 | sed 's/v//')

if [ "$NODE_MAJOR_VERSION" -lt 14 ]; then
    print_error "Node.js $NODE_VERSION es demasiado antiguo"
    echo ""
    echo "Este proyecto requiere Node.js v14 o superior"
    echo "Tu versión actual: $NODE_VERSION"
    echo ""
    
    # Intentar actualizar automáticamente si hay conda
    if command -v conda &> /dev/null; then
        print_warning "Actualizando Node.js a versión 20..."
        conda install -c conda-forge nodejs=20 -y
        if [ $? -eq 0 ]; then
            print_status "Node.js actualizado correctamente"
            NODE_VERSION=$(node -v)
        else
            print_error "No se pudo actualizar Node.js"
            echo "Por favor actualiza manualmente:"
            echo "  - Descarga desde: https://nodejs.org/"
            echo "  - O ejecuta: conda install -c conda-forge nodejs=20 -y"
            read -p "Presiona Enter para cerrar..."
            exit 1
        fi
    else
        print_error "No se puede actualizar automáticamente sin conda"
        echo "Por favor actualiza Node.js:"
        echo "  - Descarga desde: https://nodejs.org/"
        echo "  - O usa nvm: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash"
        echo "    Luego ejecuta: nvm install 20 && nvm use 20"
        read -p "Presiona Enter para cerrar..."
        exit 1
    fi
fi

print_status "Node.js encontrado: $NODE_VERSION"
echo ""

# 2. Verificar npm
echo "Verificando npm..."
if ! command -v npm &> /dev/null; then
    print_error "npm no está instalado"
    read -p "Presiona Enter para cerrar..."
    exit 1
fi
NPM_VERSION=$(npm -v)
print_status "npm encontrado: $NPM_VERSION"
echo ""

# 3. Crear archivo .env si no existe
echo "Configurando archivo .env..."
if [ ! -f ".env" ]; then
    print_warning "Archivo .env no encontrado, creando uno nuevo..."
    cat > .env << 'EOF'
ANTHROPIC_API_KEY=
EOF
    print_status "Archivo .env creado"
    print_warning "IMPORTANTE: Debes configurar tu ANTHROPIC_API_KEY en el archivo .env o en la interfaz de la aplicación"
else
    print_status "Archivo .env ya existe"
fi
echo ""

# 4. Verificar e instalar dependencias
echo "Verificando dependencias de Node.js..."
if [ ! -d "node_modules" ]; then
    print_warning "Dependencias no encontradas, instalando..."
    npm install
    print_status "Dependencias instaladas"
else
    print_status "Dependencias encontradas"
    # Verificar si package.json cambió
    if [ "package.json" -nt "node_modules" ]; then
        print_warning "package.json se actualizó, reinstalando dependencias..."
        npm install
        print_status "Dependencias actualizadas"
    fi
fi
echo ""

# 5. Limpiar enlaces simbólicos rotos (fix común en Linux)
echo "Limpiando enlaces simbólicos rotos..."
if [ -L "src/node_modules" ]; then
    if [ ! -e "src/node_modules" ]; then
        print_warning "Enlace roto detectado en src/node_modules, eliminando..."
        rm -f src/node_modules
    fi
fi
if [ -L ".erb/node_modules" ]; then
    if [ ! -e ".erb/node_modules" ]; then
        print_warning "Enlace roto detectado en .erb/node_modules, eliminando..."
        rm -f .erb/node_modules
    fi
fi
print_status "Enlaces verificados"
echo ""

# 6. Matar procesos previos en el puerto 1212
echo "Verificando puerto 1212..."
if lsof -Pi :1212 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_warning "Puerto 1212 ocupado, liberando..."
    lsof -ti:1212 | xargs kill -9 2>/dev/null || true
    sleep 1
    print_status "Puerto liberado"
else
    print_status "Puerto disponible"
fi
echo ""

# 7. Configurar sandbox de Electron (si es necesario)
echo "Configurando Electron..."
CHROME_SANDBOX="node_modules/electron/dist/chrome-sandbox"
if [ -f "$CHROME_SANDBOX" ]; then
    # Verificar si el sandbox necesita configuración
    if [ ! -u "$CHROME_SANDBOX" ]; then
        print_warning "Configurando permisos del sandbox de Electron..."
        sudo chown root:root "$CHROME_SANDBOX" 2>/dev/null && sudo chmod 4755 "$CHROME_SANDBOX" 2>/dev/null
        if [ $? -eq 0 ]; then
            print_status "Sandbox configurado correctamente"
        else
            print_warning "No se pudo configurar el sandbox, usando modo sin sandbox"
            export ELECTRON_DISABLE_SANDBOX=1
        fi
    else
        print_status "Sandbox ya configurado"
    fi
else
    print_status "Electron configurado"
fi
echo ""

# 8. Iniciar la aplicación
echo "=========================================="
echo "  Iniciando Agent.exe..."
echo "=========================================="
echo ""
print_status "La aplicación se está iniciando..."
echo ""
echo "Presiona Ctrl+C para detener el agente"
echo ""

npm start

# Mantener la terminal abierta si hay error
if [ $? -ne 0 ]; then
    echo ""
    echo "=========================================="
    echo "  Hubo un error al iniciar la aplicación"
    echo "=========================================="
    echo ""
    read -p "Presiona Enter para cerrar..."
fi
