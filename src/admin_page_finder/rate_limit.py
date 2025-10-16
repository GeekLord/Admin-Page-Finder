import asyncio
import time


class AsyncRateLimiter:
    def __init__(self, rate_per_sec: float, burst: int = 1) -> None:
        if rate_per_sec <= 0:
            raise ValueError("rate_per_sec must be > 0")
        self.rate = float(rate_per_sec)
        self.capacity = max(1, int(burst))
        self._tokens = float(self.capacity)
        self._last = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last
            self._last = now
            self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
            if self._tokens < 1.0:
                need = 1.0 - self._tokens
                await asyncio.sleep(need / self.rate)
                self._tokens = 0.0
            else:
                self._tokens -= 1.0
