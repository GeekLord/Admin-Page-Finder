from __future__ import annotations

import asyncio
import time

from admin_page_finder.scanner import scan_admin_paths


async def main() -> None:
    base = "http://example.com"
    # Synthetic paths
    paths = [f"admin/{i}" for i in range(200)]
    start = time.perf_counter()
    await scan_admin_paths(base, paths, concurrency=50)
    mid = time.perf_counter()
    await scan_admin_paths(base, paths, concurrency=200)
    end = time.perf_counter()
    print(f"50 concurrency: {mid - start:.3f}s, 200 concurrency: {end - mid:.3f}s")


if __name__ == "__main__":
    asyncio.run(main())
