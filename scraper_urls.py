import time
from playwright.sync_api import sync_playwright

TARGET_URLS = [
    "https://pirlotv.la/",
    "https://www.pirlotv.world/",
    "https://tarjetarojahd.com.co/chile/",
    "https://tarjetarojatv.sale/",
    "https://www.gacetamapfre.com.mx/",
    "https://tarjetarojahd.com.co/chile/",
    "https://futbollibretv.sx/",
    "https://librefutbol.vip/",
    "https://futbollibre.mx/",
    "https://librefutbol.vip/",
    "https://goluchas.com/tag/lucha-en-vivo/",
]

def capture_api_endpoints(target_url):
    discovered_urls = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ignore_https_errors=True
        )
        page = context.new_page()

        def handle_request(request):
            if request.resource_type in ["fetch", "xhr"] or any(ext in request.url for ext in [".m3u8", ".mpd", ".json", "/api/"]):
                discovered_urls.add((request.method, request.url))

        page.on("request", handle_request)

        try:
            page.goto(target_url, timeout=30000, wait_until="domcontentloaded")
            time.sleep(8)
        except Exception as e:
            print(f"Error en {target_url}: {e}")
        finally:
            browser.close()

    return discovered_urls

if __name__ == "__main__":
    for site in TARGET_URLS:
        urls = capture_api_endpoints(site)
        print(f"\n--- PETICIONES DETECTADAS EN {site} ---")
        for method, url in urls:
            print(f"[{method}] {url}")