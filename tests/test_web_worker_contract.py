"""Verify Web Worker file syntax and message contracts."""

from pathlib import Path


def test_worker_file_contains_pyodide_loading() -> None:
    worker_path = Path("docs/assets/playground/playground-worker.js")
    assert worker_path.exists(), "playground-worker.js does not exist"
    content = worker_path.read_text(encoding="utf-8")
    assert "importScripts" in content
    assert "pyodide" in content
    assert "evaluate_code" in content
    assert "INIT" in content
    assert "RUN" in content
