import pytest
import respx

from admin_page_finder.scanner import scan_admin_paths


@pytest.mark.asyncio
async def test_scan_admin_paths_basic():
    base = "http://example.com"
    with respx.mock(base_url=base) as router:
        router.get("/admin/").respond(200, text="ok")
        router.get("/login").respond(302, headers={"Location": "/"})
        router.get("/missing").respond(404)
        res = await scan_admin_paths(base, ["admin/", "login", "missing"], concurrency=5)
    assert any(r.ok and r.path == "/admin/" for r in res)
    assert any((r.status == 302) for r in res)
    assert any((r.status == 404) for r in res)
