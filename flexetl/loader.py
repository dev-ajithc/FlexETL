"""
Data loading module for FlexETL.

Handles loading of transformed data into target destinations.
Phase 1 supports SQLite database.
"""

import logging
import sqlite3
from pathlib import Path

import pandas as pd


logger = logging.getLogger(__name__)


class SQLiteLoader:
    """Load data into SQLite database."""

    def __init__(
        self,
        database_path: str,
        table_name: str,
        if_exists: str = 'replace'
    ) -> None:
        """
        Initialize SQLite loader.

        Args:
            database_path: Path to SQLite database file.
            table_name: Name of the table to load data into.
            if_exists: How to behave if table exists
                      ('fail', 'replace', 'append').
        """
        self.database_path = Path(database_path)
        self.table_name = table_name
        self.if_exists = if_exists

        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self, dataframe: pd.DataFrame) -> int:
        """
        Load DataFrame into SQLite database.

        Args:
            dataframe: DataFrame to load.

        Returns:
            Number of rows loaded.

        Raises:
            ValueError: If DataFrame is empty.
            sqlite3.Error: If database operation fails.
        """
        if dataframe.empty:
            raise ValueError("Cannot load empty DataFrame")

        logger.info(
            f"Loading {len(dataframe)} records to "
            f"{self.table_name} in {self.database_path}"
        )

        try:
            conn = sqlite3.connect(str(self.database_path))

            dataframe.to_sql(
                self.table_name,
                conn,
                if_exists=self.if_exists,
                index=False
            )

            conn.commit()
            conn.close()

            logger.info(
                f"Successfully loaded {len(dataframe)} records "
                f"to {self.table_name}"
            )

            return len(dataframe)

        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def verify_load(self) -> int:
        """
        Verify data was loaded by counting records.

        Returns:
            Number of records in the table.

        Raises:
            sqlite3.Error: If database operation fails.
        """
        try:
            conn = sqlite3.connect(str(self.database_path))
            cursor = conn.cursor()

            query = f'SELECT COUNT(*) FROM "{self.table_name}"'
            cursor.execute(query)
            count = cursor.fetchone()[0]

            conn.close()

            logger.info(
                f"Verified {count} records in {self.table_name}"
            )

            return count

        except sqlite3.Error as e:
            logger.error(f"Verification error: {e}")
            raise
