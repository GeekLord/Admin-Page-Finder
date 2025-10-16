from typer.testing import CliRunner

from admin_page_finder.cli import app


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "async scanner" in result.stdout.lower()
