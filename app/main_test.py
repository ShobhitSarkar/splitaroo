"""
Tests for app.main.

Cyclomatic flows:
  - main() prints the greeting (single path).
  - FastAPI app exposes the receipt router (no `if __name__ == "__main__"`
    branch reachable from tests, but we verify the imports + mount wired up).
"""

from fastapi.routing import APIRoute

from app import main as main_module


def test_main_prints_greeting(capsys) -> None:
    main_module.main()
    captured = capsys.readouterr()
    assert "Hello from buddysplit!" in captured.out


def test_fastapi_app_has_receipt_router_mounted() -> None:
    paths = {
        route.path for route in main_module.app.routes if isinstance(route, APIRoute)
    }
    assert "/receipt/uploadReciept" in paths
    assert "/receipt/unstructuredData" in paths
    assert "/receipt/get_split" in paths
    assert "/receipt/stt" in paths
