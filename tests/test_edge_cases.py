"""
Edge Case Test Suite for FLAMEHAVEN FileSearch

Tests boundary conditions, unusual inputs, and error scenarios.
"""

import pytest
from fastapi.testclient import TestClient

from flamehaven_filesearch.api import app
from flamehaven_filesearch.config import Config


class TestFileUploadEdgeCases:
    """Test edge cases in file upload functionality"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_zero_byte_file(self, client):
        """Test uploading zero-byte file"""
        response = client.post(
            "/api/upload/single",
            files={"file": ("empty.txt", b"", "text/plain")},
        )

        # Should handle gracefully
        assert response.status_code in [200, 400]

    def test_very_long_filename(self, client):
        """Test uploading file with extremely long filename"""
        # 255 characters (typical filesystem limit)
        long_filename = "a" * 250 + ".txt"

        response = client.post(
            "/api/upload/single",
            files={"file": (long_filename, b"content", "text/plain")},
        )

        # Should handle or reject appropriately
        assert response.status_code in [200, 400]

    def test_unicode_filename(self, client):
        """Test uploading file with Unicode characters in filename"""
        unicode_filenames = [
            "文档.txt",  # Chinese
            "документ.txt",  # Russian
            "مستند.txt",  # Arabic
            "📄_document.txt",  # Emoji
            "café_résumé.txt",  # Accents
        ]

        for filename in unicode_filenames:
            response = client.post(
                "/api/upload/single",
                files={"file": (filename, b"content", "text/plain")},
            )

            # Should handle Unicode gracefully
            assert response.status_code in [200, 400]

    def test_special_characters_filename(self, client):
        """Test filenames with special characters"""
        special_filenames = [
            "file name with spaces.txt",
            "file-with-dashes.txt",
            "file_with_underscores.txt",
            "file.multiple.dots.txt",
            "file(with)parens.txt",
            "file[with]brackets.txt",
            "file{with}braces.txt",
        ]

        for filename in special_filenames:
            response = client.post(
                "/api/upload/single",
                files={"file": (filename, b"content", "text/plain")},
            )

            # Legitimate special chars should be accepted
            assert response.status_code in [200]

    def test_no_file_extension(self, client):
        """Test uploading file without extension"""
        response = client.post(
            "/api/upload/single",
            files={"file": ("README", b"# README content", "text/plain")},
        )

        # Should accept files without extensions
        assert response.status_code == 200

    def test_multiple_extensions(self, client):
        """Test file with multiple extensions"""
        response = client.post(
            "/api/upload/single",
            files={"file": ("archive.tar.gz", b"content", "application/gzip")},
        )

        assert response.status_code == 200

    def test_duplicate_filenames_multiple_upload(self, client):
        """Test uploading multiple files with same name"""
        duplicate_files = [
            ("files", ("document.txt", b"First version", "text/plain")),
            ("files", ("document.txt", b"Second version", "text/plain")),
            ("files", ("document.txt", b"Third version", "text/plain")),
        ]

        response = client.post("/api/upload/multiple", files=duplicate_files)

        # Should handle duplicates (rename or reject)
        assert response.status_code in [200, 400]

    def test_unsupported_mime_type(self, client):
        """Test uploading file with unusual MIME type"""
        unusual_mimes = [
            ("file.xyz", b"content", "application/x-unknown"),
            ("file.bin", b"binary", "application/octet-stream"),
            ("file.custom", b"data", "application/x-custom"),
        ]

        for filename, content, mime in unusual_mimes:
            response = client.post(
                "/api/upload/single",
                files={"file": (filename, content, mime)},
            )

            # Should accept or have clear rejection reason
            assert response.status_code in [200, 400, 415]


class TestSearchEdgeCases:
    """Test edge cases in search functionality"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_empty_search_query(self, client):
        """Test search with empty query"""
        response = client.post(
            "/api/search",
            json={"query": ""},
        )

        # Should reject or handle empty query
        assert response.status_code in [200, 400, 422]

    def test_very_long_search_query(self, client):
        """Test search with extremely long query"""
        long_query = "word " * 1000  # Very long query

        response = client.post(
            "/api/search",
            json={"query": long_query},
        )

        # Should handle or reject gracefully
        assert response.status_code in [200, 400, 413]

    def test_special_regex_characters_search(self, client):
        """Test search with regex special characters"""
        regex_chars = [
            "C++ programming",
            "cost is $100",
            "use regex: .*",
            "match [abc]",
            "group (test)",
            "question?",
            "star*",
            "plus+",
            "pipe|test",
            "backslash\\test",
        ]

        for query in regex_chars:
            response = client.post(
                "/api/search",
                json={"query": query},
            )

            # Should escape or handle regex chars
            assert response.status_code in [200, 404]

    def test_unicode_search_query(self, client):
        """Test search with Unicode characters"""
        unicode_queries = [
            "机器学习",  # Machine learning in Chinese
            "искусственный интеллект",  # AI in Russian
            "café résumé",  # Accented characters
            "emoji test 🔍",  # With emoji
        ]

        for query in unicode_queries:
            response = client.post(
                "/api/search",
                json={"query": query},
            )

            # Should handle Unicode in search
            assert response.status_code in [200, 404]

    def test_search_with_only_stopwords(self, client):
        """Test search containing only stopwords"""
        stopword_queries = [
            "the a an",
            "is was were",
            "to from at",
        ]

        for query in stopword_queries:
            response = client.post(
                "/api/search",
                json={"query": query},
            )

            # Should handle stopword-only queries
            assert response.status_code in [200, 400, 404]

    def test_search_before_indexing(self, client):
        """Test search when no documents are indexed"""
        response = client.post(
            "/api/search",
            json={"query": "test query"},
        )

        # Should return empty results or appropriate message
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data.get("results", []), list)


