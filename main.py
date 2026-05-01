#!/usr/bin/env python3
"""
main.py — Genera presentaciones en Gamma desde la terminal usando la API nativa.

Requiere la variable de entorno GAMMA_API_KEY.

Uso:
    python main.py "Tendencias de IA en finanzas corporativas 2026"
    python main.py "Intro to LLMs" --cards 8 --theme onyx
"""

import argparse
import json
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

# ─── Configuración ───────────────────────────────────────────────────────────

GAMMA_API_URL = "https://public-api.gamma.app/v1.0/generations"

DEFAULTS = {
    "cards": 20,
    "additional_instructions": (
        "Never include any letters, numbers, text, or characters "
        "inside or crossing over the generated images. "
        "All images must be purely visual with no typography or numerals."
    ),
}

# ─── Themes disponibles ──────────────────────────────────────────────────────

KNOWN_THEMES = {
    "anticiparte": "e5ukwaw8omaqad3",
    "base": "xqcf9gpsumijxan",
    "codelco": "xi4k021nm58su1w",
    "fen": "my4gypek52gile2",
    "latam": "lpfa6nm1ieln81w",
    "profesionales-bci": "7lgrn9rh9b940o9",
    "udd-bci": "03na9mukrhgm3tz",
    "udd-ia-2025": "sbg4fcen8eqc7p3",
    "ash": "ash",
    "onyx": "onyx",
    "howlite": "howlite",
    "coal": "coal",
    "slate": "slate",
    "pearl": "pearl",
    "chimney-smoke": "chimney-smoke",
    "chimney-dust": "chimney-dust",
    "consultant": "consultant",
    "commons": "commons",
    "founder": "founder",
    "gleam": "gleam",
    "vortex": "vortex",
    "default-dark": "default-dark",
    "default-light": "default-light",
    "dawn": "dawn",
    "blue-steel": "blue-steel",
    "bonan-hale": "bonan-hale",
    "aurum": "aurum",
    "night-sky": "nightsky",
    "stratos": "stratos",
    "mercury": "mercury",
    "nova": "nova",
}

def get_api_key() -> str:
    if not os.path.exists(".env"):
        print("Warning: Archivo .env no encontrado. Asegúrate de tenerlo configurado.", file=sys.stderr)
    key = os.environ.get("GAMMA_API_KEY", "").strip()
    if not key:
        print("Error: define GAMMA_API_KEY como variable de entorno.", file=sys.stderr)
        sys.exit(1)
    return key

def resolve_theme(name: str) -> str:
    """Resuelve un nombre de theme a su ID."""
    if not name:
        return None
    lower = name.lower().strip()
    if lower in KNOWN_THEMES:
        return KNOWN_THEMES[lower]
    # Si parece un ID (letras y números, longitud > 5), lo usamos tal cual
    if any(c.isdigit() for c in name) and len(name) > 5:
        return name
    # Búsqueda parcial
    matches = [(k, v) for k, v in KNOWN_THEMES.items() if lower in k]
    if len(matches) == 1:
        return matches[0][1]
    return name # Fallback al nombre original

def call_gamma(api_key: str, args: argparse.Namespace) -> dict:
    """Llama a la API nativa de Gamma."""
    
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputText": args.prompt,
        "textMode": "generate",
        "format": "presentation",
        "numCards": args.cards,
        "additionalInstructions": args.additional or DEFAULTS["additional_instructions"]
    }

    theme_id = resolve_theme(args.theme)
    if theme_id:
        payload["themeId"] = theme_id

    # Opciones de texto si se especifican (audiencia, idioma)
    text_options = {}
    if args.write_for:
        text_options["audience"] = args.write_for
    if args.language:
        text_options["language"] = args.language
    
    if text_options:
        payload["textOptions"] = text_options

    try:
        response = requests.post(GAMMA_API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        print(f"Error HTTP {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}", file=sys.stderr)
        sys.exit(1)

def list_themes():
    """Imprime los themes disponibles."""
    print("\nThemes disponibles:")
    print("-" * 45)
    for name, tid in sorted(KNOWN_THEMES.items()):
        print(f"  {name:<25} → {tid}")

def main():
    parser = argparse.ArgumentParser(description="Genera presentaciones en Gamma.")
    parser.add_argument("prompt", nargs="?", help="Temática de la presentación")
    parser.add_argument("--file", help="Ruta a un archivo Markdown para usar como contenido")
    parser.add_argument("--cards", type=int, default=DEFAULTS["cards"], help="Número de slides")
    parser.add_argument("--theme", help="Nombre o ID del theme")
    parser.add_argument("--write-for", help="Audiencia objetivo")
    parser.add_argument("--additional", help="Instrucciones adicionales")
    parser.add_argument("--language", default="es", help="Idioma (default: es)")
    parser.add_argument("--list-themes", action="store_true", help="Listar themes y salir")
    parser.add_argument("--verbose", action="store_true", help="Mostrar respuesta completa")

    args = parser.parse_args()

    if args.list_themes:
        list_themes()
        sys.exit(0)

    # Lógica para determinar el contenido del prompt
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                args.prompt = f.read()
        except Exception as e:
            parser.error(f"Error al leer el archivo {args.file}: {e}")

    if not args.prompt:
        parser.error("Se requiere un prompt o un archivo con --file.")

    if len(args.prompt) > 100000:
        parser.error("El contenido es demasiado largo (máximo 100,000 caracteres).")

    api_key = get_api_key()

    display_prompt = (args.prompt[:50] + "...") if len(args.prompt) > 50 else args.prompt
    print(f"🚀 Generando presentación: \"{display_prompt}\"")
    print(f"   Cards: {args.cards} | Idioma: {args.language}")
    
    result = call_gamma(api_key, args)
    
    if args.verbose:
        print("\n📦 Respuesta:")
        print(json.dumps(result, indent=2))

    if "generationId" in result:
        gen_id = result["generationId"]
        print(f"\n✅ Generación iniciada. ID: {gen_id}")
        print("🔗 Puedes ver el progreso en tu dashboard de Gamma.")
    else:
        print("\n⚠️ Respuesta inesperada de la API.")

if __name__ == "__main__":
    main()