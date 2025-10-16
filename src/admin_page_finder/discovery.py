import re
from html import unescape
from urllib.parse import urljoin, urlparse

from .http import AsyncHttpClient

ADMIN_HINT_RE = re.compile(r"(admin|login|wp-admin|wp-login|cpanel|dashboard)", re.I)


async def fetch_robots_paths(client: AsyncHttpClient, base_url: str) -> list[str]:
    robots_url = urljoin(base_url + "/", "robots.txt")
    try:
        resp = await client.get(robots_url)
        if resp.status_code != 200:
            return []
        lines = resp.text.splitlines()
        paths: list[str] = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.lower().startswith("disallow:"):
                _, value = line.split(":", 1)
                p = value.strip()
                if p and ADMIN_HINT_RE.search(p):
                    paths.append(p)
        return paths
    except Exception:
        return []


async def fetch_sitemap_paths(client: AsyncHttpClient, base_url: str) -> list[str]:
    candidates = [
        urljoin(base_url + "/", "sitemap.xml"),
        urljoin(base_url + "/", "sitemap_index.xml"),
    ]
    discovered: list[str] = []
    for url in candidates:
        try:
            resp = await client.get(url)
            if resp.status_code != 200:
                continue
            text = resp.text
            for m in re.finditer(r"<loc>(.*?)</loc>", text, re.I | re.S):
                loc = unescape(m.group(1)).strip()
                if not loc:
                    continue
                parsed = urlparse(loc)
                if ADMIN_HINT_RE.search(parsed.path):
                    discovered.append(parsed.path)
        except Exception:
            continue
    return discovered


async def fetch_homepage_hints(client: AsyncHttpClient, base_url: str) -> list[str]:
    try:
        resp = await client.get(base_url)
        if resp.status_code != 200:
            return []
        html = resp.text
        paths: list[str] = []
        for m in re.finditer(r"<a\s+[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", html, re.I | re.S):
            href = unescape(m.group(1)).strip()
            text = unescape(m.group(2) or "").strip()
            if ADMIN_HINT_RE.search(href) or ADMIN_HINT_RE.search(text):
                parsed = urlparse(href)
                if parsed.scheme or parsed.netloc:
                    base_host = urlparse(base_url).netloc
                    if parsed.netloc and parsed.netloc != base_host:
                        continue
                    paths.append(parsed.path)
                else:
                    paths.append(href)
        return list({p for p in paths if p})
    except Exception:
        return []
