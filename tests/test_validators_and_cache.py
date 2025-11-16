import pytest

from flamehaven_filesearch.cache import (
    FileMetadataCache,
    SearchResultCache,
    get_all_cache_stats,
    get_file_cache,
    get_search_cache,
    reset_all_caches,
)
from flamehaven_filesearch.exceptions import (
    FileSizeExceededError,
    InvalidFilenameError,
    InvalidSearchQueryError,
    ValidationError,
)
from flamehaven_filesearch.validators import (
    ConfigValidator,
    FilenameValidator,
    FileSizeValidator,
    MimeTypeValidator,
    SearchQueryValidator,
    validate_search_request,
    validate_upload_file,
)


@pytest.mark.parametrize(
    "filename",
    [
        "../secret.txt",
        "C:\\\\system32\\\\cmd.exe",
        ".hidden",
        "bad:name?.txt",
        "con.txt",
    ],
)
def test_filename_validator_rejects_unsafe_names(filename):
    with pytest.raises(InvalidFilenameError):
        FilenameValidator.validate_filename(filename)


def test_filename_validator_returns_basename():
    assert FilenameValidator.validate_filename(" reports/summary.txt ") == "summary.txt"


def test_sanitize_filename_removes_invalid_sequences():
    sanitized = FilenameValidator.sanitize_filename("../..hidden?.txt")
    assert sanitized == "hidden_.txt"


def test_file_size_validator_checks_limit():
    with pytest.raises(FileSizeExceededError):
        FileSizeValidator.validate_file_size(
            3 * 1024 * 1024, max_size_mb=1, filename="big.txt"
        )

    assert FileSizeValidator.bytes_to_mb(1048576) == 1.0


def test_search_query_validator_strict_mode_blocks_patterns():
    with pytest.raises(InvalidSearchQueryError):
        SearchQueryValidator.validate_query("<script>alert(1)</script>", strict=True)


def test_search_query_sanitize_strips_html():
    cleaned = SearchQueryValidator.sanitize_query("  <b>Hello</b> -- DROP  ")
    assert cleaned == "Hello  DROP"


def test_config_validator_enforces_types_and_ranges():
    assert ConfigValidator.validate_positive_int(5, "limit", min_value=1) == 5
    with pytest.raises(ValidationError):
        ConfigValidator.validate_positive_int("oops", "limit")

    assert ConfigValidator.validate_float_range(0.5, "temperature", 0.0, 1.0) == 0.5
    with pytest.raises(ValidationError):
        ConfigValidator.validate_float_range(2.5, "temperature", 0.0, 1.0)

    assert ConfigValidator.validate_string_not_empty("  data ", "field") == "data"
    with pytest.raises(ValidationError):
        ConfigValidator.validate_string_not_empty("", "field")


def test_mime_type_validator_handles_alias_and_custom_list():
    assert MimeTypeValidator.validate_mime_type("text/x-markdown") is True
    assert MimeTypeValidator.validate_mime_type(
        "application/rare", custom_allowed=["application/rare"]
    )
    assert not MimeTypeValidator.validate_mime_type("application/unknown")


def test_validate_upload_file_returns_clean_name(tmp_path):
    sample = tmp_path / "note.txt"
    sample.write_text("content", encoding="utf-8")
    filename, mime_valid = validate_upload_file(
        filename=sample.name,
        file_size=sample.stat().st_size,
        mime_type="text/plain",
        max_size_mb=10,
    )
    assert filename == "note.txt"
    assert mime_valid is True


def test_validate_search_request_caps_results():
    query, limit = validate_search_request("explain", max_results=500)
    assert query == "explain"
    assert limit == 100


def test_search_result_cache_hit_miss_and_stats():
    cache = SearchResultCache(maxsize=2, ttl=5)
    assert cache.get("hello", "default") is None
    cache.set("hello", "default", {"status": "success"})
    assert cache.get("hello", "default") == {"status": "success"}
    stats = cache.get_stats()
    assert stats["total_requests"] == 2
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    cache.invalidate()
    cache.reset_stats()
    assert cache.get_stats()["total_requests"] == 0


def test_search_result_cache_handles_internal_errors(monkeypatch):
    cache = SearchResultCache(maxsize=1, ttl=1)

    class FailingContainer:
        def get(self, key):
            raise RuntimeError("boom")

        def __setitem__(self, key, value):
            raise RuntimeError("boom")

    cache.cache = FailingContainer()
    assert cache.get("x", "store") is None
    cache.set("x", "store", {"status": "success"})


def test_file_metadata_cache_operations():
    cache = FileMetadataCache(maxsize=1)
    cache.set("a.txt", {"size": 10})
    assert cache.get("a.txt") == {"size": 10}
    cache.invalidate("a.txt")
    assert cache.get("a.txt") is None
    cache.set("b.txt", {"size": 5})
    cache.invalidate()
    assert cache.get_stats()["current_size"] == 0


def test_global_cache_helpers_provide_stats():
    reset_all_caches()
    search_cache = get_search_cache(maxsize=1, ttl=1)
    file_cache = get_file_cache(maxsize=1)
    search_cache.set("query", "default", {"status": "success"})
    file_cache.set("doc", {"size": 1})

    stats = get_all_cache_stats()
    assert "search_cache" in stats
    assert "file_cache" in stats

    reset_all_caches()
    reset_stats = get_all_cache_stats()
    assert reset_stats["search_cache"]["current_size"] == 0
    assert reset_stats["file_cache"]["current_size"] == 0
