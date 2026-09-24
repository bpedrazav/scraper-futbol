# scraper-futbol

Conjunto de scripts en Python para explorar y extraer, con fines educativos, información sobre agendas de eventos de fútbol y endpoints de red (APIs, streams `.m3u8`/`.mpd`) usados por sitios que retransmiten partidos.

> ⚠️ **Aviso legal**: este proyecto interactúa con sitios de terceros que en muchos casos retransmiten contenido deportivo sin licencia. El uso de estos scripts para acceder, distribuir o consumir contenido protegido por derechos de autor sin autorización puede infringir la ley y los términos de servicio de dichos sitios. Este repositorio se documenta con fines técnicos/educativos; el autor y quien lo use son responsables del uso que le den.

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `scraper_rojadirecta.py` | Consulta la API JSON de `agenda18.com` para obtener la agenda de partidos del día, y decodifica (base64) las URLs de los canales/streams embebidos en cada evento. |
| `scraper_urls.py` | Usa Playwright para navegar por una lista de sitios de streaming y capturar, mediante interceptación de peticiones de red, las URLs de tipo `fetch`/`xhr`, `.m3u8`, `.mpd` o `/api/` que estos sitios cargan en segundo plano. |

## Requisitos

- Python 3.8+
- Dependencias:
  - [`requests`](https://pypi.org/project/requests/) (usado por `scraper_rojadirecta.py`)
  - [`playwright`](https://playwright.dev/python/) (usado por `scraper_urls.py`)

## Instalación

```bash
git clone https://github.com/bpedrazav/scraper-futbol.git
cd scraper-futbol

# Se recomienda usar un entorno virtual
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

pip install requests playwright
playwright install chromium
```

## Uso

### 1. Agenda de eventos (`scraper_rojadirecta.py`)

Obtiene la agenda de partidos del día y, para cada evento, lista los canales disponibles junto con la URL decodificada del stream embebido.

```bash
python scraper_rojadirecta.py
```

Salida esperada (ejemplo):

```
=== AGENDA DE EVENTOS ACTUALIZADA (N partidos) ===

  Equipo A vs Equipo B [20:00]
    └─ Canal 1: https://ejemplo.com/embed/...
    └─ Canal 2: https://ejemplo.com/embed/...
------------------------------------------------------------
```

### 2. Detección de endpoints (`scraper_urls.py`)

Recorre una lista predefinida de sitios (`TARGET_URLS`, editable dentro del script) con un navegador headless (Chromium vía Playwright) y muestra en consola todas las peticiones de red relevantes detectadas (APIs, `.m3u8`, `.mpd`, etc.) durante los primeros segundos de carga de cada página.

```bash
python scraper_urls.py
```

Salida esperada (ejemplo):

```
--- PETICIONES DETECTADAS EN https://ejemplo.com/ ---
[GET] https://ejemplo.com/api/stream.json
[GET] https://ejemplo.com/live/playlist.m3u8
```

Para modificar los sitios analizados, edita la lista `TARGET_URLS` al inicio de `scraper_urls.py`.

## Cómo funciona

- **`scraper_rojadirecta.py`**
  1. Hace una petición GET a `https://agenda18.com/agenda.json` (con un parámetro de cache-busting).
  2. Recorre el JSON de respuesta extrayendo título, hora y canales (`embeds`) de cada evento.
  3. Cada canal trae un `embed_iframe` cuya URL real viene codificada en base64 dentro del parámetro `?r=`; la función `decode_b64_url` la decodifica.

- **`scraper_urls.py`**
  1. Lanza un navegador Chromium headless con Playwright.
  2. Para cada URL de `TARGET_URLS`, se suscribe al evento `request` de la página.
  3. Filtra las peticiones de tipo `fetch`/`xhr` o cuya URL contenga `.m3u8`, `.mpd`, `.json` o `/api/`.
  4. Tras esperar unos segundos a que cargue la página, cierra el navegador y muestra las URLs detectadas.

## Limitaciones conocidas

- Los scripts dependen de la estructura HTML/JSON actual de los sitios objetivo; si estos cambian su diseño o API, el scraping puede dejar de funcionar.
- No hay manejo de reintentos, rotación de user-agents/proxies, ni control de rate-limiting.
- `scraper_urls.py` usa un `time.sleep(8)` fijo, lo que puede ser insuficiente o excesivo según el sitio.

## Contribuciones

Actualmente es un proyecto personal sin flujo de contribución definido. Si quieres proponer cambios, puedes abrir un *issue* o *pull request* en el repositorio.

## Licencia

No se especifica licencia en el repositorio. Sin una licencia explícita, todos los derechos quedan reservados por defecto al autor; contacta con el propietario del repositorio si necesitas permisos de uso, distribución o modificación.
