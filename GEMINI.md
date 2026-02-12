# Project Context: High-Performance Video CMS (API-First)

## 1. Project Overview
A lightweight, Python-based Video CMS designed to replace bloated systems like Maccms.
**Core Philosophy:**
- **Zero Bloat:** No internal messaging, no social networking features, no complex membership tiers unless requested.
- **API-Centric Ingestion:** The primary source of content is external resource APIs (e.g., Caobizy, Maccms-compatible APIs).
- **Performance:** Async tasks for data syncing; aggressive caching for frontend read operations.

## 2. Tech Stack & Tools
- **Language:** Python 3.12+
- **Framework:** Django 5.x (Async supported)
- **Database:** PostgreSQL (Production) / SQLite (Dev)
- **Task Queue:** Celery + Redis (CRITICAL for background API syncing)
- **Frontend:** Django Templates + Tailwind CSS + HTMX (for SPA-like feel without complexity)
- **HTTP Client:** `httpx` (for high-performance async API requests)

## 3. Architecture & App Structure
- `core/`: Settings, WSGI, ASGI, Base Models.
- `apps/videos/`: Database models for `Video`, `Category`, `Episode`.
- `apps/importer/`: Specialized logic to consume external APIs (Caobizy, etc.).
- `apps/dashboard/`: A custom, minimal admin interface for managing imports.

## 4. External API Integration Standards (The "Caobizy" Protocol)
The system must ingest data from Maccms-standard APIs (XML/JSON).
**Target API:** `https://www.caobizy.com/` (and similar resource sites).

### API Handling Rules for Agent:
1.  **Format Handling:** Always check `ac=list` (JSON/XML) responses. Prefer JSON (`ac=videolist&t=&pg=&h=&ids=&wd=`) if available.
2.  **Data Mapping:**
    -   `vod_name` -> `Video.title`
    -   `type_name` -> `Category.name` (Auto-create category if missing)
    -   `vod_pic` -> `Video.thumbnail_url`
    -   `vod_content` -> `Video.description` (Sanitize HTML tags)
    -   `vod_play_url` -> **CRITICAL PARSING REQUIRED**
3.  **URL Parsing Logic:**
    -   External APIs often format links as: `Ep1$https://link.m3u8#Ep2$https://link.m3u8`
    -   **Rule:** Split by `#` for episodes, then split by `$` for `(Label, URL)` tuples.
4.  **Idempotency:** Implement `update_or_create` logic based on the external API's `vod_id` to prevent duplicates.

## 5. Coding Guidelines for Agent
-   **Models:** Use `UUIDField` for primary keys internally, but store `external_id` for API mapping.
-   **Async:** Use `async def` for API fetchers to handle thousands of items quickly.
-   **Error Handling:** If an API image `vod_pic` is 404, use a default placeholder; do not crash the sync.
-   **Logging:** Log every import batch status (Success/Fail counts) to a dedicated `ImportLog` model.

## 6. Sample Data Structure (Expected from API)
```json
{
  "code": 1,
  "msg": "Data list",
  "page": 1,
  "pagecount": 230,
  "limit": 20,
  "total": 4600,
  "list": [
    {
      "vod_id": 12345,
      "vod_name": "Sample Movie",
      "type_id": 2,
      "type_name": "Action",
      "vod_play_from": "m3u8",
      "vod_play_url": "Ep1$[https://example.com/v1.m3u8#Ep2$https://example.com/v2.m3u8](https://example.com/v1.m3u8#Ep2$https://example.com/v2.m3u8)"
    }
  ]
}