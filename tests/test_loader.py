"""Unit tests for loader module."""

import pandas as pd
import pytest

from flexetl.loader import SQLiteLoader


class TestSQLiteLoader:
    """Test SQLiteLoader class."""

    @pytest.fixture
    def sample_data(self):
        """Create sample DataFrame for testing."""
        return pd.DataFrame({
            'date': ['2026-02-01', '2026-02-02'],
            'product_id': ['P001', 'P002'],
            'total_quantity': [5, 10],
            'total_revenue': [500.0, 250.0]
        })

    def test_load_success(self, tmp_path, sample_data):
        """Test successful data load."""
        db_path = tmp_path / "test.db"

        loader = SQLiteLoader(
            database_path=str(db_path),
            table_name="test_table",
            if_exists="replace"
        )

        rows_loaded = loader.load(sample_data)

        assert rows_loaded == 2
        assert db_path.exists()

    def test_load_empty_dataframe(self, tmp_path):
        """Test error when loading empty DataFrame."""
        db_path = tmp_path / "test.db"
        empty_df = pd.DataFrame()

        loader = SQLiteLoader(
            database_path=str(db_path),
            table_name="test_table"
        )

        with pytest.raises(ValueError, match="empty DataFrame"):
            loader.load(empty_df)

    def test_verify_load(self, tmp_path, sample_data):
        """Test verification of loaded data."""
        db_path = tmp_path / "test.db"

        loader = SQLiteLoader(
            database_path=str(db_path),
            table_name="test_table"
        )

        loader.load(sample_data)
        count = loader.verify_load()

        assert count == 2

    def test_load_replace_mode(self, tmp_path, sample_data):
        """Test replace mode overwrites existing data."""
        db_path = tmp_path / "test.db"

        loader = SQLiteLoader(
            database_path=str(db_path),
            table_name="test_table",
            if_exists="replace"
        )

        loader.load(sample_data)
        first_count = loader.verify_load()

        new_data = pd.DataFrame({
            'date': ['2026-02-03'],
            'product_id': ['P003'],
            'total_quantity': [15],
            'total_revenue': [750.0]
        })

        loader.load(new_data)
        second_count = loader.verify_load()

        assert first_count == 2
        assert second_count == 1

    def test_load_append_mode(self, tmp_path, sample_data):
        """Test append mode adds to existing data."""
        db_path = tmp_path / "test.db"

        loader = SQLiteLoader(
            database_path=str(db_path),
            table_name="test_table",
            if_exists="append"
        )

        loader.load(sample_data)
        first_count = loader.verify_load()

        loader.load(sample_data)
        second_count = loader.verify_load()

        assert first_count == 2
        assert second_count == 4

    def test_database_directory_creation(self, tmp_path, sample_data):
        """Test that parent directories are created."""
        db_path = tmp_path / "subdir" / "nested" / "test.db"

        loader = SQLiteLoader(
            database_path=str(db_path),
            table_name="test_table"
        )

        loader.load(sample_data)

        assert db_path.exists()
        assert db_path.parent.exists()
