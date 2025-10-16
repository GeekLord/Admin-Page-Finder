<!-- 4345ba02-9899-48be-a5b1-677247169bec 40f1840a-8f5d-4971-80a3-fbd857fbfdde -->
# Admin Page Finder – Modernization Plan

### Scope

Refactor and enhance `admin-page-finder.py` for Python 3, performance, reliability, and usability. Add async I/O, robust error handling, richer wordlists, and a modern CLI, plus tests, packaging, and CI.

### Key Changes

- **Python 3 migration**: Ensure full compatibility (encoding, `urllib` → modern HTTP, `print`/exceptions, bytes/str boundaries).
- **HTTP client**: Replace legacy requests with `httpx` (sync + async), optional `aiohttp` if preferred.
- **Async/concurrency**: Use `asyncio` with connection pooling, bounded semaphores, and per-host concurrency caps.
- **Error handling & logging**: Structured logging with `logging` (JSON optional), timeouts, retries with backoff and jitter, circuit-breaker-lite for persistently failing hosts.
- **Wordlists**: Curate expanded admin paths for common stacks (PHP, Laravel, Symfony, WordPress, Django, Flask, Rails, Express, Spring, ASP.NET, Strapi, Ghost, Magento, OpenCart, Presta, Drupal, Joomla), and technology-agnostic patterns.
- **CLI/UX**: `typer` CLI with subcommands, colored output, progress bars, quiet/verbose, JSON/CSV output, resume, and cache.
- **Networking controls**: Rate limiting, robots.txt respect toggle, retries, proxy/Tor support, custom headers, user-agent rotation, cookies, redirect policy, TLS opts.
- **Discovery helpers**: Optional sitemap.xml fetch, robots.txt parsing, homepage heuristic extraction, and simple JS-less link discovery.
- **Results**: Save successes/failures, status, timings, content length, redirect chains. Deterministic exits and codes.
- **Quality**: Type hints, `ruff` + `black`, unit/integration tests (pytest), benchmark script, GitHub Actions CI.
- **Packaging**: Project layout with `src/`, `pyproject.toml`, console script entry point `apf`.
- **Docs**: Updated `README.md` with usage examples and tuning guidance.

### Files/Structure

- `src/admin_page_finder/__init__.py`
- `src/admin_page_finder/cli.py` (Typer entry)
- `src/admin_page_finder/scanner.py` (sync/async scanning core)
- `src/admin_page_finder/http.py` (HTTP client wrappers, retries, headers)
- `src/admin_page_finder/wordlists/*.txt` (stack-specific)
- `tests/` (unit + integration)
- `pyproject.toml` (poetry or PEP 621), `ruff.toml`, `README.md`

### Notes

- Concurrency defaults: total=100, per-host=10; timeouts: connect=5s, read=10s; retries=3 with exponential backoff (cap 10s) + jitter.
- Output: stdout human mode, `--json` for machine output, `--csv` for spreadsheets.
- Config precedence: CLI flags > env vars > config file.

### To-dos

- [ ] Migrate codebase fully to Python 3 (syntax, types, encodings)
- [ ] Replace legacy HTTP with httpx client (sync + async, pooling)
- [ ] Implement asyncio-based concurrent scanner with bounded semaphores
- [ ] Add retry with exponential backoff and jitter; circuit-breaker-lite
- [ ] Enforce sane timeouts and redirect policy across requests
- [ ] Add global and per-host rate limiting and concurrency caps
- [ ] Support proxies, Tor, custom headers, cookies, and UA rotation
- [ ] Add robots.txt toggle and sitemap.xml discovery option
- [ ] Implement simple homepage heuristic discovery for admin links
- [ ] Add curated wordlists for popular frameworks and CMSs
- [ ] Implement JSON/CSV outputs with status, timings, sizes, redirects
- [ ] Create modern Typer CLI with flags, profiles, and subcommands
- [ ] Add structured logging with levels and optional JSON format
- [ ] Add on-disk cache and resume capability to skip scanned paths
- [ ] Restructure to src/ layout with modules and entry point
- [ ] Add type hints, ruff and black, and pre-commit config
- [ ] Write unit tests for http, scanner, and CLI
- [ ] Add integration tests against local httpbin/nginx fixtures
- [ ] Add simple benchmark script for sync vs async performance
- [ ] Create pyproject.toml and console script entry point
- [ ] Add GitHub Actions CI for lint, test, and build
- [ ] Revise README with usage, examples, and tuning tips