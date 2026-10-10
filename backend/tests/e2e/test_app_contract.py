"""App-level G1 contract: routers, registration, OpenAPI, errors."""
import ast
import importlib
from pathlib import Path

import pytest
from fastapi import APIRouter

FEATURE_MODULES = [
    "auth", "health", "fixtures", "ingestion", "gap", "scenario", "export",
    "ml", "analytics", "behavioural", "recommendations",
]
MAIN_PY = Path(__file__).resolve().parents[2] / "app" / "main.py"


@pytest.mark.parametrize("name", FEATURE_MODULES)
def test_router_module_imports_and_exposes_apirouter(name):
    module = importlib.import_module(f"app.{name}.router")
    assert isinstance(module.router, APIRouter)


def test_main_registers_every_router_exactly_once():
    tree = ast.parse(MAIN_PY.read_text(encoding="utf-8"))
    alias_to_module = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.endswith(".router"):
            for a in node.names:
                if a.name == "router":
                    alias_to_module[a.asname] = node.module.split(".")[1]
    included = [
        n.args[0].id for n in ast.walk(tree)
        if isinstance(n, ast.Call) and getattr(n.func, "attr", None) == "include_router"
    ]
    modules = sorted(alias_to_module[a] for a in included)
    assert modules == sorted(FEATURE_MODULES)
    assert len(included) == len(set(included)) == len(FEATURE_MODULES)


def test_main_imports():
    from app.main import app
    assert app.title


def test_openapi_generates(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    spec = r.json()
    assert spec["openapi"].startswith("3.")
    assert "/health" in spec["paths"]
    assert "/api/v1/fixtures/ladder" in spec["paths"]


def test_swagger_ui_served(client):
    r = client.get("/docs")
    assert r.status_code == 200 and "swagger" in r.text.lower()


def test_unknown_route_uses_error_shape(client):
    r = client.get("/api/v1/does-not-exist")
    assert r.status_code == 404
    assert r.json() == {"code": "NOT_FOUND", "message": "Not Found"}


def test_wrong_method_uses_error_shape(client):
    r = client.post("/health")
    assert r.status_code == 405
    assert r.json()["code"] == "METHOD_NOT_ALLOWED"
