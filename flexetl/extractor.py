"""
Data extraction module for FlexETL.

Handles extraction of data from various sources. Phase 1 supports CSV files.
"""

import logging
from pathlib import Path
from typing import Optional

import pandas as pd


logger = logging.getLogger(__name__)


class CSVExtractor:
    """Extract data from CSV files."""

    def __init__(self, file_path: str) -> None:
        """
        Initialize CSV extractor.

        Args:
            file_path: Path to the CSV file to extract.
        """
        self.file_path = Path(file_path)

    def extract(self) -> pd.DataFrame:
        """
        Extract data from CSV file.

        Returns:
            DataFrame containing the extracted data.

        Raises:
            FileNotFoundError: If the CSV file does not exist.
            ValueError: If the CSV file is empty or invalid.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {self.file_path}"
            )

        logger.info(f"Extracting data from {self.file_path}")

        try:
            df = pd.read_csv(self.file_path)

            if df.empty:
                raise ValueError(
                    f"CSV file is empty: {self.file_path}"
                )

            logger.info(
                f"Extracted {len(df)} records from {self.file_path}"
            )
            return df

        except pd.errors.EmptyDataError as e:
            raise ValueError(
                f"CSV file is empty or invalid: {self.file_path}"
            ) from e
        except Exception as e:
            logger.error(
                f"Error extracting data from {self.file_path}: {e}"
            )
            raise
