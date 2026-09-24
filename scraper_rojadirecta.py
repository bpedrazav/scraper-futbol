import base64
import json
import re
import time
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def decode_b64_url(iframe_path):
    b64_match = re.search(r"\?r=([A-Za-z0-9+/=]+)", iframe_path)
    if b64_match:
        try:
            return base64.b64decode(b64_match.group(1)).decode("utf-8")
        except Exception:
            return None
    return None

def fetch_and_parse_agenda():
    cache_buster = int(time.time())
    api_url = f"https://agenda18.com/agenda.json?v={cache_buster}"

    try:
        response = requests.get(api_url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"Error al conectar con la API: {response.status_code}")
            return

        data = response.json().get("data", [])
        if not data:
            print("No se encontraron eventos en la respuesta.")
            return

        print(f"=== AGENDA DE EVENTOS ACTUALIZADA ({len(data)} partidos) ===\n")

        for event in data:
            attrs = event.get("attributes", {})
            title = attrs.get("diary_description", "Sin título")
            hour = attrs.get("diary_hour", "N/A")
            embeds = attrs.get("embeds", {}).get("data", [])

            print(f" {title} [{hour}]")

            for embed in embeds:
                embed_attrs = embed.get("attributes", {})
                channel_name = embed_attrs.get("embed_name", "Canal")
                iframe_path = embed_attrs.get("embed_iframe", "")

                decoded_url = decode_b64_url(iframe_path)
                if decoded_url:
                    print(f"  └─ {channel_name}: {decoded_url}")
                else:
                    print(f"  └─ {channel_name}: {iframe_path}")

            print("-" * 60)

    except Exception as e:
        print(f"Error en la ejecución: {e}")

if __name__ == "__main__":
    fetch_and_parse_agenda()