class TestConfigurationEdgeCases:
    """Test edge cases in configuration handling"""

    def test_config_with_empty_string_api_key(self):
        """Test config with empty string API key"""
        config = Config(api_key="")

        # Empty string should be treated as no API key
        with pytest.raises(ValueError):
            config.validate(require_api_key=True)

    def test_config_with_whitespace_api_key(self):
        """Test config with whitespace-only API key"""
        config = Config(api_key="   ")

        # Whitespace should not be valid API key
        with pytest.raises(ValueError):
            config.validate(require_api_key=True)

    def test_config_with_very_long_api_key(self):
        """Test config with unusually long API key"""
        long_key = "x" * 10000

        config = Config(api_key=long_key)

        # Should accept (some keys can be long)
        assert config.validate(require_api_key=True)

    def test_config_max_file_size_edge_cases(self):
        """Test file size configuration edge cases"""
        # Zero file size
        config_zero = Config(max_file_size_mb=0)
        assert config_zero.max_file_size_mb == 0

        # Negative file size
        config_neg = Config(max_file_size_mb=-1)
        assert config_neg.max_file_size_mb == -1  # Should this be allowed?

        # Very large file size
        config_large = Config(max_file_size_mb=10000)
        assert config_large.max_file_size_mb == 10000

    def test_config_invalid_temperature(self):
        """Test config with invalid temperature values"""
        # Temperature should be 0-1 for most LLMs
        invalid_temps = [-1.0, 2.0, 100.0]

        for temp in invalid_temps:
            config = Config(temperature=temp)
            # Should accept or validate range
            assert config.temperature == temp


class TestConcurrencyEdgeCases:
    """Test concurrent access and race conditions"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_concurrent_uploads(self, client):
        """Test multiple simultaneous uploads"""
        import concurrent.futures

        def upload_file(index):
            return client.post(
                "/api/upload/single",
                files={
                    "file": (
                        f"file{index}.txt",
                        f"content{index}".encode(),
                        "text/plain",
                    )
                },
            )

        # Upload 10 files concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(upload_file, i) for i in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All should succeed or fail gracefully
        for result in results:
            assert result.status_code in [200, 429, 503]

    def test_concurrent_searches(self, client):
        """Test multiple simultaneous searches"""
        import concurrent.futures

        def search_query(index):
            return client.post(
                "/api/search",
                json={"query": f"test query {index}"},
            )

        # Run 20 searches concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(search_query, i) for i in range(20)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All should complete
        for result in results:
            assert result.status_code in [200, 404, 429, 503]


class TestMemoryEdgeCases:
    """Test memory-related edge cases"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    @pytest.mark.slow
    def test_many_small_files_upload(self, client):
        """Test uploading many small files"""
        # Upload 100 small files
        files = [
            ("files", (f"file{i}.txt", f"content{i}".encode(), "text/plain"))
            for i in range(100)
        ]

        response = client.post("/api/upload/multiple", files=files)

        # Should handle many files
        assert response.status_code in [200, 400, 413]

    @pytest.mark.slow
    def test_repeated_search_memory_leak(self, client):
        """Test for memory leaks in repeated searches"""
        # Run same search 1000 times
        for i in range(1000):
            response = client.post(
                "/api/search",
                json={"query": "test query"},
            )
            assert response.status_code in [200, 404]

        # If this completes without hanging, no obvious memory leak


class TestErrorRecoveryEdgeCases:
    """Test error recovery and resilience"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_malformed_multipart_request(self, client):
        """Test handling of malformed multipart request"""
        # Send invalid multipart data
        response = client.post(
            "/api/upload/single",
            data=b"not a valid multipart request",
            headers={"Content-Type": "multipart/form-data; boundary=invalid"},
        )

        # Should return appropriate error
        assert response.status_code in [400, 422]

    def test_missing_required_field(self, client):
        """Test request with missing required field"""
        response = client.post(
            "/api/search",
            json={},  # Missing 'query' field
        )

        assert response.status_code in [400, 422]

    def test_wrong_content_type(self, client):
        """Test request with wrong Content-Type"""
        response = client.post(
            "/api/search",
            data="query=test",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        # Should reject or handle gracefully
        assert response.status_code in [400, 415, 422]

    def test_extra_unexpected_fields(self, client):
        """Test request with extra unexpected fields"""
        response = client.post(
            "/api/search",
            json={
                "query": "test",
                "unexpected_field": "value",
                "another_field": 123,
            },
        )

        # Should ignore extra fields and process
        assert response.status_code in [200, 404, 400]


class TestBoundaryValues:
    """Test boundary values for various parameters"""

    def test_max_sources_boundary(self):
        """Test MAX_SOURCES boundary values"""
        config_zero = Config(max_sources=0)
        assert config_zero.max_sources == 0

        config_negative = Config(max_sources=-1)
        assert config_negative.max_sources == -1

        config_large = Config(max_sources=10000)
        assert config_large.max_sources == 10000

    def test_max_output_tokens_boundary(self):
        """Test MAX_OUTPUT_TOKENS boundary values"""
        config_min = Config(max_output_tokens=1)
        assert config_min.max_output_tokens == 1

        config_zero = Config(max_output_tokens=0)
        assert config_zero.max_output_tokens == 0

        config_max = Config(max_output_tokens=100000)
        assert config_max.max_output_tokens == 100000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
