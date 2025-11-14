import json
import logging

import pytest

from flamehaven_filesearch.logging_config import (
    CustomJsonFormatter,
    RequestLoggingContext,
    get_logger_with_request_id,
    setup_development_logging,
    setup_json_logging,
)
from flamehaven_filesearch.exceptions import (
    EmptySearchQueryError,
    ExternalAPIError,
    FileProcessingError,
    FileSizeExceededError,
    InvalidFilenameError,
    InvalidSearchQueryError,
    InternalServerError,
    ResourceConflictError,
    ResourceNotFoundError,
    ServiceUnavailableError,
    UnsupportedFileTypeError,
    exception_to_response,
)


@pytest.fixture
def reset_logging():
    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers[:]
    original_level = root_logger.level
    yield
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    for handler in original_handlers:
        root_logger.addHandler(handler)
    root_logger.setLevel(original_level)


def test_custom_json_formatter_injects_metadata(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "testing")
    formatter = CustomJsonFormatter("%(message)s")
    record = logging.LogRecord(
        name="flamehaven.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="structured-message",
        args=(),
        exc_info=None,
    )
    record.request_id = "req-123"

    payload = json.loads(formatter.format(record))
    assert payload["service"] == "flamehaven-filesearch"
    assert payload["environment"] == "testing"
    assert payload["request_id"] == "req-123"
    assert payload["level"] == "INFO"
    assert "timestamp" in payload


def test_setup_json_logging_accepts_level_kwarg(reset_logging):
    setup_json_logging(level=logging.DEBUG)
    root_logger = logging.getLogger()
    assert root_logger.level == logging.DEBUG
    assert any(
        isinstance(handler.formatter, CustomJsonFormatter)
        for handler in root_logger.handlers
    )


def test_setup_development_logging_produces_plain_output(reset_logging, capsys):
    setup_development_logging(level=logging.WARNING)
    base_logger = logging.getLogger("flamehaven.dev")
    logger = logging.LoggerAdapter(base_logger, {"request_id": "dev-test"})

    logger.warning("human-readable")

    assert "human-readable" in capsys.readouterr().out


def test_request_logging_context_injects_request_id(caplog):
    logger = logging.getLogger()
    with caplog.at_level(logging.INFO):
        with RequestLoggingContext("request-42"):
            logger.info("processing request")

    assert any(
        getattr(record, "request_id", None) == "request-42" for record in caplog.records
    )


def test_get_logger_with_request_id_returns_adapter():
    adapter = get_logger_with_request_id("flamehaven.adapter", "adapter-request")
    assert isinstance(adapter, logging.LoggerAdapter)
    assert adapter.extra["request_id"] == "adapter-request"


@pytest.mark.parametrize(
    "exc,code,status",
    [
        (
            FileSizeExceededError(2 * 1024 * 1024, 1, "doc.pdf"),
            "FILE_SIZE_EXCEEDED",
            400,
        ),
        (
            InvalidFilenameError("..\\secret.txt", "Path traversal detected"),
            "INVALID_FILENAME",
            400,
        ),
        (
            UnsupportedFileTypeError("application/x-bin", ["text/plain"]),
            "UNSUPPORTED_FILE_TYPE",
            400,
        ),
        (
            FileProcessingError("failed to parse", "doc.pdf"),
            "FILE_PROCESSING_ERROR",
            400,
        ),
        (EmptySearchQueryError(), "EMPTY_SEARCH_QUERY", 400),
        (
            InvalidSearchQueryError("DROP TABLE", "Query contains suspicious patterns"),
            "INVALID_SEARCH_QUERY",
            400,
        ),
        (
            ServiceUnavailableError("searcher", "maintenance"),
            "SERVICE_UNAVAILABLE",
            503,
        ),
        (ExternalAPIError("gemini", "rate limited", 429), "EXTERNAL_API_ERROR", 502),
        (ResourceNotFoundError("store", "missing"), "RESOURCE_NOT_FOUND", 404),
        (ResourceConflictError("store", "default", "exists"), "RESOURCE_CONFLICT", 409),
        (InternalServerError("boom"), "INTERNAL_SERVER_ERROR", 500),
    ],
)
def test_file_search_exceptions_to_dict(exc, code, status):
    payload = exc.to_dict()
    assert payload["error"] == code
    assert payload["status_code"] == status
    assert payload["message"]


@pytest.mark.parametrize(
    "exc,expected",
    [
        (ValueError("bad input"), {"error": "VALIDATION_ERROR", "status_code": 422}),
        (FileNotFoundError("missing"), {"error": "FILE_NOT_FOUND", "status_code": 404}),
        (PermissionError("deny"), {"error": "PERMISSION_DENIED", "status_code": 403}),
        (TimeoutError("slow"), {"error": "TIMEOUT", "status_code": 504}),
        (RuntimeError("boom"), {"error": "INTERNAL_ERROR", "status_code": 500}),
    ],
)
def test_exception_to_response_for_standard_errors(exc, expected):
    payload = exception_to_response(exc)
    assert payload["error"] == expected["error"]
    assert payload["status_code"] == expected["status_code"]
