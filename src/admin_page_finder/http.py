import random
from collections.abc import Iterable, Mapping
from typing import Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

from .rate_limit import AsyncRateLimiter

DEFAULT_HEADERS = {
    "User-Agent": "AdminPageFinder/0.1 (+https://github.com/your-org/Admin-Page-Finder)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

DEFAULT_UAS = [
    DEFAULT_HEADERS["User-Agent"],
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36"
    ),
    (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36"
    ),
    (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
    ),
]


class AsyncHttpClient:
    def __init__(
        self,
        timeout: float = 10.0,
        verify_tls: bool = True,
        proxies: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
        follow_redirects: bool = True,
        cookies: Optional[Mapping[str, str]] = None,
        rate_limiter: Optional[AsyncRateLimiter] = None,
        rotate_user_agents: bool = False,
        user_agents: Optional[Iterable[str]] = None,
    ) -> None:
        merged_headers = dict(DEFAULT_HEADERS)
        if headers:
            merged_headers.update(headers)
        self._rotate_uas = rotate_user_agents
        self._user_agents = list(user_agents) if user_agents else DEFAULT_UAS
        self._rate_limiter = rate_limiter
        self._client = httpx.AsyncClient(
            timeout=timeout,
            headers=merged_headers,
            verify=verify_tls,
            http2=True,
            follow_redirects=follow_redirects,
            proxies=proxies,
            cookies=cookies,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def _maybe_wait(self) -> None:
        if self._rate_limiter:
            await self._rate_limiter.acquire()

    def _maybe_rotate_headers(self) -> dict:
        if self._rotate_uas:
            ua = random.choice(self._user_agents)
            headers = dict(self._client.headers)
            headers["User-Agent"] = ua
            return headers
        return dict(self._client.headers)

    @retry(wait=wait_exponential_jitter(initial=0.2, max=10), stop=stop_after_attempt(3))
    async def get(self, url: str) -> httpx.Response:
        await self._maybe_wait()
        headers = self._maybe_rotate_headers()
        return await self._client.get(url, headers=headers)
