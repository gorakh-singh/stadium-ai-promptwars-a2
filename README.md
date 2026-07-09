<div align="center">

# ⚽ StadiumAI Ops Console

### *Venue Operations Copilot for FIFA World Cup 2026*

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Gemini 2.5 Flash](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev)

> A single-persona, explainable operations tool for **venue staff** — gate stewards, crowd-control officers, security leads, guest-services coordinators, and ops-center shift supervisors working a live FIFA World Cup 2026 match across **48 teams, 104 matches, 16 venues, and 3 host countries** (USA, Canada, Mexico).

</div>

---

## Problem Statement Alignment — Seven Challenge Areas

| Challenge area | Coverage in StadiumAI Ops Console |
|---|---|
| **Crowd management** | Gate capacity dashboard + Safety Priority Matrix in every advisory |
| **Operational intelligence** | Schema-constrained `StaffAdvisory` with mandatory `ReasoningTrace` on every response |
| **Navigation** | Gate redirect and steward-deployment recommendations between zones |
| **Transportation** | Traffic/parking delay signals feed into advisories |
| **Accessibility** | Wheelchair-accessible routing and sensory-friendly zone data in context + `accessibility_note` field |
| **Multilingual assistance** | English, Spanish, and French via `language` parameter and UI switcher |
| **Sustainability** | Waste-bin fill level and shuttle idle-time per zone in `stadium_data.py`, surfaced as operational nudges |

---

## What Changed in This Rebuild

- **One persona only** — Venue Staff Ops Console; Fan/Manager role switcher removed
- **Structured reasoning** — Every advisory includes `factors_considered`, `thresholds_triggered`, `alternatives_rejected`, `confidence`, and `urgency`
- **Multilingual** — `en` / `es` / `fr` with graceful fallback to English
- **Staff authentication** — Bearer token (`STAFF_ACCESS_TOKEN`) on all endpoints except `/api/health`
- **Short-TTL cache** — Identical gate-context + query + language deduplicated for a few seconds
- **Code quality** — Custom exceptions, structured JSON logging, DI via `Depends()`, `mypy --strict` config

---

## Quick Start

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env: set GEMINI_API_KEY and STAFF_ACCESS_TOKEN

python run.py
```

Open **http://localhost:8000** — the Ops Console loads with live simulated stadium data. Use `?token=dev-staff-token` or the default dev token for API calls.

---

## API Surface

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/advisory` | Bearer | Get a reasoning-backed staff recommendation |
| `GET` | `/api/context` | Bearer | Current stadium context snapshot |
| `POST` | `/api/context/refresh` | Bearer | Regenerate simulated sensor data |
| `GET` | `/api/health` | None | Health check |

### Example Advisory Request

```bash
curl -X POST http://localhost:8000/api/advisory \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev-staff-token" \
  -d '{"query": "What should I do about Gate A?", "language": "en"}'
```

### Example Response (abbreviated)

```json
{
  "recommendation": "Redirect incoming Gate A traffic to Gate B...",
  "reasoning": {
    "factors_considered": ["Gate A at 92% (CRITICAL threshold is 90%)"],
    "thresholds_triggered": ["gate_capacity_critical"],
    "alternatives_rejected": ["Full Gate A closure — would strand queue outdoors"],
    "confidence": 0.91,
    "urgency": "critical"
  },
  "suggested_actions": ["Update Gate A redirect signage"],
  "affected_zones": ["Gate A", "Gate B"],
  "accessibility_note": null,
  "context_snapshot": { "...": "..." },
  "timestamp": "2026-07-09T14:30:00+00:00",
  "session_id": "a1b2c3d4-...",
  "language": "en"
}
```

---

## Project Structure

```
src/
├── config.py
├── main.py
├── api/
│   ├── routes.py
│   ├── schemas.py          # ReasoningTrace, StaffAdvisory, UrgencyLevel
│   └── dependencies.py     # DI + staff auth
├── core/
│   ├── gemini_client.py    # Schema-constrained async advisory generation
│   ├── prompt_engine.py    # Single venue-staff system instruction
│   ├── context_manager.py
│   ├── exceptions.py
│   ├── logging_config.py
│   └── i18n.py
├── simulation/
│   └── stadium_data.py     # + sustainability + accessibility signals
└── static/                 # Ops Console UI
```

---

## Development Commands

```bash
# Run tests (fully mocked Gemini — no live API calls)
pytest tests/ -v

# Lint and format
ruff check src tests
black src tests

# Type check
mypy src
```

---

## Security Considerations

| Measure | Implementation |
|---------|---------------|
| **Staff token gate** | `STAFF_ACCESS_TOKEN` validated via Bearer auth on all endpoints except health |
| **No hardcoded secrets** | API key and staff token loaded from `.env` via pydantic-settings |
| **Prompt injection defense** | 7 regex patterns detect and replace injection attempts with `[FILTERED]` |
| **Unicode-aware sanitization** | Input truncated by Unicode character count (not bytes) |
| **Structured output validation** | `confidence` and `urgency` re-validated after Gemini parse |
| **Rate limiting** | Sliding-window: 30 requests/min per IP on `/api/advisory` |
| **Security headers** | `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `X-Request-ID` |
| **CORS** | Configurable allowed origins |
| **Fail-fast config** | Missing `GEMINI_API_KEY` terminates startup with a clear error |

---

## Accessibility

- WCAG-AA measures preserved: ARIA roles, keyboard navigation, `aria-live` regions, focus indicators, reduced motion, forced-colors support
- **Language switcher** — labeled `<select>`, keyboard-operable, announces changes via `aria-live="polite"`
- **Reasoning panel** — real `<button>` with `aria-expanded`, not a clickable `div`
- **Spectator accessibility feature** — advisories can include wheelchair-accessible routing or nearest sensory-friendly zone via `accessibility_note`

---

## License

MIT License.
