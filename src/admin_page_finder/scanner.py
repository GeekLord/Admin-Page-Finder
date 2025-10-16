import asyncio
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin, urlparse

import httpx

from .http import AsyncHttpClient
from .rate_limit import AsyncRateLimiter


@dataclass
class ScanResult:
    path: str
    url: str
    status: int
    ok: bool
    redirected: bool
    final_url: str
    elapsed_ms: int
    content_length: int


def _normalize_base_url(base_url: str) -> str:
    if not base_url.startswith(("http://", "https://")):
        return f"http://{base_url.rstrip('/')}"
    return base_url.rstrip("/")


async def _probe_path(
    client: AsyncHttpClient,
    base_url: str,
    path: str,
) -> ScanResult:
    path_clean = path.strip()
    if not path_clean:
        return ScanResult(
            path=path,
            url="",
            status=0,
            ok=False,
            redirected=False,
            final_url="",
            elapsed_ms=0,
            content_length=0,
        )
    if not path_clean.startswith("/"):
        path_clean = "/" + path_clean
    url = urljoin(base_url + "/", path_clean.lstrip("/"))
    try:
        resp: httpx.Response = await client.get(url)
        content_length = int(resp.headers.get("content-length", 0) or 0)
        return ScanResult(
            path=path_clean,
            url=url,
            status=resp.status_code,
            ok=resp.status_code == 200,
            redirected=len(resp.history) > 0,
            final_url=str(resp.url),
            elapsed_ms=int(resp.elapsed.total_seconds() * 1000),
            content_length=content_length,
        )
    except Exception:
        return ScanResult(
            path=path_clean,
            url=url,
            status=0,
            ok=False,
            redirected=False,
            final_url=url,
            elapsed_ms=0,
            content_length=0,
        )


async def scan_admin_paths(
    base_url: str,
    paths: Iterable[str],
    *,
    concurrency: int = 100,
    per_host_concurrency: int = 10,
    rate_limit: Optional[float] = None,
    rate_burst: int = 1,
    timeout: float = 10.0,
    verify_tls: bool = True,
    follow_redirects: bool = True,
    proxy: Optional[str] = None,
    headers: Optional[Mapping[str, str]] = None,
    cookies: Optional[Mapping[str, str]] = None,
    rotate_user_agents: bool = False,
) -> list[ScanResult]:
    base_url_norm = _normalize_base_url(base_url)
    global_sem = asyncio.Semaphore(max(1, concurrency))
    per_host_sems: dict[str, asyncio.Semaphore] = {}

    parsed = urlparse(base_url_norm)
    host_key = parsed.netloc
    per_host_sems[host_key] = asyncio.Semaphore(max(1, per_host_concurrency))

    results: list[ScanResult] = []

    limiter = AsyncRateLimiter(rate_limit, rate_burst) if rate_limit else None

    client = AsyncHttpClient(
        timeout=timeout,
        verify_tls=verify_tls,
        follow_redirects=follow_redirects,
        proxy=proxy,
        headers=headers,
        cookies=cookies,
        rate_limiter=limiter,
        rotate_user_agents=rotate_user_agents,
    )

    async def worker(p: str) -> None:
        async with global_sem, per_host_sems[host_key]:
            res = await _probe_path(client, base_url_norm, p)
            results.append(res)

    try:
        await asyncio.gather(*(worker(p) for p in paths))
    finally:
        await client.aclose()

    path_index = {path: i for i, path in enumerate(paths)}
    return sorted(
        results,
        key=lambda r: path_index.get(r.path.lstrip("/"), path_index.get(r.path, 0)),
    )
