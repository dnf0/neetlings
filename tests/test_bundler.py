"""Tests for bundle generator."""

from pathlib import Path

from neetlings.bundler import generate_bundle


def test_generate_bundle_structure() -> None:
    """Verify that the generated bundle has the correct structure and categories."""
    # Resolve the repository root relative to this test file.
    repo_root = Path(__file__).resolve().parent.parent

    # Generate the bundle using the bundler implementation.
    bundle = generate_bundle(repo_root=repo_root)

    # Assert top-level keys in the generated bundle.
    assert "version" in bundle
    assert "chapters" in bundle
    assert "exercises" in bundle
    assert "runtime_modules" in bundle

    # Assert essential runtime module files are correctly bundled.
    assert "models.py" in bundle["runtime_modules"]
    assert "visualizers.py" in bundle["runtime_modules"]
    assert "complexity.py" in bundle["runtime_modules"]
    assert "test_runner.py" in bundle["runtime_modules"]

    # Verify that all 18 NeetCode categories are present.
    assert len(bundle["chapters"]) == 18
