# Agent.exe 🤖

Control tu computadora con Claude AI usando computer use.

## 🚀 Inicio Rápido

### Linux / macOS
```bash
./run-agent.sh
```

### Windows
```batch
start-agent.bat
```

O simplemente haz **doble clic** en el archivo correspondiente a tu sistema operativo.

Este script automáticamente:
- ✅ Verifica Node.js y npm
- ✅ Crea el archivo `.env` si no existe
- ✅ Instala todas las dependencias necesarias
- ✅ Limpia problemas comunes de instalación
- ✅ Libera el puerto si está ocupado
- ✅ Inicia la aplicación

## 📋 Requisitos

- **Node.js** v14 o superior ([Descargar aquí](https://nodejs.org/))
- **npm** v7 o superior (viene con Node.js)
- Una **API Key de Anthropic** ([Obtener aquí](https://console.anthropic.com/))

## 🔑 Configurar API Key

Tienes 2 opciones:

### Opción 1: En la interfaz (Recomendado)
Simplemente ejecuta `./run-agent.sh` y pega tu API key en el campo de texto de la aplicación.

chmod +x run-agent.sh

### Opción 2: En archivo .env
Edita el archivo `.env` y agrega tu key:
```
ANTHROPIC_API_KEY=tu-api-key-aqui
```

## 💡 Uso

1. Ejecuta `./run-agent.sh`
2. Ingresa tu API key (si aún no lo has hecho)
3. Escribe qué quieres que haga el agente
4. ¡Observa cómo Claude toma control de tu computadora!

## ⚠️ Advertencias

- El agente puede **controlar completamente tu computadora**
- Úsalo con precaución y supervisa sus acciones
- Claude funciona mejor con **Firefox** instalado

## 📁 Estructura del Proyecto

```
agent.exe/
├── run-agent.sh          # ← Script para Linux/macOS
├── start-agent.bat       # ← Script para Windows
├── .env                  # Configuración de API key
├── package.json          # Dependencias del proyecto
├── src/                  # Código fuente
├── docs/                 # Documentación y recursos
└── scripts/              # Scripts auxiliares
```

## 🛠️ Desarrollo

Si quieres modificar el código:

```bash
npm install              # Instalar dependencias
npm start               # Modo desarrollo
npm run build           # Compilar para producción
npm run package         # Crear ejecutable
```

## 🐛 Solución de Problemas

### Puerto 1212 ocupado
El script lo soluciona automáticamente, pero si persiste:
```bash
pkill -f electron
```

### Error "Cannot read properties of undefined"
Asegúrate de tener la API key configurada correctamente.

### Dependencias rotas
```bash
rm -rf node_modules package-lock.json
npm install
```

## 📝 Licencia

Apache-2.0 - Ver archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Créditos

Proyecto original por [Kyle Corbitt](https://corbt.com)

---

**¿Problemas?** Abre un issue en [GitHub](https://github.com/corbt/agent.exe/issues)
