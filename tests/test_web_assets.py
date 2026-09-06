"""Verify that web application static assets exist and adhere to contracts."""

import json
from pathlib import Path


def test_web_assets_contract() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    docs_dir = repo_root / "docs"

    index_html = docs_dir / "playground" / "index.html"
    playground_css = docs_dir / "assets" / "playground" / "playground.css"
    playground_js = docs_dir / "assets" / "playground" / "playground.js"
    bundle_json = docs_dir / "assets" / "playground" / "playground-bundle.json"

    if not bundle_json.exists():
        from neetlings.bundler import export_bundle

        export_bundle(bundle_json, repo_root)

    assert index_html.exists(), "docs/playground/index.html is missing"
    assert playground_css.exists(), "docs/assets/playground/playground.css is missing"
    assert playground_js.exists(), "docs/assets/playground/playground.js is missing"
    assert bundle_json.exists(), "docs/assets/playground/playground-bundle.json is missing"

    html_content = index_html.read_text(encoding="utf-8")
    assert "problem-pane" in html_content
    assert "editor-pane" in html_content
    assert "diagnostics-pane" in html_content
    assert "category-select" in html_content
    assert "exercise-select" in html_content
    assert "btn-run" in html_content

    css_content = playground_css.read_text(encoding="utf-8")
    assert "--bg-primary" in css_content or "--pg-bg" in css_content
    assert "problem-pane" in css_content
    assert "diagnostics-pane" in css_content

    js_content = playground_js.read_text(encoding="utf-8")
    assert "NeetlingsStorage" in js_content
    assert "playground-worker.js" in js_content
    assert "playground-bundle.json" in js_content

    data = json.loads(bundle_json.read_text(encoding="utf-8"))
    assert "exercises" in data
    assert len(data["exercises"]) >= 30

    # Ensure Category 2 verification checks that all 5 Two Pointers exercises are present in the bundle.
    tp_chapter = next(ch for ch in data["chapters"] if ch["id"] == "two_pointers")
    assert len(tp_chapter["exerciseIds"]) == 5
    assert tp_chapter["exerciseIds"] == [
        "01_valid_palindrome",
        "02_two_sum_ii_input_array_is_sorted",
        "03_3sum",
        "04_container_with_most_water",
        "05_trapping_rain_water",
    ]

