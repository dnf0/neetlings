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

    # Verify that the bundle contains at least 30 exercises (9 Arrays + 5 Two Pointers + 16 remaining).
    assert len(bundle["exercises"]) >= 30

    # Verify that Category 1 (Arrays & Hashing) registers all 9 exercise IDs in order.
    cat1 = bundle["chapters"][0]
    assert cat1["id"] == "arrays_and_hashing"
    assert len(cat1["exerciseIds"]) == 9
    assert cat1["exerciseIds"] == [
        "01_contains_duplicate",
        "02_valid_anagram",
        "03_two_sum",
        "04_group_anagrams",
        "05_top_k_frequent_elements",
        "06_product_of_array_except_self",
        "07_valid_sudoku",
        "08_encode_and_decode_strings",
        "09_longest_consecutive_sequence",
    ]

    # Verify that Category 2 (Two Pointers) registers all 5 exercise IDs in order.
    cat2 = bundle["chapters"][1]
    assert cat2["id"] == "two_pointers"
    assert len(cat2["exerciseIds"]) == 5
    assert cat2["exerciseIds"] == [
        "01_valid_palindrome",
        "02_two_sum_ii_input_array_is_sorted",
        "03_3sum",
        "04_container_with_most_water",
        "05_trapping_rain_water",
    ]


def test_manifest_categories_and_chapters() -> None:
    """Verify that manifest.CATEGORIES and manifest.CHAPTERS register problems correctly."""
    from neetlings.manifest import CATEGORIES, CHAPTERS

    # Ensure CHAPTERS is an alias for CATEGORIES.
    assert CATEGORIES is CHAPTERS
    assert len(CATEGORIES) == 18

    # Verify that the first chapter is arrays_and_hashing with 9 registered problems.
    arrays_cat = CATEGORIES[0]
    assert arrays_cat.id == "arrays_and_hashing"
    assert arrays_cat.exercise_ids == [
        "01_contains_duplicate",
        "02_valid_anagram",
        "03_two_sum",
        "04_group_anagrams",
        "05_top_k_frequent_elements",
        "06_product_of_array_except_self",
        "07_valid_sudoku",
        "08_encode_and_decode_strings",
        "09_longest_consecutive_sequence",
    ]

    # Verify that Category 2 is two_pointers with all 5 registered problems.
    two_pointers_cat = CATEGORIES[1]
    assert two_pointers_cat.id == "two_pointers"
    assert two_pointers_cat.exercise_ids == [
        "01_valid_palindrome",
        "02_two_sum_ii_input_array_is_sorted",
        "03_3sum",
        "04_container_with_most_water",
        "05_trapping_rain_water",
    ]


