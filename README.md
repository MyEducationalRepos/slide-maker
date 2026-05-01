# Slide Maker 🚀

Generador de presentaciones profesional para **Gamma.app** directamente desde la terminal.

## 🛠 Setup

1. **Instalar dependencias**:
   ```bash
   uv sync
   ```

2. **Configurar API Key**:
   Crea o edita el archivo `.env` en la raíz del proyecto:
   ```env
   GAMMA_API_KEY=sk-gamma-xxxx
   ```

## 📖 CLI Usage

La interfaz básica es:
```bash
python main.py "[PROMPT]" [OPTIONS]
```

### Opciones Disponibles

| Opción | Descripción | Default |
| :--- | :--- | :--- |
| `prompt` | El tema central o descripción de la presentación. | (Requerido*) |
| `--file` | Ruta a un archivo Markdown (.md) para usar como contenido. | `None` |
| `--cards` | Número de slides a generar. | `20` |
| `--theme` | Nombre o ID del theme (ej: `fen`, `onyx`, `latam`). | (Workspace Default) |
| `--write-for` | Define la audiencia objetivo (ajusta el nivel del lenguaje). | `None` |
| `--language` | Código de idioma (ej: `es`, `en`, `pt`). | `es` |
| `--additional`| Instrucciones extra para el motor de IA. | (Anti-text-in-images) |
| `--list-themes`| Lista todos los themes configurados y sus IDs. | - |
| `--verbose` | Muestra la respuesta JSON completa de la API. | - |

> \* Se requiere `prompt` o `--file`.

## 💡 Ejemplos

### 1. Desde un archivo Markdown
```bash
python main.py --file mi_presentacion.md --theme latam --cards 12
```

### 2. Presentación Corporativa (Finanzas)
```bash
python main.py "Reporte de Riesgos Q3: Sector Bancario Latam" \
  --theme fen \
  --cards 15 \
  --write-for "Directorio y C-Level"
```

### 2. Workshop Técnico (Educación)
```bash
python main.py "Introducción a los AI Agents y MCP" \
  --theme udd-ia-2025 \
  --cards 8 \
  --language en \
  --write-for "Estudiantes de Ingeniería" \
  --cards 12
```

## 🔒 Seguridad (Security by Design)

Este proyecto implementa principios de **Security by Design**:

- **Protección de Credenciales**: El archivo `.env` debe tener permisos restringidos (`chmod 600`). El script notificará si detecta permisos demasiado amplios.
- **Validación Estricta**: Uso de **Pydantic** para validar todos los payloads antes de enviarlos a la API de Gamma.
- **Sanitización de Logs**: En modo `--verbose`, las API Keys son automáticamente enmascaradas en la salida de la terminal.
- **Aislamiento de Archivos**: Prevención de ataques de *Path Traversal* al cargar archivos con `--file`.

## 🧪 Tests

Ejecuta las pruebas unitarias para asegurar la integridad del sistema:
```bash
PYTHONPATH=. uv run pytest
```

### 3. Pitch Deck Rápido (Minimalista)
```bash
python main.py "Startup: Marketplace de Energía Renovable" \
  --theme onyx \
  --cards 10
```

### 4. Consultoría de Procesos
```bash
python main.py "Optimización de la Cadena de Suministro" \
  --theme codelco \
  --cards 20 \
  --additional "Enfatizar diagramas de flujo y eficiencia operativa"
```

## 🎨 Themes Especiales
Este CLI incluye atajos para themes institucionales y profesionales:
- `fen`: Facultad de Economía y Negocios
- `codelco`: Estilo corporativo minero
- `anticiparte`: Estilo consultoría premium
- `latam`: Estilo aerolínea/corporativo
- `udd-ia-2025`: Estilo académico vanguardista

Usa `python main.py --list-themes` para ver la lista completa.

---
Desarrollado para propósitos educativos y profesionales.
