"""
Data transformation module for FlexETL.

Handles transformation of extracted data including filtering,
aggregation, and cleaning operations.
"""

import logging
from typing import List, Optional

import pandas as pd


logger = logging.getLogger(__name__)


class DataTransformer:
    """Transform data using Pandas operations."""

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Initialize transformer with a DataFrame.

        Args:
            dataframe: Input DataFrame to transform.
        """
        self.df = dataframe.copy()

    def filter_nulls(
        self,
        columns: Optional[List[str]] = None
    ) -> 'DataTransformer':
        """
        Remove rows with null values in specified columns.

        Args:
            columns: List of column names to check. If None, checks all.

        Returns:
            Self for method chaining.
        """
        initial_count = len(self.df)

        if columns:
            self.df = self.df.dropna(subset=columns)
        else:
            self.df = self.df.dropna()

        removed_count = initial_count - len(self.df)
        if removed_count > 0:
            logger.info(f"Filtered {removed_count} rows with null values")

        return self

    def filter_by_value(
        self,
        column: str,
        operator: str,
        value: float
    ) -> 'DataTransformer':
        """
        Filter rows based on column value comparison.

        Args:
            column: Column name to filter on.
            operator: Comparison operator ('>', '<', '>=', '<=', '==', '!=').
            value: Value to compare against.

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If operator is invalid or column doesn't exist.
        """
        if column not in self.df.columns:
            raise ValueError(f"Column not found: {column}")

        initial_count = len(self.df)

        if operator == '>':
            self.df = self.df[self.df[column] > value]
        elif operator == '<':
            self.df = self.df[self.df[column] < value]
        elif operator == '>=':
            self.df = self.df[self.df[column] >= value]
        elif operator == '<=':
            self.df = self.df[self.df[column] <= value]
        elif operator == '==':
            self.df = self.df[self.df[column] == value]
        elif operator == '!=':
            self.df = self.df[self.df[column] != value]
        else:
            raise ValueError(f"Invalid operator: {operator}")

        removed_count = initial_count - len(self.df)
        logger.info(
            f"Filtered {removed_count} rows where {column} "
            f"{operator} {value}"
        )

        return self

    def aggregate(
        self,
        group_by: List[str],
        aggregations: dict
    ) -> 'DataTransformer':
        """
        Aggregate data by grouping columns.

        Args:
            group_by: List of columns to group by.
            aggregations: Dict mapping output column names to aggregation
                         expressions (e.g., {'total': 'sum(quantity)'}).

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If grouping columns don't exist.
        """
        for col in group_by:
            if col not in self.df.columns:
                raise ValueError(f"Grouping column not found: {col}")

        logger.info(f"Aggregating data by {group_by}")

        agg_dict = {}
        for output_col, expr in aggregations.items():
            if expr.startswith('sum(') and expr.endswith(')'):
                col = expr[4:-1]
                agg_dict[col] = 'sum'
            elif expr.startswith('count(') and expr.endswith(')'):
                col = expr[6:-1]
                agg_dict[col] = 'count'
            elif expr.startswith('mean(') and expr.endswith(')'):
                col = expr[5:-1]
                agg_dict[col] = 'mean'

        grouped = self.df.groupby(group_by).agg(agg_dict).reset_index()

        grouped.columns = group_by + list(aggregations.keys())

        self.df = grouped

        logger.info(f"Aggregated to {len(self.df)} rows")
        return self

    def calculate_revenue(
        self,
        quantity_col: str,
        price_col: str,
        output_col: str = 'total_revenue'
    ) -> 'DataTransformer':
        """
        Calculate revenue as quantity * unit_price.

        Args:
            quantity_col: Column name for quantity.
            price_col: Column name for unit price.
            output_col: Name for the calculated revenue column.

        Returns:
            Self for method chaining.
        """
        if quantity_col not in self.df.columns:
            raise ValueError(f"Column not found: {quantity_col}")
        if price_col not in self.df.columns:
            raise ValueError(f"Column not found: {price_col}")

        self.df[output_col] = self.df[quantity_col] * self.df[price_col]

        logger.info(
            f"Calculated {output_col} from {quantity_col} * {price_col}"
        )
        return self

    def get_result(self) -> pd.DataFrame:
        """
        Get the transformed DataFrame.

        Returns:
            Transformed DataFrame.
        """
        return self.df
