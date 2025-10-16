import pytest
import respx

from admin_page_finder.discovery import (
    fetch_homepage_hints,
    fetch_robots_paths,
    fetch_sitemap_paths,
)
from admin_page_finder.http import AsyncHttpClient


@pytest.mark.asyncio
async def test_fetch_robots_paths():
    base = "http://example.com"
    with respx.mock(base_url=base) as router:
        router.get("/robots.txt").respond(
            200,
            text="""
            User-agent: *
            Disallow: /admin/
            Disallow: /private
            """,
        )
        client = AsyncHttpClient()
        paths = await fetch_robots_paths(client, base)
        await client.aclose()
    assert "/admin/" in paths


@pytest.mark.asyncio
async def test_fetch_sitemap_paths_and_homepage():
    base = "http://example.com"
    with respx.mock(base_url=base) as router:
        router.get("/sitemap.xml").respond(
            200,
            text="""
            <urlset>
              <url><loc>http://example.com/</loc></url>
              <url><loc>http://example.com/admin/login</loc></url>
            </urlset>
            """,
        )
        router.get("/").respond(
            200,
            text='<a href="/dashboard">Dashboard</a> <a href="/public">Public</a>',
        )
        client = AsyncHttpClient()
        sm = await fetch_sitemap_paths(client, base)
        hp = await fetch_homepage_hints(client, base)
        await client.aclose()
    assert "/admin/login" in sm
    assert "/dashboard" in hp
