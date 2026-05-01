#!/bin/bash

# Ejemplos de uso para Slide Maker

echo "🚀 Iniciando ejemplos de Slide Maker..."

# 1. Finanzas
echo "Generando ejemplo de Finanzas (FEN)..."
# python main.py "Reporte de Riesgos Q3: Sector Bancario Latam" --theme fen --cards 15 --write-for "Directorio" --dry-run

# 2. IA / Tech
echo "Generando ejemplo de IA (UDD)..."
# python main.py "Introducción a los AI Agents y MCP" --theme udd-ia-2025 --cards 8 --language en --dry-run

# 3. Minería / Corporativo
echo "Generando ejemplo de Minería (Codelco)..."
# python main.py "Optimización de Procesos en Faena" --theme codelco --cards 12 --dry-run

# 4. Desde Archivo Markdown
echo "Generando ejemplo desde archivo .md..."
# python main.py --file mi_contenido.md --theme latam --cards 15 --dry-run

echo "✅ Ejemplos listos. Para ejecutarlos realmente, quita el flag --dry-run."
