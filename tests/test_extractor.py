"""Unit tests for extractor module."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest

from flexetl.extractor import CSVExtractor


class TestCSVExtractor:
    """Test CSVExtractor class."""

    def test_extract_valid_csv(self, tmp_path):
        """Test extracting data from valid CSV file."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "id,name,value\n1,test1,100\n2,test2,200\n"
        )

        extractor = CSVExtractor(str(csv_file))
        df = extractor.extract()

        assert len(df) == 2
        assert list(df.columns) == ['id', 'name', 'value']
        assert df['id'].tolist() == [1, 2]

    def test_extract_file_not_found(self):
        """Test error when CSV file doesn't exist."""
        extractor = CSVExtractor("nonexistent.csv")

        with pytest.raises(FileNotFoundError):
            extractor.extract()

    def test_extract_empty_csv(self, tmp_path):
        """Test error when CSV file is empty."""
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("")

        extractor = CSVExtractor(str(csv_file))

        with pytest.raises(ValueError, match="empty or invalid"):
            extractor.extract()

    def test_extract_only_headers(self, tmp_path):
        """Test error when CSV has only headers."""
        csv_file = tmp_path / "headers_only.csv"
        csv_file.write_text("id,name,value\n")

        extractor = CSVExtractor(str(csv_file))

        with pytest.raises(ValueError, match="empty"):
            extractor.extract()
