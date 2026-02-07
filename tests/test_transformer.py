"""Unit tests for transformer module."""

import pandas as pd
import pytest

from flexetl.transformer import DataTransformer


class TestDataTransformer:
    """Test DataTransformer class."""

    @pytest.fixture
    def sample_data(self):
        """Create sample DataFrame for testing."""
        return pd.DataFrame({
            'date': ['2026-02-01', '2026-02-01', '2026-02-02'],
            'product_id': ['P001', 'P002', 'P001'],
            'quantity': [2, 5, None],
            'unit_price': [100.0, 25.0, 100.0]
        })

    def test_filter_nulls_all_columns(self, sample_data):
        """Test filtering null values from all columns."""
        transformer = DataTransformer(sample_data)
        result = transformer.filter_nulls().get_result()

        assert len(result) == 2
        assert result['quantity'].notna().all()

    def test_filter_nulls_specific_columns(self, sample_data):
        """Test filtering nulls from specific columns."""
        transformer = DataTransformer(sample_data)
        result = transformer.filter_nulls(['quantity']).get_result()

        assert len(result) == 2

    def test_filter_by_value_greater_than(self):
        """Test filtering by greater than operator."""
        df = pd.DataFrame({
            'value': [1, 5, 10, 15, 20]
        })

        transformer = DataTransformer(df)
        result = transformer.filter_by_value(
            'value', '>', 10
        ).get_result()

        assert len(result) == 2
        assert result['value'].tolist() == [15, 20]

    def test_filter_by_value_invalid_column(self):
        """Test error when filtering non-existent column."""
        df = pd.DataFrame({'value': [1, 2, 3]})
        transformer = DataTransformer(df)

        with pytest.raises(ValueError, match="Column not found"):
            transformer.filter_by_value('invalid', '>', 0)

    def test_filter_by_value_invalid_operator(self):
        """Test error with invalid operator."""
        df = pd.DataFrame({'value': [1, 2, 3]})
        transformer = DataTransformer(df)

        with pytest.raises(ValueError, match="Invalid operator"):
            transformer.filter_by_value('value', 'invalid', 0)

    def test_calculate_revenue(self):
        """Test revenue calculation."""
        df = pd.DataFrame({
            'quantity': [2, 5, 3],
            'unit_price': [100.0, 25.0, 75.0]
        })

        transformer = DataTransformer(df)
        result = transformer.calculate_revenue(
            'quantity', 'unit_price', 'revenue'
        ).get_result()

        assert 'revenue' in result.columns
        assert result['revenue'].tolist() == [200.0, 125.0, 225.0]

    def test_aggregate_sum(self):
        """Test aggregation with sum."""
        df = pd.DataFrame({
            'date': ['2026-02-01', '2026-02-01', '2026-02-02'],
            'product': ['A', 'B', 'A'],
            'quantity': [10, 20, 30]
        })

        transformer = DataTransformer(df)
        result = transformer.aggregate(
            group_by=['product'],
            aggregations={'total': 'sum(quantity)'}
        ).get_result()

        assert len(result) == 2
        assert 'total' in result.columns
        a_total = result[result['product'] == 'A']['total'].iloc[0]
        assert a_total == 40

    def test_aggregate_invalid_column(self):
        """Test error with invalid grouping column."""
        df = pd.DataFrame({'value': [1, 2, 3]})
        transformer = DataTransformer(df)

        with pytest.raises(ValueError, match="Grouping column not found"):
            transformer.aggregate(
                group_by=['invalid'],
                aggregations={'total': 'sum(value)'}
            )

    def test_method_chaining(self, sample_data):
        """Test chaining multiple transformations."""
        result = (
            DataTransformer(sample_data)
            .filter_nulls(['quantity'])
            .filter_by_value('quantity', '>', 1)
            .get_result()
        )

        assert len(result) == 2
        assert all(result['quantity'] > 1)
