# Admin Page Finder

Fast async admin page finder with modern HTTP, discovery, and wordlists.

## Install

```bash
pip install -e .[dev]
```

## Usage

```bash
apf scan https://example.com -w src/admin_page_finder/wordlists/core.txt \
  -c 100 --per-host 10 --rate 50 --timeout 10 \
  --json results.json --csv results.csv \
  --discover --cache .apf-cache.jsonl \
  --proxy http://127.0.0.1:8080 --rotate-ua \
  --header "X-My-Header: value" --cookie "session=abc"
```

- `--discover/--no-discover`: include robots.txt, sitemap.xml, homepage hints
- `--rate/--burst`: global rate limiting
- `--no-verify`, `--no-redirects`, `--proxy`, `--rotate-ua`, `--header`, `--cookie`
- Outputs: human, `--json`, `--csv`

## Wordlists
See `src/admin_page_finder/wordlists/` for stack-specific lists.

## Development
- Lint: `ruff check . && ruff format --check .`
- Test: `pytest -q`
- Pre-commit: `pre-commit install`

## License
MIT
