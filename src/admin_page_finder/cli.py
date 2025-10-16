import asyncio
import csv
import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress

from .cache import JsonlCache
from .discovery import fetch_homepage_hints, fetch_robots_paths, fetch_sitemap_paths
from .http import AsyncHttpClient
from .logging_utils import configure_logging
from .scanner import scan_admin_paths

app = typer.Typer(help="Admin Page Finder – async scanner for common admin paths")
console = Console()


def _load_wordlist(path: Optional[Path]) -> list[str]:
    if path and path.is_file():
        lines = path.read_text(encoding="utf-8").splitlines()
        return [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    return [
        "admin/",
        "administrator/",
        "wp-admin/",
        "wp-login.php",
        "admin/login.php",
        "login",
    ]


@app.command()
def scan(
    url: str = typer.Argument(..., help="Target base URL or hostname"),
    wordlist: Optional[Path] = typer.Option(
        None,
        "--wordlist",
        "-w",
        exists=True,
        readable=True,
        help="Path to wordlist file",
    ),
    discover: bool = typer.Option(
        True, "--discover/--no-discover", help="Include robots/sitemap/homepage hints"
    ),
    concurrency: int = typer.Option(100, "--concurrency", "-c", help="Max concurrent requests"),
    per_host: int = typer.Option(10, "--per-host", help="Per-host concurrency cap"),
    rate_limit: Optional[float] = typer.Option(
        None, "--rate", help="Global requests per second (float)"
    ),
    rate_burst: int = typer.Option(1, "--burst", help="Token bucket burst capacity"),
    timeout: float = typer.Option(10.0, "--timeout", "-t", help="Request timeout (seconds)"),
    json_out: Optional[Path] = typer.Option(None, "--json", help="Write results JSON to file"),
    csv_out: Optional[Path] = typer.Option(None, "--csv", help="Write results CSV to file"),
    proxy: Optional[str] = typer.Option(
        None, "--proxy", help="Proxy URL (e.g. http://127.0.0.1:8080)"
    ),
    ua: Optional[str] = typer.Option(None, "--user-agent", help="Override User-Agent header"),
    rotate_ua: bool = typer.Option(False, "--rotate-ua", help="Enable User-Agent rotation"),
    header: Optional[list[str]] = typer.Option(
        None, "--header", help="Extra header, repeated: Key: Value"
    ),
    cookie: Optional[list[str]] = typer.Option(
        None, "--cookie", help="Cookie key=value (repeatable)"
    ),
    no_verify: bool = typer.Option(False, "--no-verify", help="Disable TLS verification"),
    no_redirects: bool = typer.Option(False, "--no-redirects", help="Do not follow redirects"),
    cache_file: Optional[Path] = typer.Option(None, "--cache", help="JSONL cache file for resume"),
    log_level: str = typer.Option("INFO", "--log-level", help="Logging level"),
    log_json: bool = typer.Option(False, "--log-json", help="Log in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose progress output"),
):
    configure_logging(log_level, json_mode=log_json)

    base_paths = _load_wordlist(wordlist)

    headers: dict[str, str] = {}
    if ua:
        headers["User-Agent"] = ua
    if header:
        for h in header:
            if ":" in h:
                k, v = h.split(":", 1)
                headers[k.strip()] = v.strip()

    cookies: dict[str, str] = {}
    if cookie:
        for c in cookie:
            if "=" in c:
                k, v = c.split("=", 1)
                cookies[k.strip()] = v.strip()

    cache = JsonlCache(cache_file) if cache_file else None

    with Progress(transient=not verbose) as progress:
        task = progress.add_task("Scanning", total=0)

        async def run():
            all_paths = list(base_paths)
            if discover:
                client = AsyncHttpClient(
                    timeout=timeout,
                    verify_tls=not no_verify,
                    follow_redirects=not no_redirects,
                    proxies=proxy,
                    headers=headers or None,
                    cookies=cookies or None,
                )
                robots, sitemap, homepage = await asyncio.gather(
                    fetch_robots_paths(client, url),
                    fetch_sitemap_paths(client, url),
                    fetch_homepage_hints(client, url),
                )
                await client.aclose()
                all_paths.extend(robots)
                all_paths.extend(sitemap)
                all_paths.extend(homepage)
            seen = set()
            paths = [p for p in all_paths if not (p in seen or seen.add(p))]

            if cache:
                seen_paths = cache.load_seen()
                paths = [p for p in paths if p not in seen_paths]

            progress.update(task, total=len(paths))

            results = await scan_admin_paths(
                url,
                paths,
                concurrency=concurrency,
                per_host_concurrency=per_host,
                rate_limit=rate_limit,
                rate_burst=rate_burst,
                timeout=timeout,
                verify_tls=not no_verify,
                follow_redirects=not no_redirects,
                proxies=proxy,
                headers=headers or None,
                cookies=cookies or None,
                rotate_user_agents=rotate_ua,
            )
            for r in results:
                progress.update(task, advance=1)
                if cache:
                    cache.append_result(r.__dict__)

            hits = [r for r in results if r.ok]
            if hits:
                console.print(f"[bold green]{len(hits)} admin page(s) found[/bold green]")
                for r in hits:
                    console.print(
                        f"[green]{r.status}[/green] {r.url} "
                        f"({r.elapsed_ms} ms, {r.content_length} bytes)"
                        f"{' [redirect]' if r.redirected else ''}"
                    )
            else:
                console.print("[yellow]No admin pages found[/yellow]")
            if json_out:
                json_out.write_text(
                    json.dumps([r.__dict__ for r in results], indent=2),
                    encoding="utf-8",
                )
            if csv_out:
                with csv_out.open("w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(
                        f,
                        fieldnames=[
                            "path",
                            "url",
                            "status",
                            "ok",
                            "redirected",
                            "final_url",
                            "elapsed_ms",
                            "content_length",
                        ],
                    )
                    writer.writeheader()
                    for r in results:
                        writer.writerow(r.__dict__)

        asyncio.run(run())


if __name__ == "__main__":
    app()
